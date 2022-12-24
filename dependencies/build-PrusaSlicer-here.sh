#!/bin/bash
# This file is based on the PrusaSlicer "Building PrusaSlicer on UNIX/Linux" documentation at
# <https://github.com/prusa3d/PrusaSlicer/blob/master/doc/How%20to%20build%20-%20Linux%20et%20al.md>.
me="$0"
PRUSASLICER_REPO_DIR="`pwd`"
echo "[$me] If anything fails, first try:"

PACKAGE_TYPE="apt"
if [ -f "`command -v dnf`" ]; then
    PACKAGE_TYPE="rpm"
elif [ -f "`command -v rpm`" ]; then
    PACKAGE_TYPE="rpm"
fi

if [ "$PACKAGE_TYPE" = "rpm" ]; then
>&2 cat <<END
sudo dnf -y groupinstall "C Development Tools and Libraries"
sudo dnf -y groupinstall "Development Tools"
sudo dnf install -y \
    git \
    autoconf \
    cmake \
    mesa-libGLU-devel \
    gtk3-devel \
    dbus-devel \
;

END
else
>&2 cat <<END
# Install build dependencies on Ubuntu 20.10 or a similar distro:
sudo apt-get install  -y \
    git \
    build-essential \
    autoconf \
    cmake \
    libglu1-mesa-dev \
    libgtk-3-dev \
    libdbus-1-dev \
;

END
fi

cd deps
if [ $? -ne 0 ]; then exit 1; fi
mkdir -p build
if [ $? -ne 0 ]; then exit 1; fi
cd build
if [ $? -ne 0 ]; then exit 1; fi
cmake .. -DDEP_WX_GTK3=ON
if [ $? -ne 0 ]; then >&2 echo "[$me] cmake failed in `pwd`"; exit 1; fi
make
if [ $? -ne 0 ]; then exit 1; fi
# cd ../..
cd "$PRUSASLICER_REPO_DIR"
if [ $? -ne 0 ]; then exit 1; fi

mkdir -p build
if [ $? -ne 0 ]; then exit 1; fi
cd build
if [ $? -ne 0 ]; then exit 1; fi
cmake .. -DSLIC3R_STATIC=1 -DSLIC3R_GTK=3 -DSLIC3R_PCH=OFF -DCMAKE_PREFIX_PATH=$(pwd)/../deps/build/destdir/usr/local
if [ $? -ne 0 ]; then >&2 echo "[$me] cmake failed in `pwd`/.."; exit 1; fi
# make -j$(nproc)
# ^ froze an Intel i7 12000U (ASUS ROG Strix C15 tower)
physical_cores=`grep ^"core id" /proc/cpuinfo | sort -u | wc -l`
make -j$((physical_cores-1))
# make -j4
if [ $? -ne 0 ]; then >&2 echo "[$me] make failed in `pwd`. If you don't see an error in red/orange, maybe a test failed. You may want to copy the output to a text editor and search for the word \"error\""; exit 1; fi

cd src
./prusa-slicer
