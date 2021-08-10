#!/bin/bash
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
return $?

cat > /dev/null <<END
. /etc/os-release
#CODEBLOCKS_PKG=codeblocks
if [ "@$VERSION_CODENAME" = "@buster" ]; then
    #CODEBLOCKS_PKG=
    echo "* You are using buster and codeblocks is very old and crashy on that."
    if [ -f "`command -v flatpak`" ]; then
        # ^ Use flatpak if Debian 10 it is really old and crashes.
        flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
        # flatpak install -y flathub org.codeblocks.codeblocks
        # ^ Use system rather than `--user` for *everything* in linux-preinstall to avoid doubling up on dependencies.
        if [ $? -ne 0 ]; then
            echo "Error: 'flatpak install -y flathub org.codeblocks.codeblocks' failed."
            exit 1
        fi
    else
        echo " Error: flatpak is not installed."
        exit 1
    fi
else
    echo "Error: This script is only tested on buster."
    exit 1
fi

END
