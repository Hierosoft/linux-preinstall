#!/bin/sh
# See <https://www.qemu.org/download/#linux>
PRETTY_NAME=
ID=
DISTRO_FAMILY=

if [ -f "/etc/os-release" ]; then
    . /etc/os-release
    DISTRO_FAMILY="$ID"
    if [ "@$ID" = "@centos" ]; then
        DISTRO_FAMILY="redhat"
    elif [ "@ID" = "devuan" ]; then
        DISTRO_FAMILY="debian"
    fi
elif [ -f "/etc/centos-release" ]; then
    # os-release also sets these on centos, so this probably isn't important.
    PRETTY_NAME="`cat /etc/centos-release`"
    ID="centos"
    DISTRO_FAMILY="redhat"
elif [ -f "/etc/redhat-release" ]; then
    DISTRO_FAMILY="redhat"
    ID="redhat"
    PRETTY_NAME="`cat /etc/redhat-release`"
fi

echo "Detected OS:"
echo "  ID: $ID"
echo "  PRETTY_NAME: $PRETTY_NAME"
echo "  DISTRO_FAMILY: $DISTRO_FAMILY"



if [ -f "`command -v dnf`" ]; then
    # dnf install -y qemu virt-manager
    dnf install -y @virtualization
# elif [ -f "`command -v yum`" ]; then
elif [ "@$DISTRO_FAMILY" = "@redhat" ]; then
    # yum install -y qemu virt-manager
    yum install -y qemu-kvm
elif [ -f "`command -v apt`" ]; then
    # apt install -y qemu virt-manager qemu-system-x86
    apt install -y qemu
elif [ -f "`command -v apt-get`" ]; then
    # apt-get install -y qemu virt-manager qemu-system-x86
    apt-get install -y qemu
elif [ -f "`command -v emerge`" ]; then
    emerge --ask app-emulation/qemu
elif [ -f "`command -v pacman`" ]; then
    pacman -S qemu
elif [ -f "`zypper`" ]; then
    zypper install qemu
else
    echo "Your package manager isn't implemented in $0. Install qemu manually (You will probably also have to install qemu-system-x86)."
    exit 1
fi
