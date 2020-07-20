#!/bin/bash
echo
echo
echo "INFO: Choose the Java Edition if your OS is 32-bit."
echo
sleep 5
if [ ! -f "`rpm`" ]; then
    echo "Only rpm-based distros are available currently."
    echo "For deb-based distros, use the official deb."
    echo "For Arch, use AUR."
    exit 1
fi
curl https://raw.githubusercontent.com/DarkWav/Minecraft-Installer-RPM/master/minecraft-installer.sh | bash

echo "Uninstall:"
echo "    sudo rpm -e minecraft-launcher"
