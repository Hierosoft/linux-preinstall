#!/bin/sh
WIN_PAPPS_DEST=/home/owner/.wine/drive_c/PortableApps
WIN_PORTABLE_CATEGORY_DEST=$WIN_PAPPS_DEST/System
WIN_UVNCR_DEST=$WIN_PORTABLE_CATEGORY_DEST/PcHelpWare
DOWNLOADED_ZIP_PATH=$HOME/Downloads/PcHelpWare_rel10.zip
#PcHelpWare folder is created by unzip command!

if [ ! -f "$DOWNLOADED_ZIP_PATH" ]; then
  cd $HOME/Downloads
  wget http://www.uvnc.com/download/PcHelpWare_rel10.zip
else
  echo using existing 
fi
#DOES have PcHelpWare folder inside

if [ ! -d "$WIN_PAPPS_DEST" ]; then
  mkdir "$WIN_PAPPS_DEST"
fi
if [ ! -d "$WIN_PORTABLE_CATEGORY_DEST" ]; then
  mkdir "$WIN_PORTABLE_CATEGORY_DEST"
fi
if [ -d "$WIN_PORTABLE_CATEGORY_DEST" ]; then
  cd "$WIN_PORTABLE_CATEGORY_DEST"
  echo ""
  echo "Installing to $(pwd)..."
  unzip "$DOWNLOADED_ZIP_PATH"
  if [ -d "$WIN_UVNCR_DEST" ]; then
    echo "Finished installing uvnc_repeater to $WIN_UVNCR_DEST"
  else
    echo "unzipping failed to create $WIN_UVNCR_DEST."
  fi
else
  echo "Failed to create $WIN_PORTABLE_CATEGORY_DEST so installation could not continue"
fi


