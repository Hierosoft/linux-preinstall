#!/bin/sh
cd
if [ ! -d Downloads/git ]; then
  mkdir -p Downloads/git
fi
cd Downloads/git
url="$1"
if [ -z "$url" ]; then
  echo
  echo "ERROR: nothing done since no url was specified (http* url ending in .git should be specified as param to this script)"
  echo
  echo
  exit 1
fi
project_dot_git=${url##*/}
name=`echo "$project_dot_git" | cut -d'.' -f1`
echo "$name"
src=""
if [ ! -d "$name" ]; then
  git clone "$url"
  if [ -d "$name" ]; then
    cd "$name"
    src="$(pwd)"
  fi
else
  cd "$name"
  src="$(pwd)"
  git pull
fi
if [ ! -d "$src" ]; then
  echo
  echo "ERROR: nothing done since url was not accessible"
  echo
  echo
  exit 2
fi
#addons="/usr/local/share/blender/scripts/addons"
versions_path="$HOME/.blender"
if [ -d "$HOME/.config/blender" ]; then
  versions_path="$HOME/.config/blender"
fi
version_path=""
version=""
if [ ! -d "$versions_path" ]; then
  echo
  echo "ERROR: Nothing done since $versions_path is missing so cannot determine Blender addons path"
  echo "--path such as $HOME/.blender/2.79 must exist for this script to work."
  echo
  echo
  exit 1
fi
for sv in 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99
do
  version_path="$versions_path/2.$sv"
  #echo "looking for $version_path..."
  if [ -d "$version_path" ]; then
    echo "found."
    cd "$version_path"
    version="2.$sv"
  fi
done
version_path="$versions_path/$version"
if [ ! -d "$version_path" ]; then
  echo
  echo "ERROR: Nothing done since $versions_path is missing version-specific directory so cannot determine Blender addons path"
  echo "--path such as $version_path must exist for this script to work."
  echo
  echo
  exit 2
fi
addons="$version_path/scripts/addons"
if [ ! -d "$addons" ]; then
  mkdir -p "$addons"
fi
echo
addon="$addons/$name"
echo "Installing $name/* files to $addons..."
echo
#rsync -rtv "$src/" "$addons"
if [ -d "$addon" ]; then
  echo "Removing incorrectly installed $addon..."
  rm -Rf "$addon"
fi
cp -R $src/*.py "$addons/"
echo
echo "You still need to enable the addon in Blender:"
echo "  * File, User Preferences"
echo "  * Addons"
echo "  * Check the box for $name"
echo
echo
