#!/bin/sh
mkdir -p ~/tmp
cd ~/tmp
BIN_DIR=~/.local/bin
LIB_DIR=~/.local/lib
mkdir -p $LIB_DIR/minecraft
if [ $? -ne 0 ]; then exit 1; fi
wget -O Minecraft.tar.gz https://launcher.mojang.com/download/Minecraft.tar.gz

tar xvf ~/tmp/Minecraft.tar.gz
if [ $? -ne 0 ]; then exit 1; fi

mkdir -p $BIN_DIR
if [ $? -ne 0 ]; then exit 1; fi

if [ -d $BIN_DIR/minecraft-launcher ]; then
    rm $BIN_DIR/minecraft-launcher/minecraft-launcher
    rmdir $BIN_DIR/minecraft-launcher
fi

if [ -f minecraft-launcher/minecraft-launcher ]; then
    mv minecraft-launcher/minecraft-launcher $BIN_DIR/
    code=$?
elif [ -f minecraft-launcher ]; then
    mv minecraft-launcher/minecraft-launcher $BIN_DIR/
    code=$?
else
    echo "Error: A minecraft-launcher file wasn't found:"
    ls -lrt ~/tmp
    exit 1
fi
chmod +x $BIN_DIR/minecraft-launcher
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/mojang-com.minecraft.desktop <<END
[Desktop Entry]
Name=Minecraft
Exec=$BIN_DIR/minecraft-launcher
Path=$LIB_DIR/minecraft
Icon=minecraft
Terminal=false
Type=Application
END
xdg-desktop-icon install ~/.local/share/applications/mojang-com.minecraft.desktop
exit $code
#cd $BIN_DIR
