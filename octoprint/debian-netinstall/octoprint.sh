#!/bin/bash
customExit() {
    >&2 echo
    >&2 echo
    >&2 echo "ERROR:"
    >&2 echo "$1"
    >&2 echo
    >&2 echo
    exit 1
}
HOW="from unknown config"
if [ -z "$SUDOER" ]; then
    if [ -z "$1" ]; then
        customExit "You must specify a user to become sudoer as the parameter."
    fi
    HOW="by first parameter"
    SUDOER="$1"
else
    # privileges
    HOW="as SUDOER"
fi
if [ ! -d "/home/$SUDOER" ]; then
    echo "User $SUDOER specified $HOW does not have a home directory. You must specify a real user."
fi
apt update
apt install -y sudo
#see https://devconnected.com/how-to-add-a-user-to-sudoers-on-debian-10-buster/
/usr/sbin/usermod -a -G sudo $SUDOER
echo "* If $SUDOER was logged in, they must log out then back in again to get sudo group priveleges."
echo "* Now you must run ../debian/octoprint.sh as root."
