#!/bin/sh
# cd "$(dirname "$0")";
# CWD="$(pwd)"
# echo $CWD
python3 /opt/bin/rsnapshot_logged.py alpha 1>/var/log/linuxpreinstall.rsnapshot_logged.sh.out 2>/var/log/linuxpreinstall.rsnapshot_logged.sh.err
if [ -f /opt/etc/last_settings.rc ]; then
    . /opt/etc/last_settings.rc
    if [ -z "$snapshot_root" ]; then
        echo "Error: no snapshot_root in /opt/etc/last_settings.rc" >> /var/log/linuxpreinstall.rsnapshot_logged.sh.err
    else
        if [ -z "$backup_drive" ]; then
            echo "Error: no snapshot_root in /opt/etc/last_settings.rc" >> /var/log/linuxpreinstall.rsnapshot_logged.sh.err
        else
             echo "cp /var/log/linuxpreinstall.rsnapshot_logged.sh.err $backup_drive/var/log/"
             cp /var/log/linuxpreinstall.rsnapshot_logged.sh.err "$backup_drive/var/log/" 1>>/var/log/linuxpreinstall.rsnapshot_logged.sh.out 2>>/var/log/linuxpreinstall.rsnapshot_logged.sh.err
             echo "cp /var/log/linuxpreinstall.rsnapshot_logged.sh.out $backup_drive/var/log/"
             cp /var/log/linuxpreinstall.rsnapshot_logged.sh.out "$backup_drive/var/log/" 1>>/var/log/linuxpreinstall.rsnapshot_logged.sh.out 2>>/var/log/linuxpreinstall.rsnapshot_logged.sh.err
        fi
    fi
else
    echo "Error: missing /opt/etc/last_settings.rc" >> /var/log/linuxpreinstall.rsnapshot_logged.sh.err
fi