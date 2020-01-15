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
source octoprint.rc || customDie "octoprint.rc must be in the same directory from which you run $0."
if [ "$USER" != "$UNPRIV_USER" ]; then
    customDie "You must be pi to run this script. See octoprint.sh."
fi
#SUDOER="$USER"
# See https://community.octoprint.org/t/setting-up-octoprint-on-a-raspberry-pi-running-raspbian/2337
cd ~
if [ ! -d "OctoPrint" ]; then
    mkdir OctoPrint
fi
cd OctoPrint || customDie "'cd OctoPrint' failed in `pwd`."
virtualenv venv
source venv/bin/activate
pip install pip --upgrade
pip install octoprint
deactivate

