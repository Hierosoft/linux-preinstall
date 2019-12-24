#!/bin/bash

customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}

installPath=`pwd`
release_version=2.80
dlName=blender-$release_version-linux-glibc217-x86_64.tar.bz2
exName=blender-$release_version-linux-glibc217-x86_64
url=https://mirror.clarkson.edu/blender/release/Blender$release_version/$dlName
blenders=$HOME/Downloads/blendernightly/versions

if [ ! -d "$HOME/Downloads" ]; then
    mkdir "$HOME/Downloads" || customDie "Cannot mkdir '$HOME/Downloads'"
fi


if [ ! -f "$HOME/Downloads/$dlName" ]; then
    wget -O "$HOME/Downloads/$dlName" $url || customDie "Cannot download '$url'"
else
    echo "Using existing $HOME/Downloads/$dlName..."
fi

cd "$HOME/Downloads" || customDie "Cannot cd '$HOME/Downloads'"

if [ ! -d "$blenders" ]; then
    mkdir -p "$blenders"
fi
if [ -d "$exName" ]; then
    echo "Removing old '`pwd`/$exName'..."
    rm -Rf "$exName"
fi
echo "Extracting..."
tar xf $dlName || customDie "Cannot extract '`pwd`/$dlName'. If you delete it then run this script again, this script will download $url automatically."
if [ ! -f "`command -v rsync`" ]; then
    customDie "This script requires rsync."
fi
if [ ! -d "$exName" ]; then
    customDie "Extracting $dlName did not result in `pwd`/$exName."
fi
rsync -rt "$exName" "$blenders"

if [ -z "$PREFIX" ]; then
    PREFIX=$HOME/.local
fi
if [ -z "$SHARE" ]; then
    SHARE=$PREFIX/share
fi
applications_path=$SHARE/applications
iconName=org.blender.blender-current.desktop
standard_icon_path=$applications_path/$iconName

installed_bin="$blenders/$exName/blender"
if [ ! -f "$installed_bin" ]; then
    customDie "rsync did not result in $installed_bin"
fi
srcShortcut="$installPath/share/applications/org.blender.blender-current.desktop"
if [ ! -f "$srcShortcut" ]; then
    echo "The shortcut is missing: '`pwd`/$srcShortcut'."
fi
if [ ! -d "$applications_path" ]; then
    mkdir -p "$applications_path"
fi
tmpSC=/tmp/$iconName
cat "$srcShortcut" | grep -v Name= | grep -v Exec= > $tmpSC
echo "Name=Blender $release_version (Current)" >> $tmpSC
echo "Exec=$installed_bin" >> $tmpSC
mv -f $tmpSC "$applications_path/"
if [ ! -f "$applications_path/$iconName" ]; then
    customDie "Generating shortcut failed: '$applications_path/$iconName'"
else
    echo "Added shortcut: '$applications_path/$iconName'"
fi
