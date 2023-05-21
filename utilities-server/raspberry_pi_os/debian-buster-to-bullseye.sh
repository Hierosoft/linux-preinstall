#!/bin/bash
me=$0
# https://linuxize.com/post/how-to-upgrade-debian-10-to-debian-11/
SOURCES_LIST_SRC=/home/owner/git/linux-preinstall/utilities-server/raspberry_pi_os/sources.list-debian-bullseye_from_buster-raspberry_pi_os
SOURCES_LIST_DST=/etc/apt/sources.list
SOURCES_LIST_BAK=/etc/apt/sources.list.buster
if [ ! -f "$SOURCES_LIST_BAK" ]; then
    >&2 echo "[$me] [$me] Error: '$SOURCES_LIST_BAK' already exists. Did you run this script already? Only run the script once, to ensure a backup and the state is correct. If you are sure you are running buster, delete the file and run this script again."
    exit 1
fi
if [ ! -f "$SOURCES_LIST_DST" ]; then
    >&2 echo "[$me] [$me] Error: There is no '$SOURCES_LIST_DST'. This can only run on Debian buster."
    exit 1
fi
if [ ! -f "$SOURCES_LIST_SRC" ]; then
    >&2 echo "[$me] [$me] Error: There is no '$SOURCES_LIST_SRC'. This script can only run in the linux-preinstall repo subdirectory containing the bullseye sources list file."
    exit 1
fi

if [ ! -f "/etc/os-release" ]; then
    >&2 echo "[$me] [$me] Error: There is no '/etc/os-release'. This can only run on Debian buster."
    exit 1
fi
if [ ! -z "$VERSION_CODENAME" ]; then
    >&2 echo "[$me] [$me] Error: VERSION_CODENAME is already set. Please start with a clean environment so that /etc/os-release can be checked."
fi
source /etc/os-release
if [ $? -ne 0 ]; then exit 1; fi
if [ "$VERSION_CODENAME" != "buster" ]; then
    >&2 echo "[$me] [$me] Error: VERSION_CODENAME=$VERSION_CODENAME but this script is only for buster."
    exit 1
fi

sudo apt update
sudo apt upgrade -y
sudo apt full-upgrade -y
sudo apt autoremove -y

if grep -Fxq "buster" "$SOURCES_LIST_DST"
    >&2 echo "[$me] Checking $SOURCES_LIST_DST...OK $SOURCES_LIST_DST is buster as expected."
else
    >&2 echo "[$me] Checking $SOURCES_LIST_DST...Error: buster is not in '$SOURCES_LIST_DST'."
    exit 1
fi

if grep -Fxq "bullseye" "$SOURCES_LIST_DST"
    >&2 echo "[$me] Error: bullseye is already in '$SOURCES_LIST_DST'."
    exit 1
else
    >&2 echo "[$me] Done checking $SOURCES_LIST_DST."
fi

sudo cp "$SOURCES_LIST_DST" "$SOURCES_LIST_BAK"
if [ $? -ne 0 ]; then exit 1; fi

sudo cp "$SOURCES_LIST_SRC" "$SOURCES_LIST_DST"
if [ $? -ne 0 ]; then exit 1; fi

export LC_ALL=C

sudo apt update
sudo apt upgrade -y
sudo apt full-upgrade -y
sudo apt autoremove -y
sudo apt dist-upgrade -y
sudo apt autoremove -y

source /etc/os-release
if [ $? -ne 0 ]; then exit 1; fi
if [ "$VERSION_CODENAME" != "bullseye" ]; then
    >&2 echo "[$me] [$me] Error: VERSION_CODENAME=$VERSION_CODENAME but should be bullseye by now. This script failed."
    exit 1
fi

printf "swappiness="
cat /proc/sys/vm/swappiness
# ^ usually 60
# "turn that down to 10 or 15. The swap file will then only be used when my RAM usage is around 80 or 90 percent"
echo "vm.swappiness = 10" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
sudo sysctl vm.swappiness=10
# ^ also ensure it is applied immediately
# "when 10 %...of ram is left then it will start using swap"
# -<https://askubuntu.com/a/103916>

>&2 echo "[$me] Done!"
>&2 echo "[$me] After reboot, run the following command to see if the upgrade worked (The output should say \"Debian GNU/Linux 11 (bullseye)\" in the Description line):"
>&2 echo "[$me]     lsb_release -a"
>&2 echo "[$me] Rebooting..."
sleep 1
>&2 echo "[$me] 4..."
sleep 1
>&2 echo "[$me] 3..."
sleep 1
>&2 echo "[$me] 2..."
sleep 1
>&2 echo "[$me] 1..."
sleep 1
sudo systemctl reboot
