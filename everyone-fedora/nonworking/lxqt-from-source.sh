#!/bin/bash
me=`basename $0`

# region common
postinstall="generated.md"
maindir=""
if [ -f api.rc ]; then
    maindir="."
elif [ -f ../api.rc ]; then
    maindir=".."
elif [ -f ../../api.rc ]; then
    maindir="../.."
elif [ -f ../../../api.rc ]; then
    maindir="../../.."
fi
if [ ! -z "$maindir" ]; then
    source $maindir/api.rc
    postinstall="$maindir/$_POSTINSTALL_NAME"
else
    echo "WARNING: api.rc cannot be found in `pwd` nor up to ../../.."
    echo "  tips will be placed in `pwd`/$postinstall instead."
fi
touch $postinstall
# endregion common

## LXQt (an LXQt dev says 2019-03-31 that 0.13.0 included with Fedora 29 is "old")
#see https://github.com/lxqt/lxqt/wiki/Building-from-source
#for compiling lxqt (Qt deps):
dnf -y install qt5-qtbase-devel qt5-qtsvg-devel qt5-qttools-devel qt5-qtx11extras-devel
#for compiling lxqt (KDE deps):
dnf -y install kf5-kguiaddons-devel libkscreen-qt5-devel kf5-kidletime-devel kf5-kwindowsystem-devel kf5-solid-devel
#for compiling lxqt (misc deps):
dnf -y install systemd-devel bash libstatgrab-devel alsa-lib-devel pulseaudio-libs-devel lm_sensors-devel libconfig-devel muParser-devel upower-devel polkit-devel polkit-qt5-1-devel sudo libexif-devel xorg-x11-apps libSM-devel libXScrnSaver-devel libXcursor-devel libXcomposite-devel libxcb-devel xcb-util-devel libxkbcommon-x11-devel dbusmenu-qt5-devel libfm-devel menu-cache-devel lxmenu-data gtk-update-icon-cache hicolor-icon-theme xdg-utils xdg-user-dirs oxygen-icon-theme openbox openbox-devel
git submodule init
git submodule update --remote --rebase
xdg-mime default pcmanfm-qt.desktop inode/directory

cat >> $postinstall <<END
## screenshot hotkey for LXQt
By Default, LXQt (0.13.0 via @lxqt metapackage in Fedora 29)
- Runs the global hotkeys daemon (lxqt-globalkeysd) on startup
- Sets PrtScr ("Print" according to LXQt) key to run: lximage-qt -s
If it doesn't work, or you  require manual settings, see:
<https://www.pcsuggest.com/linux-screenshot-with-hotkeys/>
If it is already working and you just want to change the hotkey or
program, search the application menu for "Shortcut" and use the
"Shortcut Keys" program to change the setting.
END
#dnf -y install lximage-qt scrot lxqt-globalkeys
