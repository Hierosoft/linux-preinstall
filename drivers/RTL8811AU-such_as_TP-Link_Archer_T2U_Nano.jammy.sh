#!/bin/bash
cat <<END
This installs a driver for RTL 8811AU such as TP-Link Archer T2U Nano
  but it must be compiled each time the kernel is upgraded
  (and then the device must be unplugged & re-plugged)! 

This script is based on steps from <https://docs.alfa.com.tw/Support/Linux/RTL8811AU/>.
END

source /etc/os-release

if [ "$UBUNTU_CODENAME" != "jammy" ]; then
# ^ Same for Ubuntu 22.04 or Linux Mint 21
    echo "The steps in this script are only known to work with Jammy (Ubuntu 22.04 or Linux Mint 21). See <https://docs.alfa.com.tw/Support/Linux/RTL8811AU/> for other options."
fi
sudo apt update
sudo apt install git build-essential

# STEP 3 : Download driver source

sudo mkdir -p /opt/git/aircrack-ng/

cd /opt/git/aircrack-ng/

if [ $? -ne 0 ]; then
    exit 1
fi

if [ ! -d "rtl8812au" ]; then
    git clone https://github.com/aircrack-ng/rtl8812au.git
    if [ $? -ne 0 ]; then exit; fi
    cd rtl8812au
    if [ $? -ne 0 ]; then exit; fi
else
    cd rtl8812au
    if [ $? -ne 0 ]; then exit; fi
    git pull
    if [ $? -ne 0 ]; then echo "Warning: git pull failed in \"`pwd`\"; using found version"; fi
fi

# STEP 4 : Compile and install

make
sudo make install

# STEP 5 (Optional): Check driver existance

# Run commands below:
echo "The driver should be listed below. If not, see possible alternative steps at <https://docs.alfa.com.tw/Support/Linux/RTL8811AU/>"
find /lib/modules/`uname -r`/ -name "88XXau.ko"

echo
echo "You must unplug the device and plug it in again to reload it."
echo
