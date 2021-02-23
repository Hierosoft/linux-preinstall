#!/bin/bash
# ^ bash is required for source
source /etc/os-release
if [ $? -ne 0 ]; then
    echo "source /etc/os-release failed. Try using bash (or install the \"source\" command some other way)."
    exit 1
fi
wget -q -O - http://archive.getdeb.net/getdeb-archive.key | sudo apt-key add -
sudo sh -c 'echo "deb http://archive.getdeb.net/ubuntu $UBUNTU_CODENAME-getdeb games" >> /etc/apt/sources.list.d/getdeb.list'
sudo apt-get update
sudo apt-get install ufoai
