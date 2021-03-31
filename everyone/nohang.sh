#!/bin/bash
if [ -f "`command -v dnf`" ]; then
    sudo dnf -y copr enable atim/nohang && sudo dnf -y install nohang-desktop && systemctl enable --now nohang
    exit $?
fi
mkdir -p "/opt/Downloads"
cd "/opt/Downloads"
# ^ It cannot be in $HOME where the _apt user can't access it!
if [ $? -ne 0 ]; then
    echo "Error: 'cd \"/opt/Downloads\"' failed."
    exit 1
fi
if [ ! -d nohang ]; then
    git clone https://github.com/hakavlad/nohang.git nohang
    if [ $? -ne 0 ]; then
        echo "Error: 'git clone https://github.com/hakavlad/nohang.git nohang' failed."
        exit 1
    fi
else
    cd nohang
    if [ $? -ne 0 ]; then
        echo "Error: 'cd nohang' failed."
        exit 1
    fi
    git pull
    if [ $? -ne 0 ]; then
        echo "Warning: 'git pull' failed in \"`pwd`\"."
    fi
fi
deb/build.sh
sudo chown _apt:nogroup ./deb/package.deb
# ^ prevent "N: Download is performed unsandboxed as root as file '/home/owner/Downloads/nohang/deb/package.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)"
sudo apt install --reinstall ./deb/package.deb
sudo systemctl enable --now nohang-desktop.service
