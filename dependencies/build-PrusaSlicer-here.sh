#!/bin/bash
# defaults:
# LP_CMAKE_DEBUG=false
# LP_MAKE_THREADS # physical core count minus 1
# This file is based on the PrusaSlicer "Building PrusaSlicer on UNIX/Linux" documentation at
# <https://github.com/prusa3d/PrusaSlicer/blob/master/doc/How%20to%20build%20-%20Linux%20et%20al.md>.
me="`basename $0`"
PRUSASLICER_REPO_DIR="`pwd`"
DEPS_DIR="$PRUSASLICER_REPO_DIR/deps"
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
if [ $? -ne 0 ]; then echo "deps is not in `pwd`. You must run this from the PrusaSlicer repo."; exit 1; fi
mkdir -p build
if [ $? -ne 0 ]; then exit 1; fi
cd build
if [ $? -ne 0 ]; then exit 1; fi
if [ "x$LP_CMAKE_DEBUG" = "x" ]; then
    LP_CMAKE_DEBUG=true
fi
DEBUG_OPTION=""
if [ "x$LP_CMAKE_DEBUG" = "xtrue" ]; then
    DEBUG_OPTION="-DCMAKE_BUILD_TYPE=Debug"
    echo "LP_CMAKE_DEBUG=$LP_CMAKE_DEBUG"
    sleep 1
else
    echo "LP_CMAKE_DEBUG=$LP_CMAKE_DEBUG (!= true)"
fi
# NOTE: "DEBUG" is already in
# - so env DEBUG=true causes a redefinition error in
#   src/avrdude/config.c
cmake .. -DDEP_WX_GTK3=ON
# $DEBUG_OPTION doesn't work above, and documentation
#   (<https://github.com/prusa3d/PrusaSlicer/blob/master/doc/How%20to%20build%20-%20Windows.md>)
#   only says -DDEP_DEBUG=OFF in Visual Studio.
#   There is no mention of dep debug in the linux documentation
#   (<https://github.com/prusa3d/PrusaSlicer/blob/master/doc/How%20to%20build%20-%20Linux%20et%20al.md>).
#   it only says to use the option for "CMake flags when building PrusaSlicer"
if [ $? -ne 0 ]; then >&2 echo "[$me] cmake failed in `pwd`"; exit 1; fi

physical_cores=`grep ^"core id" /proc/cpuinfo | sort -u | wc -l`
if [ "x$LP_MAKE_THREADS" = "x" ]; then
    LP_MAKE_THREADS=$((physical_cores-1))
fi

make -j$LP_MAKE_THREADS
if [ $? -ne 0 ]; then exit 1; fi
# cd ../..
cd "$PRUSASLICER_REPO_DIR"
if [ $? -ne 0 ]; then exit 1; fi

mkdir -p build
if [ $? -ne 0 ]; then exit 1; fi
cd build
if [ $? -ne 0 ]; then exit 1; fi
PROJECT_OPTION_N=""
PROJECT_OPTION_V=""
if [ ! -f "PrusaSlicer.cbp" ]; then
    PROJECT_OPTION_N='-G'
    PROJECT_OPTION_V="CodeBlocks - Unix Makefiles"
else
    >&2 echo "[$me] `pwd`/PrusaSlicer.cbp already exists. Since \"$me\" was called again, cmake will be used without generating a cbp, and then if successful, make will run..."
    sleep 1
fi
lp_cmake_dir="`pwd`"
CMAKE_CMD=
if [ "x$PROJECT_OPTION_V" != "x" ]; then
    cmake .. $PROJECT_OPTION_N "$PROJECT_OPTION_V" $DEBUG_OPTION -DSLIC3R_STATIC=1 -DSLIC3R_GTK=3 -DSLIC3R_PCH=OFF -DCMAKE_PREFIX_PATH=$(pwd)/../deps/build/destdir/usr/local
    code=$?
    CMAKE_CMD="cmake .. $PROJECT_OPTION_N \"$PROJECT_OPTION_V\" $DEBUG_OPTION -DSLIC3R_STATIC=1 -DSLIC3R_GTK=3 -DSLIC3R_PCH=OFF -DCMAKE_PREFIX_PATH=$(pwd)/../deps/build/destdir/usr/local"
else
    cmake .. $DEBUG_OPTION -DSLIC3R_STATIC=1 -DSLIC3R_GTK=3 -DSLIC3R_PCH=OFF -DCMAKE_PREFIX_PATH=$(pwd)/../deps/build/destdir/usr/local
    code=$?
    CMAKE_CMD="cmake .. $DEBUG_OPTION -DSLIC3R_STATIC=1 -DSLIC3R_GTK=3 -DSLIC3R_PCH=OFF -DCMAKE_PREFIX_PATH=$(pwd)/../deps/build/destdir/usr/local"
fi
# cmake .. -DSLIC3R_STATIC=1 -DSLIC3R_GTK=3 -DSLIC3R_PCH=OFF -DCMAKE_PREFIX_PATH=$(pwd)/../deps/build/destdir/usr/local
# code=$?
# ^ or "CodeBlocks - Unix Makefiles" for more (or MinGW Makefiles, or NMake Makefiles, or Ninja)
# ^ Use "Codeblocks - Unix Makefiles" to avoid the error: "Ninja...doesn't match...the generator used previously...Unix Makefiles" after running cmake without CodeBlocks.
if [ $code -ne 0 ]; then >&2 echo "[$me] '$CMAKE_CMD' failed in `pwd`"; exit $code; fi
if [ ! -z "$PROJECT_OPTION" ]; then
    >&2 echo "\nNow you can open the project file in CodeBlocks or run:"
    echo "  make -j$LP_MAKE_THREADS"
    echo "  To avoid Code::Blocks crash (tested on Intel Alder Lake i7-12000F) make sure you set the number of processes to number of physical cores minus 1 (or so):"
    echo "  - In the main menu bar click \"Settings\""
    echo "  - Then click  \"Compiler\", \"Build options\" tab (press right arrow or expand the window if you can't see it)"
    echo "  - Then set \"Number of processes for parallel builds\" to around $LP_MAKE_THREADS (number of physical cores minus 1) or so."
    echo "  - Consider enabling the \"Display build progress bar\" option there since the build takes a while even with i7-12000F."
    exit 0
fi
# make -j$(nproc)
# ^ froze an Intel i7 12000U (ASUS ROG Strix C15 tower)
lp_make_dir="`pwd`"
make -j$LP_MAKE_THREADS
# make -j4
if [ $? -ne 0 ]; then
    >&2 cat <<END

[$me]:
# after cd "$lp_cmake_dir" && $CMAKE_CMD
make failed in `pwd`.
If you don't see an error in red/orange, maybe there was:
- a test failure
- a linker error (usually caused by a mismatched declaration and implementation)
You may want to copy the output to a text editor and search for the word \"error\".
If there is an error regarding make targets, either this script is out of date
or the libraries were built with the wrong option(s) and need to be rebuilt
such as by deleting $DEPS_DIR/build
END

    if [ "$LP_MAKE_THREADS" != "1" ]; then
    cat <<END
To run single-threaded so the log is more clear, try:
env LP_MAKE_THREADS=1 $0
END
    echo
    fi
    exit 1
fi


cd src
>&2 echo "Running `realpath ./prusa-slicer`"
if [ "x$LP_CMAKE_DEBUG" = "xtrue" ]; then
    echo "When using gdb and the program crashes (such as Segfault), type bt, enter for a backtrace."
    gdb -ex run ./prusa-slicer
    if [ $? -ne 0 ]; then
        echo "If you are on macOS, you don't have the -ex option. Debug as follows:"
        echo "gdb `pwd`/prusa-slicer"
        echo "# Then type run, then press enter. If there is a crash, type bt, enter for a backtrace."
    fi
else
    ./prusa-slicer
fi
>&2 cat <<END
Done running:
cd $lp_cmake_dir
$CMAKE_CMD
cd $lp_make_dir
make -j$LP_MAKE_THREADS
`realpath ./prusa-slicer`
END
