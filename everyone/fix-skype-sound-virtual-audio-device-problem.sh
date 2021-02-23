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
#all of the commented commands were tried before solving

#sudo apt-get install --reinstall linux-image-$(uname -r)
#sudo apt-get install libpulse0:i386
##result: was already installed

#purge-old-kernels
#sudo apt-get upgrade
#sudo reboot
#purge-old-kernels

#to get pactl to test pulseaudio:
#sudo apt-get install pulseaudio-utils
##also it installed libpulsedsp
#pactl list
##result of pactl list was ". . . Connection Refused . . ."

#pgrep -l pulseaudio
##result: none (indicating that pulseaudio was not running)

##tried running pulseaudio manually:
#pulseaudio
##result: pulseaudio is not installed

$INSTALL_CMD pulseaudio
