#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

set -e
function cleanup()
{
    systemctl start abrtd
    systemctl start abrt-oops
}

trap cleanup EXIT

systemctl stop abrtd
systemctl stop abrt-oops
# purge dumps older than 10 days:
find /var/spool/abrt/ -type d -ctime +10 -exec abrt-cli rm {} \;
# find /var/spool/abrt/ -type d -ctime +10 -exec rm -rf {} \;
cleanup

# [install:]

#sudo crontab -e
#Add the line:
#
#*/5 * * * * bash /home/yael/purgeabrt.sh

# https://unix.stackexchange.com/questions/556307/what-is-the-right-approach-to-purge-var-spool-abrt
# answered Dec 9 '19 at 13:03
# Paulo Tomé

