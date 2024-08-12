#!/bin/sh
# cd "$(dirname "$0")";
# CWD="$(pwd)"
# echo $CWD
python3 /opt/bin/before_rsnapshot.py $1 1>/var/log/linuxpreinstall.before_rsnapshot.sh.out 2>/var/log/linuxpreinstall.before_rsnapshot.sh.err
