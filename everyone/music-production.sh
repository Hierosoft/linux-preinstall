#!/bin/sh
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
$INSTALL_CMD lmms audacity lame ffmpeg
