#!/bin/bash

me=`basename $0`

customDie() {
    echo
    echo "ERROR:"
    echo " $1"
    echo
    echo
    ret=1
    if [ ! -z $2 ]; then ret=$2; fi
    exit $ret
}

if [ ! -f "`command -v blender`" ]; then
    customDie "You must install Blender first--this script creates a special icon that uses the filmic repo directory for colormanagement"
fi

# region environment checks

if [ -z "$REFRESH_WM" ]; then
    REFRESH_WM=true
    echo "REFRESH_WM not set, so using: '$REFRESH_WM'"
elif [ "@$REFRESH_WM" = "@TRUE" ]; then
    REFRESH_WM=true
elif [ "@$REFRESH_WM" = "@1" ]; then
    REFRESH_WM=true
elif [ "@$REFRESH_WM" = "@yes" ]; then
    REFRESH_WM=true
elif [ "@$REFRESH_WM" = "@on" ]; then
    REFRESH_WM=true
fi
if [ -z "$PREFIX" ]; then
    if [[ $EUID = 0 ]]; then
        PREFIX=/usr/local
        echo "PREFIX not set, so using '$PREFIX'"
    else
        PREFIX=$HOME/.local
        echo "PREFIX not set, and you're not root, so using '$PREFIX'"
    fi
else
    echo "Installing to specified PREFIX '$PREFIX'..."
fi

if [ ! -d "$PREFIX" ]; then
    echo "WARNING: PREFIX $PREFIX not a directory; continuing anyway..."
    echo "Press Ctrl+C to cancel..."
    sleep 1
    echo "3..."
    sleep 1
    echo "2..."
    sleep 1
    echo "1..."
    sleep 1
fi

# endregion environment checks

if [ ! -f "`command -v git`" ]; then
    customDie "This script requires git. If you have Fedora, try: dnf -y install git"
fi

# region hardcoded settings

icon_name="Filmic Blender"
echo "Installing $icon_name..."

dl_name=filmic-blender
#url=https://mirror.clarkson.edu/blender/release/Blender2.79/$dl_name
dls_path=$HOME/Downloads
dl_path=$dls_path/$dl_name

bin_name=blender
bin_rel=bin/$bin_name
dest_dir_name=filmic-blender
dest_dir_path=$PREFIX/lib/$dest_dir_name
#install_src=`pwd`
#icon_img_name=voxelshop.png
#icon_img_path=$install_src/share/pixmaps/icon-48x48.png
shortcut_name=com.github.sobotka.filmic-blender.desktop
shortcut_source_name=blender.desktop
shortcut_source=
if [ -f $PREFIX/share/applications/$shortcut_source_name ]; then
    shortcut_source=$PREFIX/share/applications/$shortcut_source_name
elif [ -f /usr/local/share/applications/$shortcut_source_name ]; then
    shortcut_source=/usr/local/share/applications/$shortcut_source_name
elif [ -f /usr/share/applications/$shortcut_source_name ]; then
    shortcut_source=/usr/share/applications/$shortcut_source_name
else
    echo "WARNING: The shortcut cannot be created since there is no"
    echo "  $shortcut_source_name in PREFIX, /usr, nor /usr/local."
fi
shortcut_target=$PREFIX/share/applications/$shortcut_name

# endregion hardcoded settings

if [ ! -d "$PREFIX/lib" ]; then
    echo "WARNING: $PREFIX/lib doesn't exist, continuing anyway..."
    mkdir -p "$PREFIX/lib" || customDie "Failed to mkdir -p $PREFIX/lib"
fi

if [ ! -d "$PREFIX/share/applications" ]; then
    msg="Cannot create '$dest_dir_path/share/applications'"
    mkdir -p $dest_dir_path/share/applications || customDie "$msg"
fi

pushd $PREFIX/lib || customDie "Cannot pushd $PREFIX/lib (directory is not readable)"
git_url=https://github.com/sobotka/filmic-blender.git
if [ -d "$dest_dir_path" ]; then
    cd "$dest_dir_path"
    git pull || customDie "git pull failed in `pwd`"
else
    git clone $git_url || customDie "git clone failed for $git_url in '`pwd`'"
    if [ ! -d "$dest_dir_path" ]; then
        customDie "git clone failed to create $dest_dir_path"
    fi
fi
popd
if [ ! -f "`command -v blender`" ]; then
    echo "This will only work if blender is currently installed."
    echo "Run this script again to create an icon."
fi

if [ -z "$shortcut_source" ]; then
    exit 1
    # warning was already shown for this
fi
if [ ! -f "$shortcut_source" ]; then
    exit 1
    # warning was already shown for this
fi
if [ -f "$shortcut_target" ]; then
    rm -f "$shortcut_target" || customDie "Cannot remove old $shortcut_target."
fi
cat "$shortcut_source" | grep -v "Exec=" | grep -v "Name" >> $shortcut_target
# above intentionally removes *Name for all languages
if [ ! -f "$shortcut_target" ]; then
    customDie "You cannot rewrite $shortcut_target."
fi
echo "Name=$icon_name" >> $shortcut_target
echo "Exec=env OCIO=$dest_dir_path/config.ocio blender %f" >> $shortcut_target
echo "* rewrote $shortcut_target to use $dest_dir_path/config.ocio for OCIO."
echo "Done."
