#!/bin/sh
PREFIX=$HOME/.local
appimages=$PREFIX/lib
#if [ ! -f "`command -v git-cola`" ]; then
#  python3 -m pip install https://github.com/git-cola/git-cola/zipball/master --user
  # with --user option, this installs launch script to /home/owner/.local/bin/git-cola
#fi
# flatpak install gimp


#    kdenlive \
# DON'T use kdenlive <=18.12 (such as from Fedora 29):
# see [kdenlive] [Bug 407808] Right-Click to Transcode Clip Always Chooses PAL Even When User Chooses NTSC
# > Dev cannot backport to 18.12 and older versions anymore as 60% of the code has
# > changed.
# >
# > Please try with the current Kdenlive AppImage version 19.04.1b to see if there
# > are any packaging issues https://files.kde.org/kdenlive/release/

appimage_dir_name=kdenlive
appimage_bin_name=kdenlive
appimage_dir="$appimages/$appimage_dir_name"
dl_name=kdenlive-19.04.1b-x86_64.appimage
ok=true
present=true
enable_dl=false
if [ "`readlink $PREFIX/bin/$appimage_bin_name`" != "$appimage_dir/$dl_name" ]; then
    present=false
    echo "`readlink $PREFIX/bin/$appimage_bin_name` is not $appimage_dir/$dl_name."
fi
if [ ! -d "$appimage_dir" ]; then
    mkdir -p "$appimage_dir" || ok=false
    if [ "@$ok" = "@false" ]; then
        echo "FAILED to create $appimage_dir"
    fi
fi
dl_path=$appimage_dir/$dl_name

#if [ "@$ok" = "@false" ]; then
    if [ ! -f "$dl_path" ]; then
        present=false
        enable_dl=true
    fi
#fi
echo "present: $present"
echo "enable_dl: $enable_dl"
if [ "@$present" = "@false" ]; then
    if [ "@$enable_dl" = "@true" ]; then
        wget -O $dl_path https://files.kde.org/kdenlive/release/$dl_name || ok=false
    else
        echo "* using existing $dl_path"
    fi
    if [ "@$ok" = "@true" ]; then
        if [ ! -d "$PREFIX/bin" ]; then
            mkdir "$PREFIX/bin" || ok=false
        fi
        if [ "@$ok" = "@true" ]; then
            chmod +x "$appimage_dir/$dl_name"
            if [ -f "$PREFIX/bin/$appimage_bin_name" ]; then
                rm "$PREFIX/bin/$appimage_bin_name"
            fi
            ln -s "$appimage_dir/$dl_name" "$PREFIX/bin/$appimage_bin_name"
            shortcut_src=share/applications/org.kde.kdenlive.desktop
            shortcut_dst=$PREFIX/share/applications/org.kde.kdenlive.desktop
            if [ -f "$shortcut_src" ]; then
                cat "$shortcut_src" | grep -v "Exec=" > "$shortcut_dst"
                echo "Exec=$PREFIX/bin/$appimage_bin_name" >> "$shortcut_dst"
                echo "* Rewrote '$shortcut_dst'"
            else
                echo "MISSING $ico_src"
            fi
            #Exec=kdenlive %U
        fi
    else
        echo "FAILED to download $dl_name"
    fi
fi
exit 0
# see <https://askubuntu.com/questions/237942/how-does-copy-paste-work-with-xterm>
# (also mentions that apparently Shift+Ins or Shift+Middle Click works in some cases without the setting below)
touch ~/.Xresources
echo "XTerm*selectToClipboard: true" >> ~/.Xresources
xrdb -merge ~/.Xresources
cat <<END
Manual steps needed:
* Firefox plugin
* Blender Fiber Mesh: see also <https://blenderartists.org/t/fiber-mesh-resurrected-for-2-80/1141872>
  Install via User Preferences, Addons, Install in Blender
END
cd
if [ ! -d ~/Downloads/git/amadvance ]; then mkdir ~/Downloads/git/amadvance; fi
cd ~/Downloads/git/amadvance
# includes scalerx command (resize png while preserving edge shape):
git clone https://github.com/amadvance/scale2x.git
cd scale2x
./autogen.sh
./configure
make
