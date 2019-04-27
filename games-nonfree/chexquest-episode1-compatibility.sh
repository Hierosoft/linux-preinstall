#!/bin/bash

customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
if [ ! -f "`command -v chocolate-doom`" ]; then
    customDie "This script requires the chocolate-doom package."
fi

if [ ! -d $HOME/.local/share/applications ]; then
    mkdir -p $HOME/.local/share/applications || customDie "Cannot mkdir $HOME/.local/share/applications"
fi
src_icon_name=org.chocolate-doom.chexquest.desktop
src_icon=share/applications/$src_icon_name
dst_dir="$HOME/.local/share/Chex"
dst_wad=$dst_dir/chex.wad
patch_archive_name=chexdeh.zip
patch_name=chex.deh
dst_patch=$dst_dir/$patch_name
if [ ! -d "$dst_dir" ]; then
    customDie "You must have a legal copy of $dst_dir containing chex.wad and other files (this script can only get the original working so far)"
fi
if [ ! -f "$dst_wad" ]; then
    customDie "You must have a legal copy of $dst_dir containing chex.wad and other files (this script can only get the original working so far)"
fi
patch_url=ftp://ftp.fu-berlin.de/pc/games/idgames/utils/exe_edit/patches/chexdeh.zip
if [ ! -f "$dst_patch" ]; then
    if [ ! -d "$HOME/Downloads" ]; then
        mkdir "$HOME/Downloads" || customDie "cannot mkdir $HOME/Downloads"
    fi
    pushd "$HOME/Downloads" || customDie "cannot cd $HOME/Downloads"
    if [ ! -f "`command -v wget`" ]; then
        customDie "Using this script to get $patch_url automatically requires the wget package."
    fi
    if [ ! -f $patch_archive_name ]; then
        wget -O $patch_archive_name $patch_url || customDie "Cannot download $patch_archive_name--try downloading it yourself to `pwd` and try running this script again."
    fi
    try_msg="Try putting $patch_name in $dst_dir yourself and try running this script again."
    unzip -u $patch_archive_name || customDie "Unzipping `pwd`/$patch_archive_name failed. $try_msg"
    if [ ! -f "$patch_name" ]; then
        customDie "Unzipping $patch_archive_name did not result in a `pwd`/$patch_name file. $try_msg"
    fi
    cp "$patch_name" "$dst_dir/"
    popd
fi
if [ ! -f "$dst_patch" ]; then
    customDie "Missing $dst_patch: You must download $patch_archive_name, unzip it, and place $patch_name in $dst_dir ($patch_url didn't work)"
fi
if [ ! -f "$src_icon" ]; then
    customDie "Missing $src_icon in `pwd`"
fi
cat "$src_icon" | grep -v "Exec=" > "$HOME/.local/share/applications/$src_icon_name"
echo "Exec=chocolate-doom -iwad $dst_dir/chex.wad" >> "$HOME/.local/share/applications/$src_icon_name"
echo "* Successfully installed 'Chex Quest' icon (using Chocolate Doom icon) to the application menu."
echo "* If the icon doesn't work, try:"
echo "  - Install the timidity++ package."
echo "  - In Terminal, run 'chocolate-doom-setup'."
echo "    - Change MIDI to 'Native' and choose the timidity config file /etc/timidity.cfg, press Esc, Esc then Enter to confirm save (Don't try to change keyboard settings--they are glitched on Chocolate Doom 2.3.0)"
