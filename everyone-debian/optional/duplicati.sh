#!/bin/bash

# IGNORE THIS FILE--Duplicati requires mono, even on a headless server.

customDie() {
    code=1
    echo
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    if [ ! -z $2 ]; then
        code=$2
    fi
    exit $code
}

if [ ! -d "$HOME/Downloads" ]; then
    mkdir "$HOME/Downloads" || customDie "mkdir \"$HOME/Downloads\" failed."
fi
PKGNAME=duplicati_2.0.5.1-1_all.deb
URL=https://updates.duplicati.com/beta/$PKGNAME
INSTALLER=$HOME/Downloads/$PKGNAME
wget -O $INSTALLER $URL || customDie "'wget -O $PKGNAME $URL' failed."
apt install $INSTALLER
