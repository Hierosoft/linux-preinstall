#!/bin/sh
sudo sh -c "echo 'deb http://download.opensuse.org/repositories/isv:/ownCloud:/desktop/xUbuntu_14.04/ /' >> /etc/apt/sources.list.d/owncloud-client.list"
sudo apt-get update

sudo apt-get install -y keepassx owncloud-client mdb-tools mdbtools mdbtools-gmdb libreoffice
#an is a terminal anagram generator (usage: an -w hello)