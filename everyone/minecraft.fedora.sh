#!/bin/bash
if [ -f "`command -v apt-get`" ]; then
    echo "Use the deb from Mojang instead."
    exit 1
fi
if [ -f "`command -v pacman`" ]; then
    echo "Use the AUR version instead."
    exit 1
fi

dnf in rpm-build wget bsdtar bash

echo "Not Implemented Error: Installing Minecraft on Fedora."
