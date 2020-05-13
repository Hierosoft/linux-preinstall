#!/bin/sh

# Misfit Model 3D was discontinued in 2009.
# zturtleman's Maverick Model 3D is a modernize fork.

customExit() {
    errorCode=1
    if [ ! -z "$2" ]; then
        errorCode="$2"
    fi
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit $errorCode
}
cd ~
if [ ! -d ~/Downloads/git/zturtleman ]; then
    mkdir -p ~/Downloads/git/zturtleman
fi
cd ~/Downloads/git/zturtleman
git clone https://github.com/zturtleman/mm3d.git
cd mm3d

./autosetup.sh
# above yields several: `warning: '%'-style pattern rules are a GNU make extension`

./configure && make && sudo make install
echo "Configure may fail to find QT_VERSION_MINOR."
echo "I have reported this issue: https://github.com/zturtleman/mm3d/issues/44"
