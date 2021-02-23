#!/bin/sh
# sudo sh -c "echo 'deb http://download.opensuse.org/repositories/isv:/ownCloud:/desktop/xUbuntu_14.04/ /' >> /etc/apt/sources.list.d/owncloud-client.list"

source $HOME/.config/linux-preinstall/globals.rc
if [ $? -ne 0 ]; then
    echo "ERROR: 'source $HOME/.config/linux-preinstall/globals.rc' failed."
    echo "You must run linux-preinstall/setup.sh first."
    exit 1
fi
source $LINUX_PREINSTALL/api.rc
if [ $? -ne 0 ]; then
    echo "ERROR: 'source $LINUX_PREINSTALL/api.rc' failed."
    echo "You must run linux-preinstall/setup.sh first."
    exit 1
fi

$INSTALL_CMD keepassx
$INSTALL_CMD nextcloud-client
$INSTALL_CMD mdb-tools
$INSTALL_CMD mdbtools
$INSTALL_CMD mdbtools-gmdb
$INSTALL_CMD libreoffice
#an is a terminal anagram generator (usage: an -w hello)
