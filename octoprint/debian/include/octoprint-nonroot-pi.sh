#!/bin/bash
echo "Instead, use the install script from <https://github.com/paukstelis/octoprint_install>."
echo "See octoprint.sh output for other notes."
exit 1

customExit() {
    echo
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
source octoprint.rc || source include/octoprint.rc || source /tmp/linux_preinstall_octoprint/include/octoprint.rc || customExit "octoprint.rc must be in the same directory from which you run $0."
if [ "$USER" != "$UNPRIV_USER" ]; then
    customExit "You must be pi to run this script. See octoprint.sh."
fi
#SUDOER="$USER"
# See https://community.octoprint.org/t/setting-up-octoprint-on-a-raspberry-pi-running-raspbian/2337
cd ~
if [ ! -d "OctoPrint" ]; then
    mkdir OctoPrint || customExit "'mkdir OctoPrint' failed in `pwd` as $USER"
fi
cd OctoPrint || customExit "'cd OctoPrint' failed in `pwd`."
virtualenv venv || customExit "'virtualenv venv' failed in `pwd` as $USER"
# source venv/bin/activate || customExit "'source venv/bin/activate' failed in `pwd`"
venv/bin/pip install pip --upgrade || customExit "'pip install pip --upgrade' failed in `pwd` as $USER"
venv/bin/pip install octoprint || customExit "'pip install octoprint --upgrade' failed in `pwd` as $USER"
# deactivate

