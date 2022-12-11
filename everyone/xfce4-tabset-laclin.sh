#!/bin/bash
if [ -f "`command -v xfce4-terminal`" ]; then
    echo "Error: xfc4-terminal is already installed. If you installed a packaged version, uninstall it first. If you installed from source delete or rename '`command -v xfce4-terminal`' then run this script again."
    exit 1
fi
mkdir -p ~/tmp
cd ~/tmp
# wget -O xfce4-tabset-211106.zip https://laclin.com/misc/xfce4-tabset-211106.zip
# unzip xfce4-tabset-211106.zip
# ^ empty, so:
mkdir xfce4-tabset-211106
cd xfce4-tabset-211106
if [ $code -ne 0 ]; then exit $code; fi
wget https://laclin.com/misc/xfce4-tabset.txt
if [ $code -ne 0 ]; then exit $code; fi
wget -O xfce4-terminal-xfce4-terminal-0.8.10.zip https://gitlab.xfce.org/apps/xfce4-terminal/-/archive/xfce4-terminal-0.8.10/xfce4-terminal-xfce4-terminal-0.8.10.zip
if [ $code -ne 0 ]; then exit $code; fi
unzip xfce4-terminal-xfce4-terminal-0.8.10.zip
if [ $code -ne 0 ]; then exit $code; fi
mv xfce4-terminal-xfce4-terminal-0.8.10 xfce4-terminal-0.8.10
if [ $code -ne 0 ]; then exit $code; fi
cd xfce4-terminal-0.8.10
if [ $code -ne 0 ]; then exit $code; fi
patch -p1 < ../xfce4-tabset.txt
# ^ p1 strips off one level of the path in the patch file (xfce4-terminal-0.8.10.old/ or xfce4-terminal-0.8.10/ in this case)
code=$?
if [ $code -ne 0 ]; then exit $code; fi
if [ ! -f "configure" ]; then
    # ^ This is not a release tarball but an artefact, so ./autogen.sh would be necessary before ./configure
    ./autogen.sh
    code=$?
    if [ $code -ne 0 ]; then
        # It will show a message to install:
        # xfce4-dev-tools glib2 gtk-doc gtk+-3.0 vte-2.91 libxfce4ui-2
        echo "For Debian-based distros: sudo apt install -y xfce4-dev-tools libglib2.0-dev gtk-doc-tools gtk+-3.0-dev libvte-2.91-dev libxfce4ui-2-dev"
        exit $code
    fi
    make
    sudo make install
else
    ./configure
    code=$?
    if [ $code -ne 0 ]; then
        echo "./configure failed. Ensure you have installed build tools (such as the build-essential package on debian-based distros like Ubuntu or Linux Mint, and autotools-dev [or similar name] and autoconf packages)"
        exit $code
    fi
    make
    sudo make install

fi

../utilities/refresh-any-panel.nonroot.sh

