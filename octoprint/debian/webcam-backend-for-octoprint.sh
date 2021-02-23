#!/bin/bash
customDie() {
    echo
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
source include/octoprint.rc || customDie "'source include/octoprint.rc' failed in '`pwd`' as $USER"

echo "The scripts named webcam-backend* are only necessary for using a webcam (but not necessary for webcams that already provide an mjpeg stream that OctoPrint can see)"

# See https://community.octoprint.org/t/setting-up-octoprint-on-a-raspberry-pi-running-raspbian/2337

apt update
apt install -y uvcdynctrl
cat <<END
* Installed uvcdynctrl for controlling the webcam parameters such as brightness (see <http://www.linux-commands-examples.com/uvcdynctrl>):

  # Show current setting:
  uvcdynctrl -d /dev/video0 -g "Brightness"

  # Change setting:"
  uvcdynctrl -d /dev/video0 -g "Brightness"

  # List all settings (some are locked down to a certain range of
  # values-- or you'll get unexpected error 22. (Code: 12) ).
  # You may also have to toggle "" to use "" (tested on GUCEE HD92-720P webcam):
  uvcdynctrl -s

NOTE: The subversion package should install git.
If you still can't type the 'git' command successfully after entering the command under the warning, try:
  apt install -y git

WARNING: The backend below would add about 509MB on Debian 10.

  To continue, type:
  apt install -y subversion libjpeg62-turbo-dev imagemagick ffmpeg libv4l-dev cmake


END
usermod -a -G video $UNPRIV_USER

# See https://unix.stackexchange.com/questions/56957/how-to-start-an-application-automatically-on-boot
cat >/etc/systemd/system/mjpeg-streamer.service <<END
[Unit]
Description=mjpeg-streamer service (as $UNPRIV_USER).

[Service]
Type=simple
ExecStart=/bin/bash /home/$UNPRIV_USER/mjpeg-streamer.sh
User=pi
Group=pi

[Install]
WantedBy=multi-user.target
END

systemctl enable mjpeg-streamer

echo "* Now complete setup and generate mjpeg-streamer.sh by running the following script as $UNPRIV_USER:"
echo "  `pwd`/webcam-backend-for-octoprint-nonroot.sh"
echo "  # You must run it as $UNPRIV_USER or the setup will be incomplete."
