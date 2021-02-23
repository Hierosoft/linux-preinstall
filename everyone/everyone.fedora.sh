#!/bin/bash

# GNOME extensions: see bottom

source /etc/os-release
wget https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$VERSION_ID.noarch.rpm
wget https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$VERSION_ID.noarch.rpm
rpm -iv rpmfusion-free-release-$VERSION_ID.noarch.rpm
dnf -y upgrade
rpm -iv rpmfusion-nonfree-release-$VERSION_ID.noarch.rpm

dnf -y install \
  audacity-freeworld \
  chromium \
  evince \
  gimp \
  nano \
  openssh \
  rsync \
  simple-scan \
  thunderbird \
  ;
# audacity-freeworld installs audacity with MP3 support
# evince: ("Document Viewer") PDF viewer, fast & accurate unlike okular

# region GNOME
dnf -y install @gnome
dnf -y install gnome-tweak-tool gparted
echo "You don't need the following, but they are not removed since you may use KDE (they may not be installed anyway):"
echo "dnf -y remove kparted k3b"
cat <<END
* Install https://chrome.google.com/webstore/detail/gnome-shell-integration/gphhapmejobijbbhgpjhcjognlahblep?hl=en
  - Then the following from https://extensions.gnome.org/#page=2
    - Screenshot Locations
      * change location: Open GNOME Tweaks, Extensions,
    - Dash to Dock (keeps dash icons open, allows moving to another edge)
    - (optional) Clipboard
    - Application Menu
    - System Tray
    - [Desktop Icons](https://extensions.gnome.org/extension/1465/desktop-icons/)
    - [Sound Input & Output Device
      Chooser](https://extensions.gnome.org/extension/906/sound-output-device-chooser/)
    - [Vitals](https://extensions.gnome.org/extension/1460/vitals/)
    - [Microphone Echo-Cancellation]
      (https://extensions.gnome.org/extension/1456/microphone-echo-cancellation/)
    - [System
      Info](https://extensions.gnome.org/extension/471/system-info/)
  - and optionally:
    - [IdleRPG](https://extensions.gnome.org/extension/643/idlerpg/)
    - [Mumble](https://extensions.gnome.org/extension/1090/mumble/):
      adds overlay option when right-clicking applications
    - [Transparent GNOME panel]
      (https://extensions.gnome.org/extension/1099/transparent-gnome-panel/)
    - [Presences]
      (https://extensions.gnome.org/extension/447/presences/):
      "Enables all online status types (available, busy, away, hidden,
      offline) in user menu."
    - [Pidgin @ User Menu]
      (https://extensions.gnome.org/extension/506/pidgin-in-user-menu/)
    - [quake-menu]
      (https://extensions.gnome.org/extension/1411/quake-mode/)
    - [NVIDIA GPU Stats Tool]
      (https://extensions.gnome.org/extension/1320/nvidia-gpu-stats-tool/)
    - [KStatusNotifierItem/AppIndicator Support]
      (https://extensions.gnome.org/extension/615/appindicator-support/)
    - [Battery Percentage and Time]
      (https://extensions.gnome.org/extension/1771/battery-percentage-and-time/)
  - The following don't seem to be needed anymore on GNOME 3.32.2:
    - [Backlight Control]
      (https://extensions.gnome.org/extension/1293/backlight-control/)
    - [Applications
      Menu](https://extensions.gnome.org/extension/6/applications-menu/)
  - The following only work on the distro mentioned in the name:
    - [Fedora Linux Updates
      Indicator](https://extensions.gnome.org/extension/1150/fedora-linux-updates-indicator/)
  - Remember to ENABLE them using Tweaks (gnome-tweak-tool application),
    in the "Extensions" section.
    - Also, mannually click the gear by Dash to Dock and change:
      - Position and Size:
        - maximum width
        - Position on screen: Bottom
        - Dock size limit: 100% (prevents icons getting hidden off edge;
          icons scale by default to also prevent that default GNOME
	  behavior of hiding icons so be sure to leave Fixed icon size
	  turned off.
      - Launchers:
	- CHECK "Move the applications button to the beginning..."
	- UNCHECK "Animate 'Show Applications'"
      - Behavior: leave Click action on "Cycle through windows"
        ("Raise window" does NOT raise all instances, so it is not very
	useful)
      - Behavior: Scroll action: Do nothing
      - Appearance:
	- Shrink the dash: ON

END
# endregion GNOME

dnf -y install python3-pillow python3-numpy python3-leveldb
# there is no python2-leveldb, so skip:
#dnf -y install python2-pillow python2-numpy

