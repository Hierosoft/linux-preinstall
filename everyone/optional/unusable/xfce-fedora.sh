#!/bin/bash
dnf -y install @Xfce f29-backgrounds-extras-xfce xfce4-appfinder xfce4-mpc-plugin xfce4-screensaver xfce4-systemload-plugin xfce4-whiskermenu-plugin
#for volume control keys:
dnf -y install xfce4-volumed
#should already be installed by @Xfce:
dnf -y install xfce4-screenshooter xfce4-screenshooter-plugin
#Fedora-specific defaults:
dnf -y install fedora-release-xfce
#optional:
dnf -y install  fedora-jam-backgrounds-xfce f29-backgrounds-extras-xfce f29-backgrounds-xfce


#dockbarx (no package):
