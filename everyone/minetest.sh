#!/bin/sh
killall minetest
arcName=minetest-linux64.zip
url=https://downloads.minetest.org/$arcName
customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}

if [ ! -d "$HOME/Downloads" ]; then
    mkdir -p "$HOME/Downloads"
fi

enableOffline=false
for var in "$@"
do
    if [ "@$var" = "@--offline" ]; then
        enableOffline=true
    fi
done

cd "$HOME/Downloads" || customDie "Cannot cd '$HOME/Downloads'"
unzName=minetest-linux64
if [ "@$enableOffline" = "@false" ]; then
    wget -O "$arcName" $url || customDie "Cannot download $url"
    if [ -d "$unzName" ]; then
        rm -Rf $unzName
    fi
    unzip "$arcName" || customDie "Cannot extract `pwd`/$arcName"
else
    if [ ! -d "$unzName" ]; then
        if [ -f "$arcName" ]; then
            if [ -d "$unzName" ]; then
                rm -Rf $unzName
            fi
            unzip "$arcName" || customDie "Cannot extract `pwd`/$arcName"
        else
            customDie "Missing $arcName (required for offline install)"
        fi
    fi
fi
if [ ! -d "$unzName" ]; then
    customDie "Missing extracted '`pwd`/$unzName' (usually from '`pwd`/$arcName')"
fi
mytmp=/tmp/linux-preinstall/minetest
if [ ! -d "$mytmp" ]; then
    mkdir -p "$mytmp"
fi
if [ -d "$HOME/minetest/worlds" ]; then
    echo
    echo "Backing up worlds..."
    rsync -rt --delete --info=progress2 $HOME/minetest/worlds $mytmp
fi
if [ -d "$HOME/minetest/games/Bucket_Game/mods/codercore/coderskins" ]; then
    echo
    echo "Backing up skins..."
    rsync -rt --delete --info=progress2 $HOME/minetest/games/Bucket_Game/mods/codercore/coderskins $mytmp
fi
if [ ! -d "$HOME/minetest" ]; then
    mkdir "$HOME/minetest"
fi
echo
echo "Installing Final Minetest..."
exFile="$mytmp/exclude.txt"
rm "$exFile"
touch "$exFile"
if [ -f "$HOME/minetest.conf" ]; then
    echo "minetest.conf" >> "$exFile"
fi
if [ -f "$HOME/arrowkeys.txt" ]; then
    echo "arrowkeys.txt" >> "$exFile"
fi
rsync -rt --info=progress2 --exclude-from "$exFile" $unzName/ $HOME/minetest || customDie "Cannot rsync from '$unzName' to '$HOME/minetest'."
if [ -d "$mytmp/worlds" ]; then
    echo
    echo "Restoring worlds..."
    rsync -rt --info=progress2 $mytmp/worlds/ $HOME/minetest/worlds
fi
if [ -d "$mytmp/coderskins/textures" ]; then
    echo
    echo "Restoring skins..."
    rsync -rt --info=progress2 $mytmp/coderskins/textures/ $HOME/minetest/games/Bucket_Game/mods/codercore/coderskins/textures
fi
destPix="$HOME/.local/share/pixmaps"
if [ ! -d "$destPix" ]; then
    mkdir -p "$destPix"
fi
destApps="$HOME/.local/share/applications"
if [ ! -d "$destApps" ]; then
    mkdir -p "$destApps"
fi
cp $unzName/misc/minetest-xorg-icon-128.png $HOME/.local/share/pixmaps/minetest.png
srcShortcut=$unzName/misc/net.minetest.minetest.desktop
tryShortcut=$unzName/misc/org.minetest.minetest.desktop
if [ -f "$tryShortcut" ]; then
    srcShortcut="$tryShortcut"
fi
dstShortcut=$destApps/org.minetest.minetest.desktop
cat "$srcShortcut" | grep -v "Exec=" | grep -v "Name=" | grep -v "Icon=" > "$dstShortcut"
echo "Exec=$HOME/minetest/bin/minetest" >> "$dstShortcut"
echo "Name=Final Minetest" >> "$dstShortcut"
echo "Icon=$destPix/minetest.png" >> "$dstShortcut"
