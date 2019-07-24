#!/bin/sh
sudo sh -c "echo 'deb http://download.opensuse.org/repositories/isv:/ownCloud:/desktop/xUbuntu_14.04/ /' >> /etc/apt/sources.list.d/owncloud-client.list"
sudo apt update

sudo apt install -y keepassx
sudo apt install -y owncloud-client
sudo apt install -y mdb-tools
sudo apt install -y mdbtools
sudo apt install -y mdbtools-gmdb
sudo apt install -y libreoffice
#an is a terminal anagram generator (usage: an -w hello)
