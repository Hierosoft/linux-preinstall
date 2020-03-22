#!/bin/bash
dnf -y remove lmms
# See <https://github.com/LMMS/lmms/wiki/dependencies-fedora>
dnf -y install \
    git \
    qt5-devel \
    qt5-qtbase-private-devel \
    libsndfile-devel \
    fftw3-devel \
    libvorbis-devel \
    libsamplerate-devel \
    libogg-devel \
    stk-devel \
    fltk-devel fltk-fluid \
    fluidsynth-devel \
    alsa-lib-devel \
    pulseaudio-libs-devel \
    gcc-c++ xcb-util-devel \
    xcb-util-keysyms-devel \
    wine.i686 wine-devel.i686 \
    glibc-devel.i686 \
    perl-List-MoreUtils \
    || echo "Not all dependencies installed correctly.\n\n" && exit 1

# Compiling on Fedora 31 still says:
#-- Checking for module 'carla-native-plugin'
#--   Package 'carla-native-plugin', required by 'virtual:world', not found
#-- Checking for module 'carla-standalone>=1.9.5'
#--   Package 'carla-standalone', required by 'virtual:world', not found
#-- Checking for module 'carla-native-plugin'
#--   Package 'carla-native-plugin', required by 'virtual:world', not found
#-- Checking for module 'carla-standalone>=1.9.5'
#--   Package 'carla-standalone', required by 'virtual:world', not found
#-- Checking for module 'jack>=0.77'
#--   Package 'jack', required by 'virtual:world', not found
#-- Found FFTW: /usr/include
#  OpenGL_GL_PREFERENCE has not been set to "GLVND" or "LEGACY", so for
#  compatibility with CMake 3.10 and below the legacy GL library will be used.
#-- Checking for module 'gig'
#--   Package 'gig', required by 'virtual:world', not found
#-- Looking for sio_open in sndio
#-- Looking for sio_open in sndio - not found

# Fedora 31 has no: jack, libjack, libjack-devel, jack-devel, gig, libgig

dnf -y install lame-devel

