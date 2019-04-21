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
cat <<END
(full Blender download and patch mode (deprecated)--installs to
lib/blender-filmic to avoid confusion with lib/filmic-blender
colormanagement-only directory;

install-filmic-blender-via-runtime-env.sh
is recommended INSTEAD)..."

END
echo "Press Ctrl+C to cancel..."
sleep 2
echo "3..."
sleep 1
echo "2..."
sleep 1
echo "1..."
sleep 1

dl_name=blender-2.79b-linux-glibc219-x86_64.tar.bz2
url=https://mirror.clarkson.edu/blender/release/Blender2.79/$dl_name
dls_path=$HOME/Downloads
dl_path=$dls_path/$dl_name

bin_name=blender
bin_rel=bin/$bin_name
dest_dir_name=blender-filmic
dest_dir_path=$PREFIX/lib/$dest_dir_name
#install_src=`pwd`
#icon_img_name=voxelshop.png
#icon_img_path=$install_src/share/pixmaps/icon-48x48.png
#shortcut_name=com.blackflux.voxelshop.desktop
#shortcut_path=$install_src/share/applications/$shortcut_name

# endregion hardcoded settings

if [ ! -f "$dl_path" ]; then
    wget -O $dl_path $url || customDie "Failed to download $url"
fi


extracted_tmps=$dls_path/filmic-blender-tmp
if [ -d $extracted_tmps ]; then
    rm -Rf $extracted_tmps || customDie "Cannot remove old $dls_path/filmic-blender-tmp"
fi
mkdir -p $extracted_tmps || customDie "Cannot mkdir -p $extracted_tmps"
echo "Extracting $dl_path..."
tar -C $extracted_tmps -xjf $dl_path || tar -C $extracted_tmps -xzf $dl_path || customDie "Extracting the archive failed."

extracted_name=`ls $extracted_tmps`
install_src=$extracted_tmps/$extracted_name
if [ ! -d "$install_src" ]; then
    customDie "Extracted $install_src is not a directory."
fi
echo "Extracted $extracted_name."
echo "Installing from '$install_src'..."
patch_target="$install_src/2.79/datafiles/colormanagement"
if [ ! -d "$patch_target" ]; then
    customDie "$patch_target was not found in $patch_target: `ls $patch_target`"
fi
if [ ! -d "$dls_path/git" ]; then
    mkdir -p "$dls_path/git" || customDie "Failed to mkdir -p $dls_path/git"
fi
pushd $dls_path/git
patch_name=filmic-blender
patch_source=$dls_path/git/filmic-blender
git_url=https://github.com/sobotka/filmic-blender.git
if [ -d "$patch_name" ]; then
    cd "$patch_name"
    git pull || customDie "git pull failed in `pwd`"
else
    git clone $git_url || customDie "git clone failed for $git_url in '`pwd`'"
    if [ ! -d "$patch_source" ]; then
        customDie "git clone failed to create $patch_source"
    fi
fi
popd

echo "Removing unpatched $patch_target..."
rm -Rf "$patch_target"
echo "Overwriting $patch_target..."
cp -R "$patch_source" "$patch_target" || customDie "Failed to copy '$patch_source' to '$patch_target'."
if [ ! -d "$PREFIX/lib" ]; then
    echo "WARNING: $PREFIX/lib doesn't exist, continuing anyway..."
    mkdir -p "$PREFIX/lib" || customDie "Failed to mkdir -p $PREFIX/lib"
fi
echo "Installing to $dest_dir_path..."
rsync -rt $install_src/ $dest_dir_path
echo "Done."
echo
echo

