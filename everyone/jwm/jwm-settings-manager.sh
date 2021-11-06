#!/bin/bash
cat <<END
2021-11-14 PM to Poikilos via IRC
<OldCoder> fltk, hm
<OldCoder> wate
<OldCoder> building (verb not noun)
<OldCoder> cmake  -DCMAKE_INSTALL_PREFIX=/ram/bo ../..
<OldCoder> make -j4 works
<OldCoder> bilt
<OldCoder> links
<OldCoder> wate
<OldCoder> http://oldcoder.org/moo.png
<OldCoder> Is that what you're seeking?
<OldCoder> http://oldcoder.org/moo.png
<OldCoder> There are 2 other programs as well; I haven
<OldCoder> There are 2 other programs as well; I haven
<OldCoder> 't checked to see what they do
<OldCoder> http://oldcoder.org/jwm-settings-manager.tar.bz2
<OldCoder> http://oldcoder.org/moo.png
<OldCoder> Needs fltk, cmake, and a few other things. Not many.
<Poikilos> ty; will try
<OldCoder> have fun
<OldCoder> whee see FOSS is for me and thee
<OldCoder> just do
<OldCoder> mkdir bin/release
<OldCoder> cd bin/release
<OldCoder> cmake ../..
<OldCoder> make -j4
<OldCoder> make install
<OldCoder>
<OldCoder> Read files for/about dependencies first

Based on readme:
# Build Depends on Debian/Ubuntu
sudo apt-get update && sudo apt-get install \
  cmake \
  gcc-multilib \
  g++-multilib \
  libc6 \
  libfltk-images1.3 \
  libfltk1.3 \
  libfltk1.3-dev \
  libfltk1.3-compat-headers \
  libgcc1 \
  libstdc++6 \
  libx11-dev \
  libxpm-dev \
  fluid \
  pkg-config

mkdir -p bin/Release
cd bin/Release && cmake ../.. && sudo make install
END

sudo apt-get update && sudo apt-get install \
  cmake \
  gcc-multilib \
  g++-multilib \
  libc6 \
  libfltk-images1.3 \
  libfltk1.3 \
  libfltk1.3-dev \
  libfltk1.3-compat-headers \
  libgcc1 \
  libstdc++6 \
  libx11-dev \
  libxpm-dev \
  fluid \
  pkg-config

if [ $? -ne 0 ]; then exit 1; fi

mkdir -p ~/Downloads/minetest.org/OldCoder
cd ~/Downloads/minetest.org/OldCoder
wget -O jwm-settings-manager.tar.bz2 http://oldcoder.org/jwm-settings-manager.tar.bz2

tar -xf jwm-settings-manager.tar.bz2

cd jwm-settings-manager
if [ $? -ne 0 ]; then exit 1; fi
mkdir -p bin/Release
cd bin/Release
if [ $? -ne 0 ]; then exit 1; fi
cmake ../..
if [ $? -ne 0 ]; then exit 1; fi
sudo make install
if [ $? -ne 0 ]; then
    echo "Error: make install failed in `pwd`. Ensure you're running as root."
    exit 1;
fi
