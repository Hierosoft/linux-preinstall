#!/bin/bash

# See <https://wiki.debian.org/WiFi>:
sudo apt-get install -y firmware-ralink

# modinfo rt2800usb | grep 5370
# ^ command not found on Devuan 4 (chimaera) (based on Debian 11 (bullseye))

sudo modprobe rt2800usb

# See <https://bbs.archlinux.org/viewtopic.php?id=173808>:
sudo rfkill list all
# ^ such as:
#0: hci0: Bluetooth
#	Soft blocked: yes
#	Hard blocked: no
#3: phy2: Wireless LAN
#	Soft blocked: yes
#	Hard blocked: no
#
sudo rfkill unblock 2

cat > /etc/network/interfaces.d/CanaKit.conf <<END
auto wlx1cbfce1abfb9
iface wlx1cbfce1abfb9 inet dhcp
END

sudo service networking restart
