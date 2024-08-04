#!/usr/bin/env python3
"""
Install using a Terminal:
1. Make sure you are in the linux-preinstall/utilities folder then:
    ls before_snapshot.py && sudo mkdir -p /opt/bin && sudo ln -s before_snapshot.py /opt/bin/before_snapshot.ty
2. Add the following to rsnapshot.conf (comment any existing cmd_preexec line first then):
    cmd_preexec	/opt/bin/before_rsnapshot.py
    # (rsnapshot requires a tab character between the setting name and value)
"""
# formerly before-backup.sh
import os
import subprocess
import time
import sys


if __name__ == "__main__":
    SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
    REPO_DIR = os.path.dirname(SCRIPTS_DIR)
    sys.path.insert(0, REPO_DIR)

from generate_exclude import main as generate_exclude_main

from linuxpreinstall.more_rsnapshot import (
    LOG,
    settings,
    IS_ROOT_MODE,
)

from linuxpreinstall.sysdirs import (
    sysdirs,
)


def run_command(command, log=None):
    """Run a command and optionally log the output. Returns the
    returncode of the process."""
    try:
        output = subprocess.check_output(command, shell=True,
                                         stderr=subprocess.STDOUT)
        if log:
            with open(log, 'a') as logfile:
                logfile.write(output.decode())
        return 0  # Success
    except subprocess.CalledProcessError as e:
        if log:
            with open(log, 'a') as logfile:
                logfile.write("Error: {}\n".format(e.output.decode()))
        return e.returncode  # Return the error code


def main():
    # Write date to log
    with open(LOG, 'w') as logfile:
        logfile.write(time.strftime('%Y-%m-%d %H:%M:%S\n'))

    # Log /etc/default/cron
    with open(LOG, 'a') as logfile:
        logfile.write("* /etc/default/cron:\n")
        with open('/etc/default/cron', 'r') as cron_file:
            cron_content = cron_file.read()
            for line in cron_content.splitlines():
                if 'EXTRA_OPTS' in line:
                    logfile.write(line + '\n')

    # Log syslog configuration
    with open(LOG, 'a') as logfile:
        logfile.write("* {}:\n".format(sysdirs['SYSLOG_CONF']))
        with open(sysdirs['SYSLOG_CONF'], 'r') as syslog_file:
            for line in syslog_file:
                if 'cron.*' in line:
                    logfile.write(line)

    # Check and manage mount point
    subs = []
    if IS_ROOT_MODE and os.path.isdir(sysdirs['PROFILES']):
        subs = list(os.listdir(sysdirs['PROFILES']))
    for sub in subs:
        # Unmount fuse mounts of the backup drive that do not match the
        #   destination mountpoint.
        if "{}" in settings['backup_unused_fuse_mountpoint_fmt']:
            backup_unused_fuse_mountpoint = \
                settings['backup_unused_fuse_mountpoint_fmt'].format(sub)
        else:
            backup_unused_fuse_mountpoint = \
                settings['backup_unused_fuse_mountpoint_fmt']
        if backup_unused_fuse_mountpoint == settings['backup_drive']:
            # The fuse mountpoint is the backup drive, so don't unmount it.
            continue
        if os.path.isdir(os.path.join(backup_unused_fuse_mountpoint,
                                      settings['rsnapshot_flag_dir'])):
            result = run_command('umount {}'
                                 .format(backup_unused_fuse_mountpoint),
                                 log=LOG)
            if result == 0:
                with open(LOG, 'a') as logfile:
                    logfile.write("OK\n")
            else:
                with open(LOG, 'a') as logfile:
                    logfile.write(
                        "FAILED (umount {})\n"
                        .format(backup_unused_fuse_mountpoint))
            time.sleep(1)

    if subs:
        time.sleep(1)  # This seems to be necessary for drive to be available
    if not os.path.isdir(settings['snapshot_root']):
        result = run_command('mount {}'.format(settings['backup_drive']),
                             log=LOG)
        if result != 0:
            with open(LOG, 'a') as logfile:
                logfile.write("[before-backup.sh] Error: mount {} failed.\n"
                              .format(settings['backup_drive']))
            return result

    # Verify rsnapshot directory
    if not os.path.isdir(settings['snapshot_root']):
        print("[before-backup.sh] Error: {} is missing."
              .format(settings['snapshot_root']),
              file=sys.stderr)
        return 1

    # Run generate_exclude.py scripts
    # sys.argv = ['generate_exclude.py', '--user']
    # generate_exclude_main()
    usr_cmd = 'sudo -u owner python3 /opt/bin/generate_exclude.py --user'
    code = run_command(usr_cmd, log=LOG)
    if code != 0:
        print("Failed with code {}: {}".format(code, usr_cmd))
        print("See \"{}\"".format(LOG))
        return code
    print("OK: {}".format(usr_cmd))

    # run_command('sudo python3 /opt/bin/generate_exclude.py', log=LOG)
    sys.argv = ['generate_exclude.py']
    generate_exclude_main()
    print("OK: generate_exclude_main")

    return 0


if __name__ == "__main__":
    sys.exit(main())
