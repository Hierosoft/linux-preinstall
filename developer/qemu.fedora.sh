#!/bin/sh
if [ -f "`command -v dnf`" ]; then
    dnf install -y qemu virt-manager
elif [ -f "`command -v yum`" ]; then
    yum install -y qemu virt-manager
elif [ if "`command -v apt`" ]; then
    apt install -y qemu virt-manager qemu-system-x86
else
    echo "Your package manager isn't implemented in $0. Install qemu manually (You will probably also have to install qemu-system-x86)."
    exit 1
fi
