#!/bin/sh

#from http://www.webupd8.org/2014/04/10-things-to-do-after-installing-ubuntu.html
sudo add-apt-repository ppa:mc3man/trusty-media
sudo apt-get update
sudo apt-get install gstreamer0.10-ffmpeg

#The following produces an ERROR: Cannot satisfy dependency
#sudo apt-get install gdebi
#wget archive.ubuntu.com/ubuntu/pool/universe/g/gstreamer0.10-ffmpeg/gstreamer0.10-ffmpeg_0.10.13-5_i386.deb
#sudo gdebi gstreamer0.10-ffmpeg_0.10.13-5_i386.deb

#64-bit only:
#sudo apt-get install gdebi
#wget archive.ubuntu.com/ubuntu/pool/universe/g/gstreamer0.10-ffmpeg/gstreamer0.10-ffmpeg_0.10.13-5_amd64.deb
#sudo gdebi gstreamer0.10-ffmpeg_0.10.13-5_amd64.deb
