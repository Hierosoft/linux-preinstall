#!/bin/bash
. /etc/os-release
if [ "$NAME" != "Fedora" ]; then
    echo "Error: NAME=Fedora was expected in /etc/os-release but NAME is $NAME. This script is only for Fedora."
    exit 1
fi
me=`basename $0`
NEXT_VER=$(($VERSION_ID+1))
cat <<END
[$me] This script does:
dnf upgrade --refresh -y && dnf install dnf-plugin-system-upgrade -y && dnf system-upgrade download -y --releasever=$1
# dnf system-upgrade reboot
END
if [ -z "$1" ]; then
    echo "[$me] You must specify a version."
    if [ ! -z "$VERSION_ID" ]; then
        echo "[$me] You have $VERSION_ID so you should specify $NEXT_VER."
    else
        echo "[$me] Also, $VERSION_ID was expected in /etc/os-release but the variable wasn't present."
    fi
    exit 1
fi

dnf upgrade --refresh -y && dnf install dnf-plugin-system-upgrade -y && dnf system-upgrade download -y --releasever=$1

echo <<END
[$me] The following manual steps are necessary if everything worked so far:

dnf system-upgrade reboot

END
