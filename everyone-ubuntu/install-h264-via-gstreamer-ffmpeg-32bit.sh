#!/bin/sh
sudo apt-get install gdebi
wget archive.ubuntu.com/ubuntu/pool/universe/g/gstreamer0.10-ffmpeg/gstreamer0.10-ffmpeg_0.10.13-5_i386.deb
sudo gdebi gstreamer0.10-ffmpeg_0.10.13-5_i386.deb

#64-bit only:
#sudo apt-get install gdebi
#wget archive.ubuntu.com/ubuntu/pool/universe/g/gstreamer0.10-ffmpeg/gstreamer0.10-ffmpeg_0.10.13-5_amd64.deb
#sudo gdebi gstreamer0.10-ffmpeg_0.10.13-5_amd64.deb