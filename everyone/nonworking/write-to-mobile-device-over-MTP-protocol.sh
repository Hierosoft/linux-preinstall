#!/bin/sh

# NONWORKING
# * use an SD card instead

# Allow write to device over MTP
#such as phone connected via USB
mkdir -p ~/.kde/share/apps/solid/actions
cp /usr/share/kde4/apps/solid/actions/solid_mtp.desktop ~/.kde/share/apps/solid/actions/
nano ~/.kde/share/apps/solid/actions/solid_mtp.desktop
# change Exec=kioclient exec mtp:udi=%i/
# to
# Exec=dolphin "mtp:/"
# as per https://forum.kde.org/viewtopic.php?f=22&t=120685
# which references http://forums.opensuse.org/showthread.php/490795-kde-mtp-device-file-transfer-fix
