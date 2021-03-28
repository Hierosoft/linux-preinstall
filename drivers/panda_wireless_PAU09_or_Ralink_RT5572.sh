#!/bin/bash

# This script attempts to install:
# Panda Wireless PAU09
# "ID 148f:5572 Ralink Technology, Corp. RT5572 Wireless Adapter"

# The text below and most of the commands other than checks and output are directly from the Panda Wireless user manual for Linux: <http://www.pandawireless.com/download/PWUsersManual4Linux_v1.0s.pdf> as found at <http://www.pandawireless.com/Drivers%20%7C%20Panda%20Wireless.html>.

#Copyright (c) 2010-2013 Panda Wireless, Inc. All rights reserved.
#Fedora Download Link
mkdir -p /opt/Downloads
if [ $? -ne 0 ]; then
    echo "Error: 'mkdir -p opt/Downloads' failed."
    exit 1
fi
VER="2.5.0.3"
DL_NAME=LinuxDriver4Fedora_v$VER.tar.bz2
EX_NAME=LinuxDriver4Fedora_v$VER
DL_PATH=/opt/Downloads/$DL_NAME
DAT_NAME=RT2870STA.dat
DAT_REL=$DAT_NAME
# ^ DAT_REL is relative to EX_PATH
URL="http://www.pandawireless.com/download/$DL_NAME"
if [ ! -f "$DL_PATH" ]; then
    wget -O $DL_PATH $URL
    if [ $? -ne 0 ]; then
        echo "Error: 'wget -O $DL_PATH $URL' failed."
        exit 1
    fi
else
    echo "* using existing \"$DL_PATH\""
fi
cd /opt/Downloads
if [ $? -ne 0 ]; then
    echo "Error: 'cd /opt/Downloads' failed."
    exit 1
fi
EX_PATH="`realpath $EX_NAME`"
if [ $? -ne 0 ]; then
    echo "Error: 'EX_PATH=\"\`realpath $EX_NAME\`\"' failed in \"`pwd`\"."
    exit 1
fi
if [ ! -d "$EX_NAME" ]; then
    tar -xf "$DL_NAME"
    if [ $? -ne 0 ]; then
        echo "Error: 'tar -xf \"$DL_NAME\"' failed in \"`pwd`\"."
        exit 1
    fi
else
    echo "* using existing \"$EX_PATH\""
fi
cd "$EX_PATH"
if [ $? -ne 0 ]; then
    echo "Error: 'cd \"$EX_PATH\"' failed."
    exit 1
fi
#Instructions to compile and install the Linux driver for Panda Wireless N adapter on Fedora
#You need to become the superuser of your machine before you perform the following
#instructions:-
#1) Blacklist RT2800 wireless module in the Linux Kernel
BL=/etc/modprobe.d/blacklist.conf
if [ -f "$BL" ]; then
    if [ -z "`cat $BL | grep "blacklist rt2800usb"`" ]; then
        echo "blacklist rt2800usb" | tee -a $BL
        if [ $? -ne 0 ]; then
            echo "Error: writing to $BL failed. Run as root."
            exit 1
        fi
    else
        echo "* \"$BL\" already contains \"blacklist rt2800usb\" so it will not be added:"
        cat $BL | grep "blacklist rt2800usb"
    fi
else
    echo "Error: $BL is not present, so this script is not compatible with your computer."
    exit 1
fi

#vi blacklist.conf
#Add "blacklist rt2800usb" at the end of the file.
#2) Copy RT2870STA to /etc (RT2870STA.dat is located in your driver install directory)
#$>mkdir -p Wireless/RT2870STA (under /etc directory)
#$>cp RT2870STA.dat /etc/Wireless/RT2870STA/RT2870STA.dat
mkdir -p "/etc/Wireless/RT2870STA"
if [ $? -ne 0 ]; then
    echo "Error: 'mkdir -p \"/etc/Wireless/RT2870STA\"' failed."
fi
DST_DATS=/etc/Wireless/RT2870STA
DST_DAT=$DST_DATS/$DAT_NAME
if [ ! -f "$DST_DAT" ]; then
    cp "$EX_PATH/$DAT_REL" "$DST_DAT"
else
    echo "* using existing \"$DST_DAT\""
fi
if [ $? -ne 0 ]; then
    echo "Error: 'cp \"$EX_PATH/$DAT_REL\" \"/etc/Wireless/RT2870STA/\"' failed."
fi

#3) Create tftpboot directory under root directory
#$> mkdir /tftpboot
mkdir /tftpboot
if [ $? -ne 0 ]; then
    echo "Error: 'mkdir /tftpboot' failed."
fi

#4) Compile the driver for the Panda Wireless N adapter
#$> tar jxvf LinuxDriver4Fedora_v2.5.0.3.tar.bz2
#$> make
if [ ! -f "`command -v flex`" ]; then
    echo "Error: install flex then try again."
fi
if [ ! -f "`command -v bison`" ]; then
    echo "Error: install bison then try again."
fi

make

if [ $? -ne 0 ]; then

    cat <<END

Error: 'make' failed in \"`pwd`\"."

Ensure you have installed:
- kernel-devel
- openssl-devel
  ^ resolve scripts/sign-file.c:25:10: fatal error: openssl/opensslv.h: No such file or directory

TODO:
Resolve remaining issues
(The solution is unknown on Fedora 33)

scripts/Makefile.build:414: warning: overriding recipe for target 'modules.order'
Makefile:1409: warning: ignoring old recipe for target 'modules.order'
. . .
arch/x86/Makefile:125: *** Recursive variable 'KBUILD_CFLAGS' references itself (eventually).  Stop.
make[1]: *** [Makefile:1809: arch/x86] Error 2
make[1]: Leaving directory '/usr/src/kernels/5.11.9-200.fc33.x86_64'
make: *** [Makefile:357: LINUX] Error 2

(LinuxDriver4Fedora_v2.5.0.3, kernel 5.11.9-200.fc33.x86_64)
END
    FORK_REPO="https://github.com/maroviher/DPO_RT5572_LinuxSTA_2.6.1.3_20121022_mod.git"
    REPO_NAME="DPO_RT5572_LinuxSTA_2.6.1.3_20121022_mod"
    echo "* attempting to use a fork at $FORK_REPO"
    mkdir -p "/opt/Downloads/git/maroviher"
    if [ $? -ne 0 ]; then
        echo "Error: 'mkdir -p \"/opt/Downloads/git/maroviher\"' failed."
        exit 1
    fi
    cd "/opt/Downloads/git/maroviher"
    if [ $? -ne 0 ]; then
        echo "Error: 'cd \"/opt/Downloads/git/maroviher\"' failed."
        exit 1
    fi
    if [ -d "$REPO_NAME" ]; then
        cd "$REPO_NAME"
        if [ $? -ne 0 ]; then
            echo "Error: 'cd \"$REPO_NAME\"' failed in \"`pwd`\"."
            exit 1
        fi
        git pull
        if [ $? -ne 0 ]; then
            echo "WARNING: 'git pull' failed in \"`pwd`\"."
        fi
    else
        git clone "$FORK_REPO" "$REPO_NAME"
        if [ $? -ne 0 ]; then
            echo "Error: 'git clone \"$FORK_REPO\" \"$REPO_NAME\"' failed in \"`pwd`\"."
            exit 1
        fi
        cd "$REPO_NAME"
        if [ $? -ne 0 ]; then
            echo "Error: 'cd \"$REPO_NAME\"' failed in \"`pwd`\"."
            exit 1
        fi
    fi
    MAKE_DIR_REL="DPO_RT5572_LinuxSTA_2.6.1.3_20121022"
    cd "$MAKE_DIR_REL"
    if [ $? -ne 0 ]; then
        echo "Error: 'cd \"$MAKE_DIR_REL\"' failed in \"`pwd`\"."
        exit 1
    fi
    DST_DATS=/etc/Wireless/RT2870STA
    DST_DAT=$DST_DATS/$DAT_NAME
    if [ ! -f "$DST_DAT" ]; then
        cp "$EX_PATH/$DAT_REL" "$DST_DAT"
    else
        echo "* using existing \"$DST_DAT\""
    fi
    make
fi
SRC_KO=/tftpboot/rt3070sta.ko
if [ ! -f "$SRC_KO" ]; then
    echo "Error: 'make' in \"pwd\" did not result in $SRC_KO."
    
fi
insmod rt3070sta.ko
ifconfig ra0 inet up
cat <<END

You will find rt3070sta.ko in /tftpboot directory

5) Load driver
$>insmod rt3070sta.ko
$>ifconfig ra0 inet up

6) Unload driver
$>ifconfig ra0 inet down
$>rmmod rt3070sta.ko

Note:
You need to recompile the driver whenever you upgrade your kernel.

END

