#!/bin/sh
sudo apt-get purge bcmwl-kernel-source broadcom-sta-common broadcom-sta-source

sudo apt-get install b43-fwcutter firmware-b43-installer
code=$?
OUTFILE="$HOME/Desktop/PostInstallInstructions.md"

printf "* Broadcom b43-fwcutter and b43-fwcutter firmware-b43-installer were installed (and bcmwl-kernel-source broadcom-sta-common broadcom-sta-source were removed) by linux-preinstall" | tee -a "$OUTFILE"
if [ $code -ne 0 ]; then
    echo "  (FAILED), but usually:" | tee -a "$OUTFILE"
else
    echo "  (successfully):" | tee -a "$OUTFILE"
fi
echo "  After restart, the wifi sources should appear in nm-applet (up&down arrow icon in task tray)" | tee -a "$OUTFILE"
