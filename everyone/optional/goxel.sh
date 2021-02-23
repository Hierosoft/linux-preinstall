#!/bin/bash
source $HOME/.config/linux-preinstall/globals.rc
if [ $? -ne 0 ]; then
    echo "ERROR: 'source $HOME/.config/linux-preinstall/globals.rc' failed."
    echo "You must run linux-preinstall/setup.sh first."
    exit 1
fi
source $LINUX_PREINSTALL/api.rc
if [ $? -ne 0 ]; then
    echo "ERROR: 'source $LINUX_PREINSTALL/api.rc' failed."
    echo "You must run linux-preinstall/setup.sh first."
    exit 1
fi
cat > /dev/null <<END
if [ -z "$INSTALL_CMD" ]; then
    if [ -f "`command -v dnf`" ]; then
        INSTALL_CMD=dnf
    elif [ -f "`command -v yum`" ]; then
        INSTALL_CMD=yum
    elif [ -f "`command -v apt`" ]; then
        INSTALL_CMD=apt
    elif [ -f "`command -v apt-get`" ]; then
        INSTALL_CMD=apt-get
    fi
fi
if [ -z "$PKG_TYPE" ]; then
    if [ "$INSTALL_CMD" = "dnf" ]; then
        PKG_TYPE=rpm
    elif [ "$INSTALL_CMD" = "yum" ]; then
        PKG_TYPE=rpm
    elif [ "$INSTALL_CMD" = "apt" ]; then
        PKG_TYPE=deb
    elif [ "$INSTALL_CMD" = "apt-get" ]; then
        PKG_TYPE=deb
    fi
fi
END
# ^ from https://github.com/poikilos/linux-preinstall/api.rc
$INSTALL_CMD scons pkg-config $GTK3_DEV_PKG $GLFW_DEV_PKG
MISSING=
if [ -z "$GTK3_DEV_PKG" ]; then
    MISSING="$MISSING GTK3_DEV_PKG"
fi
if [ -z "$GLFW_DEV_PKG" ]; then
    MISSING="$MISSING GLFW_DEV_PKG"
fi
if [ -z "$MISSING" ]; then
    echo "Building is not possible because you are missing: $MISSING"
    echo "Update linux-preinstall or set those environment variables to the corresponding $INSTALL_BIN package names."
    exit 1
fi
cat > /dev/null <<END
if [ "@$PKG_TYPE" = "@rpm" ]; then
    $INSTALL_CMD scons pkg-config glfw-devel gtk3-devel
    # glfw-devel is glfw-devel-3.3.2 as of Fedora 31 2020-04-23
elif [ "@$PKG_TYPE" = "@deb" ]; then
    $INSTALL_CMD scons pkg-config libglfw3-dev libgtk-3-dev
else
    echo "The PKG_TYPE $PKG_TYPE is not yet implemented for $0."
    echo " So that this script can determine package names,"
    echo " PKG_TYPE should be set to deb or rpm even if you are not"
    echo " using a repo."
fi
END
