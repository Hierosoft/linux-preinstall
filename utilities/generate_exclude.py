#!/usr/bin/env python3
'''
generate_exclude
----------------
Author: Jake Gustafson

This script generates a root exclude list suitable for rsync's
--exclude-from option or rsnapshot.conf. It reads:
$USERPROFILE/exclude_from_backup.txt.

This script must run as the user that has that file.

For use with rsnapshot, uncomment and change the exclude_file line in
/etc/rsnapshot.conf (or /opt/etc/rsnapshot.conf used by Poikilos machines or
scripts) as follows:

exclude_file	/opt/etc/more_rsnapshot.generated_absolute_excludes.txt
# (linuxpreinstall.more_rsnapshot.GENERATED_ABS_EXCLUDES_NAME)

Other features:
- generates a 1.list_of_zips.txt in each directory where "*.zip" is
  excluded, as a record of which zips were excluded from the backup
  (The full path is calculated using the location of the
  exclude_from_backup.txt file).
- The current working directory can be used as the HOME directory if it
  contains exclude_from_backup.txt. This is useful such as if the
  User's directory is mounted at a special location during a drive
  recovery where only files not excluded are desired.

For further rsnapshot notes and a setup specific to Poikilos machines
and scripts such as linux-preinstall, see
linux-preinstall/doc/rsnapshot.md.

Options:
--user              Only generate the {exclude_from_backup}
                    (combined user excludes) temp file. It is still
                    generated anyway, but exit afterward in this case.

--help              Show this help screen then exit.
'''
import json
import os
import sys
# import platform

from collections import OrderedDict
from datetime import (
    timezone,
    datetime,
)

SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(SCRIPTS_DIR)

if os.path.isfile(os.path.join(REPO_DIR, "linuxpreinstall", "__init__.py")):
    sys.path.insert(0, REPO_DIR)


from linuxpreinstall import (  # noqa: F401, E402
    echo0,
    echo1,
    echo2,
)
from linuxpreinstall.sysdirs import (  # noqa: F401, E402
    sysdirs,
)

# HOME = None
# PROFILES = None
# USER_DIR_NAME = None

if sys.version_info.major < 3:
    try:
        PermissionError = WindowsError
    except:
        # TODO: make sure what actually is raised on `open`
        #   when file is not writable in Python 2
        PermissionError = OSError
    FileNotFoundError = IOError
    ModuleNotFoundError = ImportError

from linuxpreinstall.more_rsnapshot import (
    TMTimer,
    LOG,
    settings,
    IS_ROOT_MODE,
    state_path,
    excludes_path,
    rsnapshot_json,
    rsnapshot_excludes_txt,
)

_, me = os.path.split(__file__)


def generate_user_exclude(partial_files, new_src_txt, home):
    count = 0
    if not home:
        raise ValueError("home was blank")
    new_src_txt_dir = os.path.dirname(new_src_txt)
    if not os.path.isdir(new_src_txt_dir):
        os.makedirs(new_src_txt_dir)
    subcounts = {}
    with open(new_src_txt, "w") as outs:
        for in_name in partial_files:
            subcounts[in_name] = 0
            in_path = os.path.join(home, in_name)
            if not os.path.isfile(in_path):
                raise FileNotFoundError("Missing {}".format(in_path))
            with open(in_path, "r") as ins:
                for line in ins:
                    if not line.strip():
                        continue
                    subcounts[in_name] += 1
                    outs.write(line)
                    count += 1
    echo0("[{}] generated \"{}\" with {} line(s) combined from {}"
          .format(me, new_src_txt, count, subcounts))
    return 0


class ExcludeMaker:
    """Manage rsync (or rsnapshot) exclude files.
    Convert relative paths (for user[s]) to absolute paths.

    Attributes:
        env(dict[str]): Settings to pass along to before_rsnapshot.py,
            rsnapshot_logged.py, and any other scripts that need to
            know which user(s) have exclusion lists to join and make
            absolute.
    """

    def __init__(self, user_only=False):
        self.env = OrderedDict()
        self.env['users'] = OrderedDict()

        now = datetime.now(timezone.utc)
        utc_dt = now.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_dt.timestamp()
        # print(utc_timestamp)

        self.env['generate_start_utc_tc'] = utc_timestamp
        self.env['generate_start_utc_dt'] = utc_dt.strftime(TMTimer.dt_fmt)
        self.env['PROFILES'] = None
        self.env['USER_DIR_NAME'] = None
        if user_only is None:
            user_only = False
        self.user_only = user_only

        self._src_count = None

        self.src_parts = [
            "exclude_less_from_backup.txt",  # maybe keep large downloads etc
            "exclude_more_from_backup.txt",  # exclude reproducible/history/etc
        ]
        # ^ formerly there was only /home/owner/exclude_from_backup.txt

        self.src_txt_name = "exclude_from_backup.txt"

        self.enable_chown = False
        # try_homes = [
        #     os.path.realpath("."),
        #     os.path.join("/home", "owner")
        # ]
        try_homes = []
        if IS_ROOT_MODE:
            if os.path.isdir(sysdirs['PROFILES']):
                for sub in os.listdir(sysdirs['PROFILES']):
                    try_homes.append(os.path.join(sysdirs['PROFILES'], sub))

        self.homes = None
        self.other_user = None
        self.other_user_home = None

        for try_home in try_homes:
            # Will *not* iterate unless IS_ROOT_MODE (See `try_homes =` above)
            homes, user = os.path.split(try_home)
            # FIXME: Allow more than one (combine, & remove break below).
            self.enable_chown = True
            try_user_state_path = state_path(try_home)
            if os.path.isfile(try_user_state_path):
                self.other_user = user
                self.homes = homes
                self.other_user_home = try_home
                if 'users' not in self.env:
                    self.env['users'] = OrderedDict()
                with open(try_user_state_path, 'r') as stream:
                    self.env['users'][user] = json.load(stream)
                echo0("* detected {}".format(try_user_state_path))
                break
        for k, v in self.env.items():
            if "=" in k:
                self.env['error'] = ("Found '=' in variable name `{}`"
                                     .format(k))
                self.save_env()
                raise ValueError(self.env['error'])
            echo0('{}="{}"'.format(k, v))
        self.env['status'] = 1

    def run(self):
        """Generate the exclude file(s) based on the user_only setting.

        Returns:
            int: 0 if ok, or error code if False.
        """
        if self.user_only:
            # This mode is for a low-privilege run.
            self.env['mode'] = "user"
            echo0("mode=\"{}\"".format(self.env['mode']))

            if os.path.isfile(rsnapshot_excludes_txt):
                echo0("Warning: There is already a {}. Rewriting..."
                      .format(rsnapshot_excludes_txt))
            generate_user_exclude(self.src_parts, rsnapshot_excludes_txt,
                                  home=sysdirs['HOME'])
            # ^ Find src_parts in current home in user_only mode.
            if os.path.isfile(rsnapshot_excludes_txt):
                # Already shown above (with line count)
                pass
                # echo0("Generated \"{}\" from {}"
                #       .format(rsnapshot_excludes_txt, self.src_parts))
            else:
                echo0("Error: failed to generate \"{}\" from {}"
                      .format(rsnapshot_excludes_txt, self.src_parts))
                return 1
            self.env['status'] = 0
            self.save_env()
            return 0
        # Anything past here may require administrator privileges.
        self.env['mode'] = "user+system"
        echo0("mode=\"{}\"".format(self.env['mode']))

        code = self.generate_absolute_paths()
        self.save_env()
        return code

    def save_env(self):
        self.env['user_only'] = self.user_only
        self.env['AS_ROOT'] = IS_ROOT_MODE
        with open(rsnapshot_json, 'w') as stream:
            json.dump(self.env, stream)

    def target_home(self):
        if self.other_user_home:
            return self.other_user_home
        return sysdirs['HOME']

    def target_homes(self):
        return os.path.dirname(self.target_home())

    def _generate_absolute_paths(self, profiles, home, ins, outs):
        if (not profiles) or (profiles == "/"):
            raise ValueError(
                "Incorrect path profiles=\"{}\""
                " (Should be parent of home=\"{}\")"
                .format(profiles, home))
        results = {}
        results['src_count'] = 0
        for rawL in ins:
            line = rawL.strip()
            if len(line) < 1:
                continue
            path = line
            results['src_count'] += 1
            if path.endswith("*.zip"):
                # Leave a trail of breadcrumbs for downloads:
                parent = os.path.join(home, os.path.split(path)[0])
                # ^ OK since ignores base if 2nd param starts with /
                #   but see the other join command further down
                #   which has to check manually since adding "*"
                list_name = "1.list_of_zips.txt"
                list_path = os.path.join(parent, list_name)
                self.env['list_path'] = list_path
                if not os.path.isfile(list_path):
                    self.env['list_path_count'] = 0
                    self.env['list_path_status'] = "generated"
                    matches = []
                    for sub in os.listdir(parent):
                        # subPath = os.path.join(parent, sub)
                        if sub.lower().endswith(".zip"):
                            matches.append(sub)
                    if len(matches) > 0:
                        this_gid = None
                        this_uid = None
                        with open(list_path, 'w') as f:
                            f.write("# generated by {}\n".format(me))
                            for sub in matches:
                                subPath = os.path.join(parent, sub)
                                if this_uid is None:
                                    this_uid = os.stat(subPath).st_uid
                                if this_gid is None:
                                    this_gid = os.stat(subPath).st_gid
                                f.write(sub + "\n")
                                self.env['list_path_count'] += 1
                        echo0('* generated "{}"'.format(list_path))
                        if self.enable_chown:
                            echo0(
                                "  - changing to uid={} gid={}"
                                .format(this_uid, this_gid))
                            if (this_uid is None) or (this_gid is None):
                                echo0(
                                    "    FAILED:"
                                    " no uid or gid found for the files"
                                )
                            else:
                                os.chown(list_path, this_uid, this_gid)
                    else:
                        self.env['list_path_status'] = \
                            "skipped_generating_empty"
                        echo0(
                            '* skipped creating 0-length "{}"'
                            .format(list_path))

                else:
                    self.env['list_path_count'] = None
                    self.env['list_path_status'] = "kept"
                    echo0('* skipped existing "{}"'.format(list_path))
            if not path.startswith(profiles):
                # and (not path.startswith("/")):
                # ^ starting with / doesn't matter since
                #   that prevents root
                #   and * to be prepended anyway
                #   (the check makes no difference):
                path = os.path.join(profiles, "*", path)
            outs.write(path + "\n")
        return results

    def check_parent_of_dest_txt(self, excludes_txt, IS_ROOT=False):
        # gen_excludes_dir = os.path.join("/opt", "etc")
        gen_excludes_dir = os.path.dirname(excludes_txt)
        if IS_ROOT:
            old_dst_confs = os.path.join("/opt", "rsnapshot")
            old_dst_txt = os.path.join(
                old_dst_confs,
                "exclude_from_backup-absolute-generated.txt")
            # NOTE: new one is GENERATED_ABS_EXCLUDES_NAME
            #   in linuxpreinstall.more_rsnapshot
            if os.path.isfile(old_dst_txt):
                if not os.path.isdir(gen_excludes_dir):
                    os.makedirs(gen_excludes_dir)
                if os.path.isfile(excludes_txt):
                    raise OSError(
                        "You have old \"{}\" and new \"{}\""
                        " but should only have the new one."
                        .format(old_dst_txt, excludes_txt))
        if not os.path.isdir(gen_excludes_dir):
            try:
                os.makedirs(gen_excludes_dir)
            except PermissionError as ex:
                echo0(str(ex))
                echo0(
                    'You must create "{}" and give "{}" the write permission.'
                    .format(gen_excludes_dir, os.getlogin()))
                return 1

    def generate_absolute_paths(self):
        results = {}
        if IS_ROOT_MODE:
            if not self.other_user_home:
                some_home = os.path.join(sysdirs['PROFILES'], "$OTHER_USER")
                some_x = excludes_path(some_home, IS_ABSOLUTE=False,
                                       IS_ROOT=False)
                raise ValueError(
                    "There was no {} found in any user profile in {}."
                    " Create at least one {}, set OTHER_USER then"
                    " generate the combined {} as follows:"
                    " sudo -u $OTHER_USER ./generate_exclude --user"
                    .format(some_x,
                            sysdirs['PROFILES'],
                            self.src_parts,
                            some_x)
                )
            rel_excludes_txt = excludes_path(
                self.other_user_home,
                IS_ABSOLUTE=False,
                IS_ROOT=False)
            abs_excludes_txt = excludes_path(
                None,
                IS_ABSOLUTE=True,
                IS_ROOT=IS_ROOT_MODE)
        else:
            rel_excludes_txt = excludes_path(
                None,
                IS_ABSOLUTE=False,
                IS_ROOT=False)
            abs_excludes_txt = excludes_path(
                None,
                IS_ABSOLUTE=True,
                IS_ROOT=False)
            if rel_excludes_txt.startswith("/root"):
                raise NotImplementedError(
                    "Got a /root source in non-root mode for"
                    " {} (user_only={}): {}"
                    .format(sysdirs['HOME'],
                            self.user_only,
                            rel_excludes_txt))

        self.check_parent_of_dest_txt(abs_excludes_txt,
                                      IS_ROOT=IS_ROOT_MODE)

        try:
            with open(rel_excludes_txt, 'r') as ins:
                with open(abs_excludes_txt, 'w') as outs:
                    gen_result = self._generate_absolute_paths(
                        self.target_homes(), self.target_home(), ins, outs)
                    results.update(gen_result)

        except PermissionError as ex:
            if abs_excludes_txt in str(ex):
                echo0("{}: {}".format(type(ex).__name__, ex))
                echo0(
                    "If {user} is not an administrator, an administrator"
                    " must delete {tmp} and run this as {user}"
                    " with --user option:\n"
                    " sudo -u {user} {mypath} --user"
                    .format(user=os.getlogin(), mypath=__file__,
                            tmp=abs_excludes_txt))
                return 1
            else:
                raise
        echo0(
            '* processed {} line(s) from "{}" and generated "{}"'
            .format(results.get('src_count'), rel_excludes_txt,
                    abs_excludes_txt))
        if 'error' in results:
            echo0(results['error'])
            return 1
        return 0


def usage():
    echo0(__doc__.format(
        exclude_from_backup=excludes_path(None),
    ))


def main():
    echo0("args=\"{}\"".format(sys.argv))
    user_only = False
    for argi in range(1, len(sys.argv)):
        arg = sys.argv[argi]
        if arg == "--user":
            user_only = True
        elif arg == "--help":
            usage()
            return 0
    maker = ExcludeMaker(user_only=user_only)
    code = maker.run()
    return code


if __name__ == "__main__":
    sys.exit(main())
