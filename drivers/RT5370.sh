#!/bin/bash
echo "Installing 'Cana Kit' or any other RT5370 USB Wi-Fi device..."
echo "* If it appears here:"
modinfo rt2800usb | grep 5370
echo "* It should appear here:"
lspci -vnn | grep -i net
DONT_BLOCK="blacklist rt2800usb"
echo "* If not, remove '$DONT_BLOCK' from /etc/modprobe.d/blacklist.conf since that driver is required as per <https://superuser.com/a/692255>."
BL_PATH="/etc/modprobe.d/blacklist.conf"
if [ -f $BL_PATH ]; then
    if grep -q SomeString "$BL_PATH"; then
        echo "Error: You must remove $DONT_BLOCK from $BL_PATH first."
        exit 1
    fi
fi
# For intel cards, run:
# sudo dnf install \*-firmware
# as per https://rpmfusion.org/Configuration/
sudo modprobe rt2800usb
# The ./wireless-info script is also mentioned in Broadcom_B43_Wifi-disable_since_slow.sh
cat <<END

See which device is actually connected by looking at the GENERAL.CONNECTION (followed by -- if not connected, otherwise a network name a.k.a. SSID follows) in the "NetworkManager info" section of ~/wireless-info.txt after running:
  cd ~ && wget -N -t 5 -T 10 https://github.com/UbuntuForums/wireless-info/raw/master/wireless-info && chmod +x wireless-info && ./wireless-info

END
