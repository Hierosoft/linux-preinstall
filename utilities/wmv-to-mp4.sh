#!/bin/sh
#Known issues:
#* output was 125fps according to flowblade, 640x482 according to vlc, with "display" resolution of 640x480.
cd $HOME/Videos/without-intro

thisvideofolder=converted-mp4
mkdir $thisvideofolder

if [ -z "$1" ]; then
    echo "You must specify a wmv filename."
    exit 1
fi

thisname=$1.wmv
ffmpeg -i "$thisname" -c:v libx264 -crf 18 -c:a aac "$thisvideofolder/${thisname%.wmv}.mp4"
