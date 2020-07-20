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
# ^ even after that, packagekitd sometimes takes >10GB RAM after some time. See
#   [Bug 1354074 - Possible big memory leak in
#   packagekit](https://bugzilla.redhat.com/show_bug.cgi?id=1354074).
echo "ShutdownTimeout=300" | sudo tee -a /etc/PackageKit/PackageKit.conf
# -a: append
systemctl restart packagekit

# Not tried yet:
# dnf remove -y PackageKit
# <https://www.thegeekdiary.com/centos-rhel-7-how-to-enable-or-disable-automatic-updates-via-packagekit/>:
# systemctl stop packagekit
# systemctl disable packagekit
# systemctl mask packagekit
# ^ links /etc/systemd/system/packagekit.service to /dev/null
# dnf remove -y PackageKit*

# https://forums.fedoraforum.org/showthread.php?273225-disabling-packagekit
# killall packagekitd
# rm -rf /usr/libexec/packagekitd
# ^ upgrade undoes it
