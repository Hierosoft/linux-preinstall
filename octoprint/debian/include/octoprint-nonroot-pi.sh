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
source octoprint.rc || source include/octoprint.rc || source /tmp/linux_preinstall_octoprint/include/octoprint.rc || customDie "octoprint.rc must be in the same directory from which you run $0."
if [ "$USER" != "$UNPRIV_USER" ]; then
    customDie "You must be pi to run this script. See octoprint.sh."
fi
#SUDOER="$USER"
# See https://community.octoprint.org/t/setting-up-octoprint-on-a-raspberry-pi-running-raspbian/2337
cd ~
if [ ! -d "OctoPrint" ]; then
    mkdir OctoPrint || customDie "'mkdir OctoPrint' failed in `pwd` as $USER"
fi
cd OctoPrint || customDie "'cd OctoPrint' failed in `pwd`."
virtualenv venv || customDie "'virtualenv venv' failed in `pwd` as $USER"
source venv/bin/activate || customDie "'source venv/bin/activate' failed in `pwd`"
pip install pip --upgrade || customDie "'pip install pip --upgrade' failed in `pwd` as $USER"
pip install octoprint || customDie "'pip install octoprint --upgrade' failed in `pwd` as $USER"
deactivate

