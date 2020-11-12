#!/bin/bash

# This version will only do 00000.MTS to 00099.MTS.
if [ ! -f "`command -v ffmpegthumbnailer`" ]; then
    echo "This program requires ffmpegthumbnailer."
    echo "such as via:"
    echo "  sudo apt-get install ffmpegthumbnailer"
    echo "  # or"
    echo "  # sudo rpm install ffmpegthumbnailer"
    exit 1
fi
# BASE_DIR=
THUMBS_DIR=~/.thumbnails/linux-preinstall`pwd`
# THUMBS_DIR=`pwd`/thumbs
#Error: Failed to open output file: ....jpg
#- SELinux issue:
#  https://askubuntu.com/questions/895620/ffmpegthumbnailer-error-failed-to-load-gio-libraries-kubuntu-14-04
#  - he says must save to .thumbnails
#  - didn't have to. Moved the script off of the nfs drive to solve it instead.

# Known issues
# - "[h264 @ 0x565282c672c0] co located POCs unavailable"
#   (or other hex code) for MTS videos from Panasonic HDC-TM90

if [ ! -d "$THUMBS_DIR" ]; then mkdir -p "$THUMBS_DIR"; fi
for TENS in `seq 0 9`
do
    for ONES in `seq 0 9`
    do
        I_NOEXT=000$TENS$ONES
        I_NAME=$I_NOEXT.MTS
        if [ -f "$I_NAME" ]; then
            ffmpegthumbnailer -i $I_NAME -o $THUMBS_DIR/$I_NOEXT.jpg
            # -o<s>   : output file
            # -s<n>   : thumbnail size (use 0 for original size) (default: 128)
            # -q<n>   : image quality (0 = bad, 10 = best) (default: 8)
            # -c      : override image format (jpeg, png or rgb) (default: determined by filename)
            # -a      : ignore aspect ratio and generate square thumbnail
            # -f      : create a movie strip overlay
        else
            echo "* no $I_NAME"
        fi
    done
done
