#!/bin/sh
if [ -d ~/.kde/share/apps/kscreen ]; then
    rm -Rf ~/.kde/share/apps/kscreen
fi
if [ -d ~/.local/share/kscreen ]; then
    rm -Rf ~/.local/share/kscreen
fi
echo "Now reboot or run: sudo systemctl restart sddm"
echo "or restart whatever dm you use such as gdm."
