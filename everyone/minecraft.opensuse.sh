#!/bin/bash
if [ -f "`command -v apt-get`" ]; then
    echo "Use the deb from Mojang instead."
    exit 1
fi
if [ -f "`command -v pacman`" ]; then
    echo "Use the AUR version instead."
    exit 1
fi

sudo zypper in rpm-build wget bsdtar bash gconf2

