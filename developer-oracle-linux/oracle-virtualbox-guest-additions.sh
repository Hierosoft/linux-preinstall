#!/bin/sh
#http://localhost:5500/em/login
modprobe vboxguest
if [ ! -z "`lsmod | grep vboxguest`" ]; then
    echo "vboxguest is already installed."
    exit 0
fi

customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}

yum -y upgrade
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum install -y gcc kernel-devel kernel-headers dkms make bzip2 perl

KERN_DIR=/usr/src/kernels/`uname -r`
## Current running kernel on CentOS 5 and Red Hat (RHEL) 5 ##
#KERN_DIR=/usr/src/kernels/`uname -r`-`uname -m`
## Fedora example ##
#KERN_DIR=/usr/src/kernels/4.15.6-300.fc27.x86_64/build
## [OLD] CentOS and Red Hat (RHEL) example ##
#KERN_DIR=/usr/src/kernels/3.10.0-693.17.1.el7-x86_64/build
#*VirtualBox Guest Additions on Fedora 30/29, CentOS/RHEL 7.6/6.10/5.11 - If Not True Then False*. https://www.if-not-true-then-false.com/2010/install-virtualbox-guest-additions-on-fedora-centos-red-hat-rhel/. Accessed 26 May 2019.

if [ ! -d "$KERN_DIR" ]; then
    echo 'result of:'
    echo '    rpm -qa kernel | sort -V | tail -n 1'
    echo 'must match result of:'
    echo '    uname -r'
    customDie "Missing $KERN_DIR. Try restarting linux so 'uname -r' matches the kernel-headers install directory."
fi

export KERN_DIR

if [ -d "$HOME/Downloads" ]; then
    mkdir -p "$HOME/Downloads"
fi
cd "$HOME/Downloads"
dl_name="VBoxGuestAdditions_6.0.8.iso"
if [ ! -f "$dl_name" ]; then
    wget -O $dl_name https://download.virtualbox.org/virtualbox/6.0.8/$dl_name
fi
#mnt_iso=/mnt/iso
mnt_iso=$HOME/mnt/iso
if [ ! -d "$mnt_iso" ]; then
    mkdir -p "$mnt_iso"
    #chown $USER "$mnt_iso"
fi
mount -t iso9660 -o loop $HOME/Downloads/$dl_name $mnt_iso
#$mnt_iso/runasroot.sh <file>
$mnt_iso/VBoxLinuxAdditions.run
umount $HOME/Downloads/$dl_name


