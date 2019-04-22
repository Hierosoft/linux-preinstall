#!/bin/sh
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

sudo apt-get install pulseaudio
