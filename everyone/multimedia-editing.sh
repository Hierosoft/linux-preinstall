#!/bin/sh

#!/bin/bash
cd ~
if [ ! -d Downloads ]; then mkdir Downloads; fi
cd Downloads
dl_name=voxelshop-bin.zip
ex_name=voxelshop
if [ ! -f $dl_name ]; then
    wget -O $dl_name https://github.com/simlu/voxelshop/releases/download/1.8.25/$dl_name
fi
if [ ! -d "$ex_name" ]; then
    unzip $dl_name
fi
cd $ex_name && bash install-linux.sh
#if [ -f voxelshop.sh ]; then
#    bash voxelshop.sh
#else
#    echo "* The VoxelShop install script normally with this script was not found"
#    echo "  (try deprecated/voxelshop.sh manually)."
#    echo "  You can install VoxelShop from https://github.com/simlu/voxelshop/releases"
#fi

cat <<END
In Blender, User Preferences, Add-ons, enable:
  - Color Palette

Then click "Save User Preferences" to preserve the settings for other
project files.
END
