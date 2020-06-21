#!/bin/bash
# systemctl stop packagekit
# systemctl disable packagekit
# systemctl mask packagekit
# systemctl stop packagekit-offline-update
# systemctl disable packagekit-offline-update
# systemctl mask packagekit-offline-update
# ^ don't disable packagekit. Also don't remove it, as the following depend on it:
#  gnome-software inkscape kde-print-manager plasma-applet-redshift-control plasma-breeze plasma-discover plasma-pk-updates sddm-breeze simple-scan
dnf remove -y plasma-pk-updates
