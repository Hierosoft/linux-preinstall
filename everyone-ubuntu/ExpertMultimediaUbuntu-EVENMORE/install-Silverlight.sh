#!/bin/sh
sudo killall firefox
sudo killall chromium
sudo killall chromium-browser
sudo killall chrome
#from http://www.webupd8.org/2014/04/10-things-to-do-after-installing-ubuntu.html
sudo apt-add-repository ppa:pipelight/stable
sudo apt-get update
sudo apt-get install pipelight-multi
sudo pipelight-plugin --enable silverlight
sudo pipelight-plugin --enable widevine


sudo apt-get install chromium-browser
sudo apt-get install pepperflashplugin-nonfree
sudo update-pepperflashplugin-nonfree --install
