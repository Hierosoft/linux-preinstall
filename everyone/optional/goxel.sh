#!/bin/bash
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
if [ "@$PKG_TYPE" = "@rpm" ]; then
    $INSTALL_CMD install -y scons pkg-config glfw-devel gtk3-devel
    # glfw-devel is glfw-devel-3.3.2 as of Fedora 31 2020-04-23
elif [ "@$PKG_TYPE" = "@deb" ]; then
    $INSTALL_CMD install -y scons pkg-config libglfw3-dev libgtk-3-dev
else
    echo "The PKG_TYPE $PKG_TYPE is unknown. So that this script can determine package names, PKG_TYPE should be set to deb or rpm even if you are not using a repo."
fi
