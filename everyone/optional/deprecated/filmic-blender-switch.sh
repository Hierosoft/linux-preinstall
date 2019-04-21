#!/bin/bash
echo
if [ ! -d "$HOME/Backup" ]; then
  mkdir "$HOME/Backup"
fi
cd "$HOME/Backup"
if [ ! -d filmic-blender ]; then
  echo "Cloning filmic-blender from GitHub..."
  git clone https://github.com/sobotka/filmic-blender.git
else
  cd filmic-blender
  echo "Updating filmic-blender from GitHub..."
  git pull
  cd ..
fi

target="/usr/share/blender/datafiles/colormanagement"
if [ -d "$target" ]; then
  echo "Processing $target..."
else
  echo "Your version is not known by the script. You will have to manually overwrite your colormanagement folder because it is not '$target'."
  exit 1
fi

if [ ! -d "colormanagement" ]; then
  echo
  echo "Make sure you have NOT installed filmic-blender before running this script--otherwise replace '$target/colormanagement' (being created now from $target) with Blender's version of colormanagement."
  cp -Rf "$target" ./
  echo
fi
sudo rm -Rf "$target"
if [ $1 = "remove" ]; then
  echo "Removing filmic-blender..."
  sudo cp -Rf colormanagement "$target"
else
  echo "installing filmic-blender (run '$(basename "$0") remove' to remove)..."
  sudo cp -Rf filmic-blender "$target"
fi
