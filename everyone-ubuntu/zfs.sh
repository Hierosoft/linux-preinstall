#!/bin/sh
sudo apt-add-repository ppa:zfs-native/stable
sudo apt-get update
sudo apt-get install -y lvm2 ubuntu-zfs
sudo modprobe zfs
#sudo zpool import tank