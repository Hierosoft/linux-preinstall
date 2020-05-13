#!/bin/sh

# git pull

# - Install to $HOME/minetest.
# - Backs up skins and worlds before upgrade, then restore afterward.
# - Put icon and shortcut in correct directories in $HOME/.local
#   (as per XDG standard).
MT_BASH_SCRIPT_NAME="update-minetest-linux64.sh"
MT_BASH_SCRIPT_PATH="/tmp/$MT_BASH_SCRIPT_NAME"
curl https://raw.githubusercontent.com/poikilos/EnlivenMinetest/master/$MT_BASH_SCRIPT_NAME -o $MT_BASH_SCRIPT_PATH
bash $MT_BASH_SCRIPT_PATH
exit $?

killall minetest
arcName=minetest-linux64.zip
RELEASE_ARC_URL=https://downloads.minetest.org/$arcName
installPath="`pwd`"
customExit() {
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
cd "$HOME/Downloads" || customExit "Cannot cd '$HOME/Downloads'"
unzName=minetest-linux64
if [ -f "$arcName" ]; then
    if [ `stat --format=%Y $arcName` -gt $(( `date +%s` - (24*60*60) )) ]; then
        # File is newer than 24 hours.
        echo
        echo "* Existing '$arcName' is recent (no download is required)."
        echo
        enableOffline=true
    fi
fi
if [ "@$enableOffline" = "@false" ]; then
    wget -O "$arcName" $RELEASE_ARC_URL || customExit "Cannot download $RELEASE_ARC_URL"
    if [ -d "$unzName" ]; then
        rm -Rf $unzName
    fi
    unzip "$arcName" || customExit "Cannot extract `pwd`/$arcName"
else
    if [ ! -d "$unzName" ]; then
        if [ -f "$arcName" ]; then
            if [ -d "$unzName" ]; then
                rm -Rf $unzName
            fi
            unzip "$arcName" || customExit "Cannot extract `pwd`/$arcName"
        else
            customExit "Missing $arcName (required for offline install)"
        fi
    fi
fi
if [ ! -d "$unzName" ]; then
    customExit "Missing extracted '`pwd`/$unzName' (usually from '`pwd`/$arcName')"
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
rsync -rt --info=progress2 --exclude-from "$exFile" $unzName/ $HOME/minetest || customExit "Cannot rsync from '$unzName' to '$HOME/minetest'."
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

updaterName=org.minetest.mtupdate.desktop
updaterSrc="share/applications/$updaterName"
updaterDst="$HOME/.local/share/applications/$updaterName"

if [ -f "$installPath/$updaterSrc" ]; then
    cat "$installPath/$updaterSrc" | grep -v Exec= | grep -v Icon= > $updaterDst
    echo "Exec=$HOME/git/linux-preinstall/everyone/minetest-nonroot.sh" >> $updaterDst
    echo "Icon=$HOME/.local/share/pixmaps/minetest.png" >> $updaterDst
else
    echo "'$updaterSrc' is missing."
fi
echo
echo
echo "Update is complete."
echo
sleep 4
