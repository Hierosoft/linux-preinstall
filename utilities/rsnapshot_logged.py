#!/usr/bin/env python3
# formerly rsnapshot-logged.sh
import os
import shutil
import sys
import subprocess

if __name__ == "__main__":
    SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
    REPO_DIR = os.path.dirname(SCRIPTS_DIR)
    sys.path.insert(0, REPO_DIR)


from linuxpreinstall.more_rsnapshot import (
    # TMTimer,
    LOG,
    LOG_NAME,
    settings,
    RSNAPSHOT_LOG,
    RSNAPSHOT_LOG_NAME,
)
_, me = os.path.split(__file__)


def run_command(command):
    """Run a command and return the returncode of the process."""
    print("[{}] Running: {}".format(command, me))
    try:
        subprocess.check_call(command, shell=True)
        return 0  # Success
    except subprocess.CalledProcessError as e:
        return e.returncode  # Return the error code


def rsnapshot_logged(backup_type):
    if not backup_type:
        print(
            "[{}] Error: expected argument: backup type"
            " (such as alpha, beta, gamma, or delta)"
            .format(me),
            file=sys.stderr,
        )
        return 1

    command = ('/usr/bin/rsnapshot -c /opt/etc/rsnapshot.conf {}'
               .format(backup_type))
    code = run_command(command)
    # Write to LOG after rsnapshot
    with open(LOG, 'a') as logfile:
        logfile.write("[{}]\n".format(me))
        logfile.write("# region after backup\n")
        logfile.write('last_backup_type="{}"\n'.format(backup_type))
        if code != 0:
            logfile.write('status="FAILED"\n')
            logfile.write('error={}\n'.format(code))
        else:
            logfile.write('status="OK"\n')

    # Check and copy logs
    if os.path.isdir(settings['snapshot_root']):
        dst_logs = settings['backup_drive']
        if not os.path.isdir(dst_logs):
            # makedirs *only* when has settings['snapshot_root']
            #   not just mountpoint:
            os.makedirs(dst_logs)
        with open(LOG, 'a') as logfile:
            logfile.write("# endregion after backup\n")
        shutil.copy(LOG, os.path.join(dst_logs, LOG_NAME))
        shutil.copy(RSNAPSHOT_LOG, os.path.join(dst_logs, RSNAPSHOT_LOG_NAME))
        if not os.path.isdir("/opt/etc"):
            os.makedirs("/opt/etc")
        with open("/opt/etc/rsnapshot-generated.rc") as stream:
            for k, v in settings.items():
                stream.write("{}=\"{}\"\n".format(k, v))
    else:
        error = ("[{}] Error: {} is no longer mounted (no {})"
                 .format(me, settings['backup_drive'],
                         settings['rsnapshot_flag_dir']))
        with open(LOG, 'a') as logfile:
            logfile.write(error + "\n")
        print(error, file=sys.stderr)
        with open(LOG, 'a') as logfile:
            logfile.write("# endregion after backup\n")
        print("Finished writing \"{}\"".format(LOG), file=sys.stderr)
        return 1

    print("Finished writing \"{}\"".format(LOG), file=sys.stderr)
    return 0


def main():
    if len(sys.argv) != 2:
        print("Usage: {} <backup_type>".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    backup_type = sys.argv[1]
    rsnapshot_logged(backup_type)


if __name__ == "__main__":
    sys.exit(main())
