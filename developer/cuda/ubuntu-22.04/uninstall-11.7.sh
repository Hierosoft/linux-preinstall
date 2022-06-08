#!/bin/bash
cat <<END
A cuda python package for cuda 11.7 is not on PyPi as of June 2022.
Removing 11.7.
END
# As per <https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_local>:
sudo rm /etc/apt/preferences.d/cuda-repository-pin-600
# rm cuda-repo-ubuntu2204-11-7-local_11.7.0-515.43.04-1_amd64.deb
sudo apt-get -y remove cuda
sudo rm /usr/share/keyrings/cuda-*-keyring.gpg 
sudo apt-get remove cuda-repo-ubuntu2204-11-7-local
sudo rm /etc/apt/sources.list.d/cuda-ubuntu2204-11-7-local.list
sudo apt-get update
