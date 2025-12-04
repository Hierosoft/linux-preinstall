#!/bin/bash

source /etc/os-release

old_naming = "false"

if [ -f "`command -v bc`" ]; then
    if [ "$(echo "$VERSION_ID < 22.11" | bc -l)" -eq 1 ]; then
        old_naming = "true"
    fi
elif [ "$VERSION_CODENAME" = "jammy" ]; then
    old_naming = "true"
fi

# ^ requires bc
if [ "$old_naming" = "true" ]; then
    sudo apt install -y libwxgtk3.0-gtk3-dev libwxgtk-media3.0-gtk3-dev libboost-dev cmake make git || exit $?
else
    sudo apt install -y libwxgtk3.2-dev libwxgtk-media3.2-dev libboost-dev cmake make git || exit $?
fi

mkdir -p ~/Downloads/git/wxFormBuilder || exit $?
cd ~/Downloads/git/wxFormBuilder || exit $?
if [ ! -d wxFormBuilder ]; then
    git clone --recursive https://github.com/wxFormBuilder/wxFormBuilder.git || exit $?
    cd wxFormBuilder || exit $?
else
    cd wxFormBuilder || exit $?
    git pull || exit $?
fi
cmake -S . -B _build -G "Unix Makefiles" --install-prefix "$PWD/_install" -DCMAKE_BUILD_TYPE=Release

# On Ubuntu 22.04 jammy, it still fails:
# CMake Error at /usr/share/cmake-3.22/Modules/FindPackageHandleStandardArgs.cmake:230 (message):
#   Could NOT find wxWidgets: Found unsuitable version "3.0.5", but required is
#   at least "3.2"
if [ $? -ne 0 ]; then
    cd ..
    wget https://github.com/wxFormBuilder/wxFormBuilder/releases/download/v4.2.1/wxFormBuilder-4.2.1-x86_64.flatpak
    sudo flatpak install -y wxFormBuilder-4.2.1-x86_64.flatpak
fi
