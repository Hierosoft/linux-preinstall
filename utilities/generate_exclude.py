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
/etc/rsnapshot.conf (or /opt/rsnapshot.conf used by Poikilos machines or
scripts) as follows:

exclude_file	/opt/etc/exclude_from_backup-absolute-generated.txt

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
import sys
import os
# import platform

SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(SCRIPTS_DIR)

if os.path.isfile(os.path.join(REPO_DIR, "linuxpreinstall", "__init__.py")):
    sys.path.insert(0, REPO_DIR)


from linuxpreinstall import (  # noqa: F401, E402
    USER_DIR_NAME,
    echo0,
    echo1,
    echo2,
    HOME,  # profile,
    PROFILES,
)

if sys.version_info.major < 3:
    try:
        PermissionError = WindowsError
    except:
        # TODO: make sure what actually is raised on `open`
        #   when file is not writable in Python 2
        PermissionError = OSError
    FileNotFoundError = IOError
    ModuleNotFoundError = ImportError


def generate_user_exclude(partial_files, new_src_txt):
    with open(new_src_txt, "w") as outs:
        for in_name in partial_files:
            in_path = os.path.join(HOME, in_name)
            if not os.path.isfile(in_path):
                raise FileNotFoundError("Missing {}".format(in_path))
            with open(in_path, "r") as ins:
                for line in ins:
                    if not line.strip():
                        continue
                    outs.write(line)
    return 0


class ExcludeMaker:
    src_txt = None  # Accessible from anywhere so can be used in Usage screen!

    def __init__(self, user_only=False):
        global HOME
        global PROFILES
        global USER_DIR_NAME
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
        # ExcludeMaker.src_txt = os.path.join(HOME, self.src_txt_name)
        ExcludeMaker.src_txt = os.path.join("/tmp", self.src_txt_name)

        self.tmp_txt = ExcludeMaker.src_txt

        self.dst_confs = os.path.join("/opt", "etc")
        old_dst_confs = os.path.join("/opt", "rsnapshot")
        self.dst_txt = os.path.join(
            self.dst_confs,
            "exclude_from_backup-absolute-generated.txt")
        old_dst_txt = os.path.join(
            old_dst_confs,
            "exclude_from_backup-absolute-generated.txt")
        if os.path.isfile(old_dst_txt):
            if not os.path.isdir(self.dst_confs):
                os.makedirs(self.dst_confs)
            if os.path.isfile(self.dst_txt):
                raise OSError(
                    "You have old \"{}\" and new \"{}\""
                    " but should only have the new one."
                    .format(old_dst_txt, self.dst_txt))

        self.enable_chown = False
        try_homes = [
            os.path.realpath("."),
            os.path.join("/home", "owner")
        ]

        self.found_src_txt_name = False

        if not os.path.isfile(ExcludeMaker.src_txt):
            for try_home in try_homes:
                self.enable_chown = True
                try_txt = os.path.join(try_home, self.src_txt_name)
                if os.path.isfile(try_txt):
                    ExcludeMaker.src_txt = try_txt
                    self.found_src_txt_name = True
                    HOME = try_home
                    PROFILES, USER_DIR_NAME = os.path.split(HOME)
                    # ^ Override ones from the linuxpreinstall module
                    echo0("* detected {}".format(try_txt))
                    break
        echo0('PROFILES="{}"'.format(PROFILES))
        echo0('USER_DIR_NAME="{}"'.format(USER_DIR_NAME))
        echo0('HOME="{}"'.format(HOME))
        echo0('ExcludeMaker.src_txt="{}"'.format(ExcludeMaker.src_txt))

    def run(self):
        """Generate the exclude file(s) based on the user_only setting.

        Returns:
            int: 0 if ok, or error code if False.
        """
        self.user_only
        if self.user_only:
            echo0("mode=\"user\"")

            if os.path.isfile(ExcludeMaker.src_txt):
                echo0("Warning: There is already a {}. Rewriting..."
                      .format(ExcludeMaker.src_txt))
            generate_user_exclude(self.src_parts, ExcludeMaker.src_txt)
            if os.path.isfile(ExcludeMaker.src_txt):
                echo0("Generated \"{}\" from {}"
                      .format(ExcludeMaker.src_txt, self.src_parts))
            else:
                echo0("Error: failed to generate \"{}\" from {}"
                      .format(ExcludeMaker.src_txt, self.src_parts))
                return 1
            return 0
        echo0("mode=\"user+system\"")
        if not self.found_src_txt_name:
            # echo0("Warning: no {} in any of: {}, so using default \"{}\""
            #     .format(self.src_txt_name, try_homes, ExcludeMaker.src_txt))
            # ^ That's expected now--it should be generated by:
            #   generate_exclude.py --user
            #   so:
            if not os.path.isfile(ExcludeMaker.src_txt):
                echo0(
                    "An administrator"
                    " must delete {tmp} and run this as {user}"
                    " with --user option:\n"
                    " sudo -u {user} {mypath} --user"
                    .format(user="some_user", mypath=__file__,
                            tmp=self.tmp_txt))
        if not os.path.isdir(self.dst_confs):
            try:
                os.makedirs(self.dst_confs)
            except PermissionError as ex:
                echo0(str(ex))
                echo0(
                    'You must create "{}" and give "{}" the write permission.'
                    .format(self.dst_confs, os.getlogin()))
                return 1
        code = self.generate_absolute_paths()
        return code

    def _generate_absolute_paths(self, ins, outs):
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

                parent = os.path.join(HOME, os.path.split(path)[0])
                # ^ OK since ignores HOME if 2nd param starts with /
                #   but see the other join command further down
                #   which has to check manually since adding "*"
                list_name = "1.list_of_zips.txt"
                list_path = os.path.join(parent, list_name)
                if not os.path.isfile(list_path):
                    matches = []
                    for sub in os.listdir(parent):
                        # subPath = os.path.join(parent, sub)
                        if sub.lower().endswith(".zip"):
                            matches.append(sub)
                    if len(matches) > 0:
                        this_gid = None
                        this_uid = None
                        with open(list_path, 'w') as f:
                            f.write("# generated by generate_exclude.py\n")
                            for sub in matches:
                                subPath = os.path.join(parent, sub)
                                if this_uid is None:
                                    this_uid = os.stat(subPath).st_uid
                                if this_gid is None:
                                    this_gid = os.stat(subPath).st_gid
                                f.write(sub + "\n")
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
                        echo0(
                            '* skipped creating 0-length "{}"'
                            .format(list_path))
                else:
                    echo0('* skipped existing "{}"'.format(list_path))
            if not path.startswith(PROFILES):
                # and (not path.startswith("/")):
                # ^ starting with / doesn't matter since
                #   that prevents PROFILES and * to be prepended anyway
                #   (the check makes no difference):
                path = os.path.join(PROFILES, "*", path)
            outs.write(path + "\n")
        return results['src_count']

    def generate_absolute_paths(self):
        results = {}
        try:
            with open(ExcludeMaker.src_txt, 'r') as ins:
                with open(self.dst_txt, 'w') as outs:
                    gen_res = self._generate_absolute_paths(ins, outs)
                    results.update(gen_res)

        except PermissionError as ex:
            if self.dst_txt in str(ex):
                echo0("{}: {}".format(type(ex).__name__, ex))
                echo0(
                    "If {user} is not an administrator, an administrator"
                    " must delete {tmp} and run this as {user}"
                    " with --user option:\n"
                    " sudo -u {user} {mypath} --user"
                    .format(user=os.getlogin(), mypath=__file__,
                            tmp=self.dst_txt))
                return 1
            else:
                raise
        echo0(
            '* processed {} line(s) from "{}" and generated "{}"'
            .format(results.get('src_count'), ExcludeMaker.src_txt,
                    self.dst_txt))
        return 0


def usage():
    echo0(__doc__.format(
        exclude_from_backup=ExcludeMaker.src_txt,
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
