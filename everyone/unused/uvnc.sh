#!/bin/sh
WIN_PAPPS_DEST=/home/owner/.wine/drive_c/PortableApps
WIN_PORTABLE_CATEGORY_DEST=$WIN_PAPPS_DEST/System
WIN_UVNCR_DEST=$WIN_PORTABLE_CATEGORY_DEST/uvnc_repeater
echo "Get windows version by accepting license at http://www.uvnc.com/downloads/repeater/83-repeater-downloads.html"
echo "and save to $HOME/Downloads"
read -n1 -rsp $'Press any key to continue or Ctrl+C to exit...\n'
cd $HOME
if [ ! -d "$WIN_PAPPS_DEST" ]; then
  mkdir "$WIN_PAPPS_DEST"
fi
if [ ! -d "$WIN_PORTABLE_CATEGORY_DEST" ]; then
  mkdir "$WIN_PORTABLE_CATEGORY_DEST"
fi
if [ ! -d "$WIN_UVNCR_DEST" ]; then
  mkdir "$WIN_UVNCR_DEST"
fi
if [ -d "$WIN_UVNCR_DEST" ]; then
  cd "$WIN_UVNCR_DEST"
  echo ""
  echo "Installing to $(pwd)..."
  unzip $HOME/Downloads/repeater1200.zip
  if [ -f "$WIN_UVNCR_DEST/passwd.txt" ]; then
    echo "passwd.txt not found; perhaps installation failed."
  else
    echo "Finished installing uvnc_repeater to $WIN_UVNCR_DEST"
  fi
else
  echo "Failed to create $WIN_UVNCR_DEST so installation could not finish."
fi
#sudo apt-get install winetricks

