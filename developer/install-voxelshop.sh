#!/bin/sh

# see also ~/git/1.pull requests/simlu/voxelshop and
# https://github.com/simlu/voxelshop/issues/ by poikilos
me=`basename $0`
echo "Starting VoxelShop install using $me..."

#https://gist.github.com/steinwaywhw/a4cd19cda655b8249d908261a62687f8
#curl -s https://api.github.com/repos/simlu/voxelshop/releases/latest \
  #| grep browser_download_url \
  #| grep linux64 \
  #| cut -d '"' -f 4 \
  #| wget -qi -
archive_url=`curl -s https://api.github.com/repos/simlu/voxelshop/releases/latest | grep browser_download_url | grep bin | cut -d '"' -f 4`

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
if [ -z "$PREFIX" ]; then
    PREFIX=$HOME/.local
fi
if [ ! -d "$PREFIX" ]; then
    echo "WARNING: PREFIX $PREFIX is not a directory but continuing anyway..."
    echo "Press Ctrl C to cancel..."
    sleep 1
    echo "3..."
    sleep 1
    echo "2..."
    sleep 1
    echo "1..."
    sleep 1
fi
echo "Installing to $PREFIX..."

#* Install VoxelShop from <https://github.com/simlu/voxelshop/releases>
#  such as (current version detected above):
if [ ! -d $PREFIX/lib ]; then
    mkdir -p $PREFIX/lib || customDie "Cannot create $PREFIX/lib"
fi
cd $PREFIX/lib || customDie "Cannot cd $PREFIX/lib"
archive_name=voxelshop-bin.zip
extracted_name=voxelshop
bin_name=voxelshop
lib_jar_name=voxelshop-start.jar
lib_jar_path=$install_src/$lib_jar_name
icon_img_name=voxelshop.png
icon_img_path=$install_src/$icon_img_name
shortcut_name=com.blackflux.voxelshop.desktop
install_src=`pwd`
if [ -f $archive_name ]; then
    echo "Removing old $archive_name file..."
    rm $archive_name || customDie "Could not remove old $archive_name file."
fi
# wget -O $archive_name $archive_url
wget $archive_url
if [ ! -f ]; then
    customDie "Downloading $archive_url did not result in a $archive_name file, so installation cannot continue."
fi
if [ -d $extracted_name ]; then
    echo "Removing old $extracted_name directory..."
    rm -Rf $extracted_name || customDie "Could not remove old $extracted_name directory."
fi
unzip $archive_name || customDie "FAILED to unzip $extracted_name"
echo "Done extracting."
if [ ! -d $extracted_name ]; then
    customDie "Extracting $archive_name did not result in $extracted_name, so installation could not continue."
fi
rm $archive_name
if [ ! -d $PREFIX/bin ]; then
    mkdir -p $PREFIX/bin || customDie "Cannot create $PREFIX/bin"
fi
echo
cd $PREFIX/bin || customDie "Cannot cd $PREFIX/bin"
if [ -f "$bin_name" ]; then
    echo "Rewriting $bin_name..."
else
    echo "Writing $bin_name..."
fi
echo '#!/bin/sh' > $bin_name
echo "java -jar $PREFIX/lib/$lib_jar_name" >> $bin_name
chmod +x $bin_name
if [ -f $install_src/$shortcut_name ]; then
    tmp_shortcut=/tmp/$USER$shortcut_name.desktop
    if [ -f $tmp_shortcut ]; then
        rm $tmp_shortcut || customDie "Cannot remove old $tmp_shortcut"
    fi
    cat $install_src/$shortcut_name | grep -v "Icon=" | grep -v "Exec=" | grep -v "Path=" > $tmp_shortcut
    if [ ! -f $tmp_shortcut ]; then
        customDie "Cannot rewrite $tmp_shortcut."
    fi
    echo Exec=$PREFIX/bin/$bin_name >> $tmp_shortcut
    if [ -f $icon_img_path ]; then
        if [ ! -d $PREFIX/share/pixmaps ]; then
            mkdir -p $PREFIX/share/pixmaps || customDie "Cannot create $PREFIX/share/pixmaps"
        fi
        if [ ! -d $PREFIX/share/pixmaps ]; then
            echo "ERROR: cannot create $PREFIX/share/pixmaps, so not installing graphic for icon"
        else
            cp -f $icon_img_path $PREFIX/share/pixmaps/
            echo Icon=$PREFIX/share/pixmaps/$icon_img_name >> $tmp_shortcut
        fi
        if [ ! -d $PREFIX/share/applications ]; then
            mkdir -p "$PREFIX/share/applications" || customDie "Cannot create $PREFIX/share/applications."
        fi
        if [ -f $PREFIX/share/applications/$shortcut_name ]; then
            rm -f $PREFIX/share/applications/$shortcut_name || customDie "Cannot remove old $PREFIX/share/applications/$shortcut_name."
        fi
        if [ -d $PREFIX/share/applications/$shortcut_name ]; then
            rm -f $PREFIX/share/applications/$shortcut_name || customDie "Cannot remove bogus folder (should be file): $PREFIX/share/applications/$shortcut_name"
        fi
        cp $tmp_shortcut $PREFIX/share/applications/$shortcut_name
        echo "Writing shortcut '$PREFIX/share/applications/$shortcut_name' is complete."
        if [[ $EUID -ne 0 ]]; then
            if [ -f "`command -v gnome-shell`" ]; then
                echo "* refreshing Gnome icons..."
                gnome-shell --replace & disown
                sleep 10
            fi
            if [ -f "$HOME/.cache/icon-cache.kcache" ]; then
                echo "* clearing $HOME/.cache/icon-cache.kcache..."
                rm $HOME/.cache/icon-cache.kcache
            fi
            if [ -f "`command -v kquitapp5`" ]; then
                echo "* refreshing KDE icons..."
                if [ "`command -v kstart5`" ]; then
                    kquitapp5 plasmashell && kstart5 plasmashell && sleep 15 || echo " - skipping plasmashell icon refresh (session not loaded)"
                else
                    kquitapp5 plasmashell && kstart plasmashell && sleep 15 || echo " - skipping plasmashell icon refresh (session not loaded)"
                fi
            fi
            if [ -f "`command -v xfce4-panel`" ]; then
                echo "* refreshing Xfce icons..."
                xfce4-panel -r && xfwm4 --replace
                sleep 5
            fi
            if [ -f "`command -v lxpanelctl`" ]; then
                echo "* refreshing LXDE icons..."
                lxpanelctl restart && openbox --restart
                sleep 5
            fi
            if [ -f "`command -v lxqt-panel`" ]; then
                echo "* refreshing LXQt icons..."
                killall lxqt-panel && lxqt-panel &
            fi
        else
           echo "Since running as root, this script will not update application menus for any currently logged in user(s)."
        fi
    else
        echo "WARNING: cannot add graphical icon to shortcut since missing $install_src/$icon_img_name."
    fi
else
    echo "WARNING: cannot add shortcut since missing $install_src/$shortcut_name."
fi

echo "Done."
