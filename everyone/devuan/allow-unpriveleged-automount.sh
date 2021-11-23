#!/bin/bash
_src_file="everyone/devuan/etc/polkit-1/localauthority/50-local.d/automount.pkla"
if [ ! -d "everyone" ]; then
    try_file="etc/polkit-1/localauthority/50-local.d/automount.pkla"
    if [ -f "$try_file" ]; then
        _src_file="$try_file"
    else
        echo "Error: $try_file wasn't found. You must run this from the linux-preinstall or the linux-preinstall/everyone/devuan directory."
        exit 1
    fi
fi
_dest_dir=/etc/polkit-1/localauthority/50-local.d/
if [ ! -d "$_dest_dir" ]; then
    echo "Error: Your configuration structure is unrecognized. "
    exit 1
fi
cp "$_src_file" "$_dest_dir/"
