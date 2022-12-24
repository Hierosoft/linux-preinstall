#!/bin/bash
# See also developer/developer.fedora.sh
if [ -f "`command -v xfce4-terminal`" ]; then
    echo "Error: xfc4-terminal is already installed. If you installed a packaged version, uninstall it first. If you installed from source delete or rename '`command -v xfce4-terminal`' then run this script again."
    exit 1
fi
mkdir -p ~/tmp
cd ~/tmp
TMP_SUB=~/tmp/xfce4-tabset-211106
# wget -O xfce4-tabset-211106.zip https://laclin.com/misc/xfce4-tabset-211106.zip
# unzip xfce4-tabset-211106.zip
# ^ empty, so:
mkdir $TMP_SUB
cd $TMP_SUB
code=$?
if [ $code -ne 0 ]; then exit $code; fi
wget https://laclin.com/misc/xfce4-tabset.txt
code=$?
if [ $code -ne 0 ]; then exit $code; fi
wget -O xfce4-terminal-xfce4-terminal-0.8.10.zip https://gitlab.xfce.org/apps/xfce4-terminal/-/archive/xfce4-terminal-0.8.10/xfce4-terminal-xfce4-terminal-0.8.10.zip
code=$?
if [ $code -ne 0 ]; then exit $code; fi
unzip -o xfce4-terminal-xfce4-terminal-0.8.10.zip
# -o: overwrite files without prompting
code=$?
if [ $code -ne 0 ]; then exit $code; fi
LONG_DIR=$TMP_SUB/xfce4-terminal-xfce4-terminal-0.8.10
SHORT_DIR=$TMP_SUB/xfce4-terminal-0.8.10
echo "mv $LONG_DIR $SHORT_DIR..."
if [ -d "$SHORT_DIR" ]; then
    echo "* removing old $SHORT_DIR"
    rm -Rf "$SHORT_DIR"
fi
mv $LONG_DIR $SHORT_DIR
code=$?
if [ $code -ne 0 ]; then exit $code; fi
cd xfce4-terminal-0.8.10
code=$?
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
        cat <<END
For Debian-based distros: sudo apt install -y xfce4-dev-tools libglib2.0-dev gtk-doc-tools gtk+-3.0-dev libvte-2.91-dev libxfce4ui-2-dev
For Fedora:
  sudo dnf groupinstall "Development Tools" "Development Libraries"
  # If you get an selinux error, click Troubleshoot, run the commands it suggests if is correct, then reinstall:
  # sudo dnf groupremove "Development Tools" "Development Libraries"
  # sudo dnf groupinstall "Development Tools" "Development Libraries"
  sudo dnf install libtool gtk3-devel vte291-devel libxfce4ui-devel
  # Didn't help: vte-devel
  # You may have to close and reopen the terminal.
END
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

