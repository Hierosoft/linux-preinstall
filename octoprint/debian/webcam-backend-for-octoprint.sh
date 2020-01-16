#!/bin/bash
customDie() {
    echo
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
source include/octoprint.rc || customDie "'source include/octoprint.rc' failed in '`pwd`' as $USER"

echo "The scripts named webcam-backend* are only necessary for using a webcam (but not necessary for webcams that already provide an mjpeg stream that OctoPrint can see)"

# See https://community.octoprint.org/t/setting-up-octoprint-on-a-raspberry-pi-running-raspbian/2337

apt update
echo
echo "WARNING: This would add about 509MB on Debian 10. To continue, type:"
# NOTE: subversion package DOES install git
echo "  apt install -y subversion libjpeg62-turbo-dev imagemagick ffmpeg libv4l-dev cmake"
echo "  # if you still can't type the 'git' command successfully after that, try:"
echo "  apt install -y git"
echo
usermod -a -G video $UNPRIV_USER
