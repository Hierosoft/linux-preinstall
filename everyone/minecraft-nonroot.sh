#!/bin/bash
echo
echo
echo "INFO: Choose the Java Edition if your OS is 32-bit."
echo
sleep 5

install_minecraft_launcher_archive(){
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
    USER_DT=~/.local/share/applications/mojang-com.minecraft.desktop
    cat > "$USER_DT" <<END
[Desktop Entry]
Name=Minecraft
Exec=$BIN_DIR/minecraft-launcher
Path=$LIB_DIR/minecraft
Icon=minecraft
Terminal=false
Type=Application
END
    xdg-desktop-icon install "$USER_DT"
    code=$?
    if [ $code -ne 0 ]; then
        >&2 echo "Error: Failed to install $USER_DT to the Desktop. Try the icon in your Applications menu."
    else
        echo "Installed $USER_DT to the desktop."
    fi
    exit $code
    #cd $BIN_DIR
}


if [ ! -f "`rpm`" ]; then
    # echo "Only rpm-based distros are available currently."
    echo "Installing minecraft from official tar archive"
    echo "(Other options:"
    echo "For deb-based distros, use the official deb."
    echo "For Arch, use AUR)..."
    install_minecraft_launcher_archive
    exit $?
fi

if [ ! -f "`command -v rpmbuild`" ]; then
    echo "You must have rpmbuild"
    exit 1
fi

if [ ! -f "`command -v wget`" ]; then
    echo "You must have wget"
    exit 1
fi

if [ ! -f "`command -v tar`" ]; then
    echo "You must have tar"
    exit 1
fi

if [ ! -f "`command -v bash`" ]; then
    echo "You must have bash"
    exit 1
fi

curl https://raw.githubusercontent.com/DarkWav/Minecraft-Installer-RPM/master/minecraft-installer.sh | bash

echo "Uninstall:"
echo "    sudo rpm -e minecraft-launcher"
