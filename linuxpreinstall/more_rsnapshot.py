from __future__ import print_function

import json
import os
import platform
import shutil
import sys

from collections import OrderedDict

if __name__ == "__main__":
    MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
    REPO_DIR = os.path.dirname(MODULE_DIR)
    sys.path.insert(0, REPO_DIR)

from linuxpreinstall.sysdirs import (
    sysdirs,
    SystemPaths,
)

from linuxpreinstall.readonlydict import ReadOnlyDict

_, me = os.path.split(__file__)

default_settings = ReadOnlyDict()
default_settings['backup_drive'] = '/mnt/small'
default_settings['rsnapshot_flag_dir'] = 'rsnapshot'
default_settings['snapshot_root'] = os.path.join(
    default_settings['backup_drive'],
    default_settings['rsnapshot_flag_dir']
)
default_settings['backup_unused_fuse_mountpoint_fmt'] = '/media/{}/main'
default_settings.readonly()


SYS_USERS = ('systemd', 'root', 'cron')
ROOT_SETTINGS_DIR = "/etc/linuxpreinstall"

settings_dir = os.path.join(
    sysdirs['LOCALAPPDATA'],
    "linuxpreinstall"
)

IS_ROOT_MODE = False
RSNAPSHOT_LOG_NAME = 'rsnapshot.log'
RSNAPSHOT_LOG = os.path.join('/var/log', RSNAPSHOT_LOG_NAME)

if platform.system() == "Windows":
    USER = os.environ['USERNAME']
    SYS_USERS = ('Administrator', 'LocalService')
    ROOT_SETTINGS_DIR = settings_dir
    IS_ROOT_MODE = True
else:
    # USER = os.getlogin()  returns unpriv. GUI user in root terminal window!
    USER = os.environ.get('USER')
    # NOTE: USER is not set when run by cron!
    if USER in SYS_USERS + [None, ""]:
        settings_dir = ROOT_SETTINGS_DIR
        IS_ROOT_MODE = True
    else:
        print("Warning: Running as {} but expected one among {}"
              .format(USER, SYS_USERS),
              file=sys.stderr)

SETTINGS_JSON_NAME = "more_rsnapshot.json"  # *Not* the generated json

ROOT_SETTINGS_FILE = os.path.join(
    ROOT_SETTINGS_DIR,
    SETTINGS_JSON_NAME
)

BAD_DESTINATIONS = ("/", "c:", "c:\\")
BAD_DESTINATION_STARTS = ("/bin", "/etc", "/lib", "/lib.usr-is-merged",
                          "/opt", "/bin.usr-is-merged", "/cdrom", "/lib64",
                          "/proc", "/sbin", "/dev", "/boot", "/sys",
                          "/var", "/usr", "c:\\", "c:")

settings_file = os.path.join(
    settings_dir,
    SETTINGS_JSON_NAME
)


def vars_from_rsnapshot_conf(path):
    meta = OrderedDict()
    line_n = -1
    with open(path, 'r') as stream:
        for _raw in stream:
            line_n += 1
            line = _raw.strip()
            if line.startswith("#"):
                # Comment
                continue
            if not line.strip():
                # Blank line
                continue
            tabI = line.find("\t")
            if tabI == 0:
                print("{}, line {}: Warning: tab before var name in `{}`"
                      .format(path, line_n, line))
                continue
            elif tabI < 0:
                print("{}, line {}: Warning: no tab after var name in `{}`"
                      .format(path, line_n, line))
                continue
            k = line[:tabI].strip()
            v = line[tabI:].strip()
            meta[k] = v
    return meta


def get_user_settings_path(user):
    this_settings_dir = settings_dir
    if (user in SYS_USERS) or (platform.system() == "Windows"):
        this_settings_dir = ROOT_SETTINGS_DIR

    this_settings_file = os.path.join(
        this_settings_dir,
        SETTINGS_JSON_NAME
    )
    return this_settings_file


def get_user_settings(user):

    settings = ReadOnlyDict()
    this_settings_file = get_user_settings_path(user)
    _settings_file_bad = this_settings_file + ".bad"

    if os.path.isfile(this_settings_file):
        try:
            with open(this_settings_file, 'r') as stream:
                _settings_dict = json.load(stream)
            settings.update(_settings_dict)
        except Exception as ex:
            if os.path.isfile(_settings_file_bad):
                os.remove(_settings_file_bad)
            shutil.move(this_settings_file, _settings_file_bad)
            print(
                "[{} \"{}\"] {}: {}"
                .format(me, this_settings_file, type(ex).__name__, ex),
                file=sys.stderr)

    for k, v in default_settings.items():
        if k not in settings:
            settings[k] = v

    if settings['snapshot_root'].endswith(os.path.sep):
        print(
            "Warning: snapshot_root=\"{}\" (from \"{}\")"
            " ends with \"{}\" which will be removed."
            .format(settings['snapshot_root'], this_settings_file,
                    os.path.sep)
        )
        settings['snapshot_root'] = \
            settings['snapshot_root'].rstrip(os.path.sep)

    try_real_file = "/opt/etc/rsnapshot.conf"
    if os.path.isfile(try_real_file):
        conf = vars_from_rsnapshot_conf(try_real_file)
        no_create_root_msg = None

        if 'no_create_root' not in conf:
            no_create_root_msg = "(currently not set)"
        elif conf['no_create_root'] != "1":
            no_create_root_msg = ("(currently {})"
                                  .format(conf['no_create_root']))
        if no_create_root_msg:
            print("Warning: `no_create_root\t1` should be used"
                  " {} in \"{}\" for removable drives"
                  " to ensure they are mounted"
                  " and that the mountpoint isn't made unusable"
                  " by containing files from '/'!"
                  .format(no_create_root_msg, try_real_file))
        if 'snapshot_root' not in conf:
            print("Warning: No snapshot_root in \"{}\""
                  .format(try_real_file))
        else:
            conf['snapshot_root'] = \
                conf['snapshot_root'].rstrip(os.path.sep)
            if (conf['snapshot_root']
                    != settings['snapshot_root']):
                print(
                    "[{}] Warning: changing snapshot_root=\"{}\" (from \"{}\")"
                    " to match snapshot_root=\"{}\" (from \"{}\")"
                    .format(os.path.realpath(__file__),
                            settings['snapshot_root'], this_settings_file,
                            conf['snapshot_root'], try_real_file)
                )

                settings['snapshot_root'] = \
                    conf['snapshot_root'].rstrip(os.path.sep)
                # ^ Remove trailing slash, or os.path.dirname
                #   will only remove that!
                bad_start = None
                if settings['snapshot_root']:
                    for _bad_start in BAD_DESTINATION_STARTS:
                        lower = settings['snapshot_root'].lower()
                        if lower.startswith(_bad_start):
                            bad_start = _bad_start
                if ((not settings['snapshot_root']) or bad_start
                        or (settings['snapshot_root'] in BAD_DESTINATIONS)):
                    suffix = ""
                    if bad_start:
                        suffix = (" should not start with \"{}\""
                                  .format(bad_start))
                    raise ValueError("Bad snapshot setting=\"{}\"{}"
                                     .format(settings['snapshot_root'],
                                             suffix))
    else:
        print("Warning: no {}".format(try_real_file))

    try_drive = os.path.dirname(settings['snapshot_root'])
    if settings['backup_drive'] != try_drive:
        print("Warning: got backup_drive=\"{}\""
              " but expected a parent of \"{}\" such as {}"
              .format(settings['backup_drive'], settings['snapshot_root'],
                      try_drive))

    _userspace_comment = (
        "This file will only be used for a user-space backup of {}."
        " See {} for the root configuration"
        " such as runs from the cron job specified"
        " in the more_rsnapshot documentation"
        " in linux-preinstall.".format(user, ROOT_SETTINGS_FILE)
    )

    scope_comment = _userspace_comment

    _root_comment = "This file will be used by cron jobs."

    if user == "root":
        scope_comment = _root_comment

    if platform.system() != "Windows":
        settings['comment'] = scope_comment
    return settings


settings = get_user_settings(os.getlogin())
settings.readonly()

if not os.path.isfile(settings_file):
    if not os.path.isdir(settings_dir):
        os.makedirs(settings_dir)

    with open(settings_file, 'w') as stream:
        json.dump(settings, stream)
    print("[{}] Created a new \"{}\"".format(me, settings_file))

if sys.version_info.major < 3:
    FileNotFoundError = IOError
    ModuleNotFoundError = ImportError
    NotADirectoryError = OSError


class TMTimer:
    """Partial timer class based on backupnow.taskmanager"""
    time_fmt = "%H:%M"
    date_fmt = "%Y-%m-%d"
    dt_fmt = date_fmt + " " + time_fmt
    # dow_name_fmt = "%A"  # full name of day of week (first letter capital)
    dow_index_fmt = "%w"  # Number of day of week where Sunday is 0.


LOG_NAME = "linuxpreinstall.rsnapshot.log"
LOG = os.path.join('/var/log', LOG_NAME)
if not IS_ROOT_MODE:
    LOG = os.path.join(sysdirs['LOGS'], LOG_NAME)


def state_path(home):
    if home:
        user_sysdirs = SystemPaths()
        user_sysdirs.init_platform(platform.system(), home=home)
    else:
        user_sysdirs = sysdirs
    rsnapshot_json = os.path.join(user_sysdirs['HOME'],
                                  'linuxpreinstall.rsnapshot.json')
    return rsnapshot_json


GENERATED_USER_EXCLUDES_NAME = 'more_rsnapshot.generated_excludes.txt'
GENERATED_ABS_EXCLUDES_NAME = 'more_rsnapshot.generated_absolute_excludes.txt'


def excludes_path(home, IS_ROOT=False, IS_ABSOLUTE=False):
    if home:
        user_sysdirs = SystemPaths()
        user_sysdirs.init_platform(platform.system(), home=home)
    else:
        user_sysdirs = sysdirs
    rsnapshot_cache_dir = os.path.join(user_sysdirs['CACHES'],
                                       'linuxpreinstall')
    if IS_ROOT:
        if platform.system() != "Windows":
            rsnapshot_cache_dir = "/opt/etc"
    name = GENERATED_USER_EXCLUDES_NAME
    if IS_ABSOLUTE:
        name = GENERATED_ABS_EXCLUDES_NAME
    rsnapshot_cache = os.path.join(rsnapshot_cache_dir, name)
    return rsnapshot_cache


rsnapshot_json = state_path(None)  # None defaults to current user
rsnapshot_excludes_txt = excludes_path(None, IS_ROOT=IS_ROOT_MODE)
# ^ None defaults to current user


MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(MODULE_DIR)

rel_install_paths = [
    os.path.join("etc", "cron.d", "rsnapshot-linux-preinstall")
]
for rel in rel_install_paths:
    install_files = []
    src = os.path.join(MODULE_DIR, "static", "more_rsnapshot", rel)
    dst = "/" + rel
    install_files.append(
        (src, dst)
    )

DEST_CRON_D = "/etc/cron.d"


def install_rsnapshot_scripts():
    """Install linux-preinstall's rsnapshot automation scripts.

    Ensure /opt/bin directory exists, then attempt to
    create symbolic links to linux-preinstall's rsnapshot scripts.

    Troubleshooting:
    > Can cron run your job?
    > Check /var/log/cron.log or /var/log/messages for errors.
    > Ubuntu: grep CRON /var/log/syslog
    > Redhat: /var/log/cron
    > . . .
    > service cron restart
    -<https://stackoverflow.com/a/22744360>

    Returns:
        int: Returns 0 if all symlinks are created successfully. Returns 1
            if a PermissionError occurs, or if there is an issue creating
            symlinks.

    Raises:
        Exception: If an unexpected exception occurs during symlink creation.
    """
    # alternative to:
    # cd linux-preinstall/utilities && sudo mkdir -p /opt/bin \
    #  && sudo ln -s `pwd`/before_rsnapshot.py /opt/bin/before_rsnapshot.py \
    #  && sudo ln -s `pwd`/before_rsnapshot.sh /opt/bin/before_rsnapshot.sh \
    #  && sudo ln -s `pwd`/generate_exclude.py /opt/bin/generate_exclude.py \
    #  && sudo ln -s `pwd`/rsnapshot_logged.py /opt/bin/rsnapshot_logged.py \
    #  && sudo ln -s `pwd`/rsnapshot_logged.sh /opt/bin/rsnapshot_logged.sh
    # cd ../linuxpreinstall \
    #  && sudo cp static/more_rsnapshot/etc/cron.d/rsnapshot-linux-preinstall \
    #   /etc/cron.d/
    #  && sudo chown 0:0 /etc/cron.d/rsnapshot-linux-preinstall
    if platform.system() == "Windows":
        raise OSError("{} is not supported by linux-preinstall's rsnapshot"
                      " scripts."
                      .format(platform.system()))
    scripts_dir = os.path.join(REPO_DIR, "utilities")

    # Ensure the /opt/bin directory exists
    os.makedirs("/opt/bin", exist_ok=True)

    # Define the files to link
    files_to_link = [
        "before_rsnapshot.py",
        "before_rsnapshot.sh",
        "generate_exclude.py",
        "rsnapshot_logged.py",
        "rsnapshot_logged.sh"
    ]

    for filename in files_to_link:
        target = os.path.join(scripts_dir, filename)
        dst = os.path.join("/opt/bin", filename)

        try:
            if os.path.isfile(dst) and not os.path.islink(dst):
                print("Error: {} exists as a regular file.".format(dst),
                      file=sys.stderr)
                return 1

            if os.path.islink(dst):
                existing_target = os.readlink(dst)
                if existing_target != target:
                    print("Error: {} exists but points to {} instead of {}."
                          .format(dst, existing_target, target),
                          file=sys.stderr)
                    return 1

            os.symlink(target, dst)

        except PermissionError:
            print("Permission denied: unable to create symlink at {}."
                  .format(dst), file=sys.stderr)
            return 1

    if not os.path.isdir(DEST_CRON_D):
        print("There is no \"{}\"".format(DEST_CRON_D), file=sys.stderr)
        return 1
    for src, dst in install_files:
        shutil.copy(src, dst)  # does overwrite
        if dst.startswith("/etc/cron."):
            os.chown(dst, 0, 0)  # required for cron scripts
            # ^ (prevents "2024-08-12T13:15:01.269357-04:00 pgs
            #   cron[536868]: (*system*rsnapshot-linux-preinstall) WRONG
            #   FILE OWNER (/etc/cron.d/rsnapshot-linux-preinstall)"
            #   in /var/log/syslog)!

    return 0
