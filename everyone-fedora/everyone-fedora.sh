#!/bin/bash

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

