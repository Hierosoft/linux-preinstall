#!/bin/bash
cat /dev/null <<END
2021-11-05 PM from OldCoder to Poikilos
OldCoder: ===
OldCoder: https://laclin.com/xfce4-tabset.html
OldCoder: If you, please test
OldCoder: Build instructions are:
OldCoder: wget http://deb.debian.org/debian/pool/main/x/xfce4-terminal/xfce4-terminal_0.8.10.orig.tar.bz2
OldCoder: tar jxf that.tar.bz2
OldCoder: cd that
OldCoder: patch -p1 < /somewhere/thepatch.txt
Poikilos: will do!
OldCoder: autoreconf -fi
OldCoder: ./configure --enable-maintainer-mode
OldCoder: make -j4
OldCoder: make install
OldCoder: # done
END
mkdir -p ~/Downloads/laclin
cd ~/Downloads/laclin
echo "* Information and updates regarding this feature patch is at <https://laclin.com/xfce4-tabset.html>."
sudo apt install -y libvte-2.91-dev libxfce4ui-2-dev intltool xfce4-dev-tools
if [ ! -f "xfce4-terminal_0.8.10.orig.tar.bz2" ]; then
    wget http://deb.debian.org/debian/pool/main/x/xfce4-terminal/xfce4-terminal_0.8.10.orig.tar.bz2
    if [ $? -ne 0 ]; then exit 1; fi
fi
if [ ! -d "xfce4-terminal-0.8.10" ]; then
    tar xf xfce4-terminal_0.8.10.orig.tar.bz2
    if [ $? -ne 0 ]; then exit 1; fi
fi
cd xfce4-terminal-0.8.10
if [ $? -ne 0 ]; then exit 1; fi
if [ ! -f "xfce4-tabset.txt" ]; then
    wget https://laclin.com/misc/xfce4-tabset.txt
    if [ $? -ne 0 ]; then
        if [ -f "xfce4-tabset.txt" ]; then
            rm "xfce4-tabset.txt"
        fi
        exit 1
    fi
    # nano xfce4-tabset.txt
    echo "* patching..."
    patch -p1  < "xfce4-tabset.txt"
    # ^ p1 is remove first filename before slash (is supposed to prevent needing to do cd ..)
    if [ $? -ne 0 ]; then exit 1; fi
fi
#echo "* [$0] autoreconf -fi..."
#autoreconf -fi
cat > /dev/null <<END
Poikilos: ./configure gives: checking for Gnome default applications dir... Package gnome-default-applications was not found in the pkg-config search path.
Poikilos: Perhaps you should add the directory containing \`gnome-default-applications.pc'
Poikilos: to the PKG_CONFIG_PATH environment variable
Poikilos: No package 'gnome-default-applications' found
Poikilos: Using prefix of terminal
Poikilos: ./configure: line 16295: syntax error near unexpected token \`1.9'
Poikilos: ./configure: line 16295: \`GTK_DOC_CHECK(1.9)
OldCoder: bbs
Poikilos: There is no gnome-default-applications in Devuan
OldCoder: Back
OldCoder: OK, redo w/out autoreconf step and also install
END
if [ $? -ne 0 ]; then exit 1; fi
echo "* [$0] ./configure --enable-maintainer-mode..."
./configure --enable-maintainer-mode
if [ $? -ne 0 ]; then exit 1; fi
echo "* [$0] make -j4..."
make -j4
if [ $? -ne 0 ]; then exit 1; fi
echo "* [$0] sudo killall xfce4-terminal..."
sudo killall xfce4-terminal
echo "* [$0] sudo make install..."
sudo make install
if [ $? -ne 0 ]; then exit 1; fi
echo Done
exit 0
