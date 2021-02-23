#!/bin/sh
#get Wine 1.7 on Trusty (ships with 1.6 or so)
sudo apt-add-repository ppa:joe-yasi/yasi
sudo apt-add-repository ppa:ubuntu-wine/ppa
sudo apt-get update
sudo apt-get install wine1.7 winetricks
