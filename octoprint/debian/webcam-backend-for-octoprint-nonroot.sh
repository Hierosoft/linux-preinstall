#!/bin/bash
# See https://community.octoprint.org/t/setting-up-octoprint-on-a-raspberry-pi-running-raspbian/2337
# but don't put ./ before *.so or OS won't find the so files unless they are in the current directory (even if you set LD_LIBRARY_PATH)!
cd ~
git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
export LD_LIBRARY_PATH=`pwd`
make


echo "* $USER should already be in the video group, so the user should be able to run one of the following successfully:"
cat <<END
   # if you don't specify -r, the inpub driver will try the default
   # resolution of 640x480, which may not work with your camera.
   LD_LIBRARY_PATH=`pwd` `pwd`/mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 1280x720" -o "output_http.so"
END
cat > ~/mjpeg-streamer.sh <<END
#!/bin/sh
LD_LIBRARY_PATH=`pwd` `pwd`/mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 1280x720" -o "output_http.so"
END
# Do `u+x` instead of `x` below so only the current user can execute it (only that would work anyway unless you run it as root, which is not recommended):
chmod u+x ~/mjpeg-streamer.sh
chmod g+x ~/mjpeg-streamer.sh
echo
echo "* You must now manually:"
echo "  - Open OctoPrint (Such as http://`hostname -I`:5000 in a browser)"
echo "  - Go to settings (the wrench symbol), then Webcam & Timelapse."
echo "  - Set:"
echo "    - Stream URL: http://127.0.0.1:8080/?action=stream"
echo "      - You may need http://`hostname -I`:8080/?action=stream"
echo "      - formerly: /webcam/?action=stream"
echo "    - Snapshot URL: http://127.0.0.1:8080/?action=snapshot"
echo "    - Path to FFMPEG: /usr/bin/ffmpeg"
echo
echo "* If your webcam doesn't natively support MJPEG, converting can strain your CPU and cause reduced print quality. See https://github.com/foosel/OctoPrint/wiki/Webcams-known-to-work (as noted by https://community.octoprint.org/t/setting-up-octoprint-on-a-raspberry-pi-running-raspbian/2337)"
