#!/bin/bash
src_dt_name=clean-lbry.desktop
src_dt=./utilities/dist/share/applications/$src_dt_name
if [ ! -d "$src_dt" ]; then
    echo "* \"$src_dt\" is missing. Run this from the linux-preinstall directory."
    exit 1
fi
dst_applications="$HOME/.local/share/applications"
if [ ! -d "$dst_applications" ]; then
    mkdir -p "$dst_applications"
fi
dst_dt="$dst_applications/$src_dt_name"
cp "$src_dt" "$dst_dt"
xdg-desktop-icon install --novendor "$dst_dt"
# xdg-desktop-icon uninstall "$dst_dt"
