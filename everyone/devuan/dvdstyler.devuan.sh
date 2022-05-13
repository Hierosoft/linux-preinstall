#!/bin/bash

myPath="`realpath "$0"`"
myDir="`dirname "$myPath"`"
. devuanCodenames.rc
if [ $? -ne 0 ]; then
    . "$myDir/devuanCodenames.rc"
    if [ $? -ne 0 ]; then
        exit 1
    fi
fi

if [ "@$debianV" = "@" ]; then
    usage
    echo "Error: There was no debian version known by the script $0 to match VERSION_CODENAME=$VERSION_CODENAME."
    exit 1
fi

oldLine="`cat /etc/apt/sources.list | grep deb-multimedia`"

if [ "@$oldLine" != "@" ]; then
    echo "INFO: Skipping add deb-multimedia for $debianV since the following line is already in /etc/apt/sources.list:"
    echo "  $oldLine"
    exit 1
else
    echo "deb http://www.deb-multimedia.org bullseye main" >> /etc/apt/sources.list
    apt update
fi

apt install -y dvdstyler



