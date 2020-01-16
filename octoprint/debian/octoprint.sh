#!/bin/bash

# See https://community.octoprint.org/t/setting-up-octoprint-on-a-raspberry-pi-running-raspbian/2337

echo "* $0 should work even if you install Debian netinstall with only the \"standard utilities\"."
source include/octoprint.rc || customDie "octoprint.rc must be in the same directory from which you run $0."
if [ -z "$UNPRIV_USER" ]; then
    customDie "You must set UNPRIV_USER in 'octoprint.rc'."
fi
if [ ! -d "/home/$UNPRIV_USER" ]; then
    # NOTE: setting the password with the -p option will not work unless
    # the password following it is encrypted.  The option is only below
    # to prevent the password from being blank.
    useradd -m -p changeThisPwd1 -s /bin/bash $UNPRIV_USER || customDie "'useradd -m -p changeThisPwd1 -s /bin/bash $UNPRIV_USER' failed as $USER"
fi

apt update
apt install -y openssh-server  # recommended but not part of octoprint instructions
apt install -y python-pip python-dev python-setuptools python-virtualenv git libyaml-dev build-essential || customDie "'apt install -y python-pip python-dev python-setuptools python-virtualenv git libyaml-dev build-essential' failed as $USER"
usermod -a -G tty $UNPRIV_USER
usermod -a -G dialout $UNPRIV_USER


disposeTemps() {
    rm "$temps/include/octoprint.rc"
    rm "$temps/include/octoprint-nonroot-pi.sh"
    rmdir "$temps/include"
    rmdir "$temps"
}


if [ -d "$temps" ]; then
    disposeTemps
fi
mkdir -p $temps/include
tmp_sh=$temps/include/octoprint-nonroot-pi.sh
chmod +x "`pwd`/include/octoprint-nonroot-pi.sh"
cp -f "`pwd`/include/octoprint.rc" "$temps/include/"
cp -f "`pwd`/include/octoprint-nonroot-pi.sh" "$temps/include/"
chown -R $UNPRIV_USER "$temps"
chgrp -R $UNPRIV_USER "$temps"
chmod +x "$tmp_sh"
/bin/su -c "$tmp_sh" - pi
mkdir /home/$UNPRIV_USER/include
mv "$temps/include/octoprint.rc" /home/$UNPRIV_USER/include/
mv "$temps/include/octoprint-nonroot-pi" /home/$UNPRIV_USER/include/
disposeTemps
cd ~
if [ -f "octoprint.init" ]; then
    rm octoprint.init || customDie "'rm octoprint.init' failed in `pwd`"
fi
wget https://github.com/foosel/OctoPrint/raw/master/scripts/octoprint.init  || customDie "'wget https://github.com/foosel/OctoPrint/raw/master/scripts/octoprint.init' failed in `pwd`."
mv octoprint.init /etc/init.d/octoprint || customDie "'mv octoprint.init /etc/init.d/octoprint' failed in `pwd`."
if [ -f "octoprint.default" ]; then
    rm octoprint.default || customDie "'rm octoprint.default' failed in `pwd`"
fi
wget https://github.com/foosel/OctoPrint/raw/master/scripts/octoprint.default || customDie "'wget https://github.com/foosel/OctoPrint/raw/master/scripts/octoprint.default' failed in `pwd`."
OCTOPRINT_USER_comment="The init.d script will only run if this variable non-empty"
grep -v "OCTOPRINT_USER=pi" octoprint.default | grep -v "$OCTOPRINT_USER_comment" > octoprint.default.tmp
echo "" >> octoprint.default.tmp
echo "# $OCTOPRINT_USER_comment." >> octoprint.default.tmp
echo "OCTOPRINT_USER=$UNPRIV_USER" >> octoprint.default.tmp
if [ -f /etc/default/octoprint ]; then
    # Backup if an old copy exists.
    if [ ! -d ~/Backup/etc/default ]; then
    mkdir -p ~/Backup/etc/default
    fi
    if [ ! -f ~/Backup/etc/default/octoprint ]; then
      cp /etc/default/octoprint ~/Backup/etc/default
    fi
fi
mv -f octoprint.default.tmp /etc/default/octoprint || customDie "'mv octoprint.default.tmp /etc/default/octoprint' failed in `pwd`"
rm octoprint.default || customDie "'rm octoprint.default' failed in `pwd`"
chmod +x /etc/init.d/octoprint
# Usually 'DAEMON=/home/pi/OctoPrint/bin/octoprint':
DAEMON_comment="Path to the OctoPrint executable, you need to set this to match your installation"
DAEMON_default="DAEMON=/home/pi/OctoPrint/venv/bin/octoprint"
echo "" >> /etc/default/octoprint
echo "DAEMON=/home/$UNPRIV_USER/OctoPrint/venv/bin/octoprint" >> /etc/default/octoprint
echo "OCTOPRINT_USER=$UNPRIV_USER" >> /etc/default/octoprint
systemctl enable octoprint
# apt -y install ffmpeg  # not unless your main drive is > 2 GB (adds 391MB, which is approximately all of your remaining space if you have a 2GB drive)
echo
echo "* You can check the status after reboot by typing any of the following:"
echo "  service octoprint status"
echo "  sudo lsof -i -P -n | grep LISTEN"
echo "  ss -tulw"
echo "* If the 'service octoprint status' results in 'dead', enable the service:"
echo "  service octoprint enable"
echo "  service octoprint start"
echo "* If 'service octoprint status' still says 'dead' or 'active (exited)', the virtualenv may not have setup automatically. Try:"
echo "  su $UNPRIV_USER"
echo "  cd /home/$UNPRIV_USER/include/"
echo "  ./octoprint-nonroot-pi.sh"
echo "  service octoprint stop"
echo "  service octoprint start"
echo
echo "* Now you must manually set a password for pi by typing:"
echo "  passwd pi"
echo "* Also, you must set the usb device in octoprint by going to http://`hostname -I`:5000 in your browser."
echo "  - Follow the steps to complete setup."
echo "  - Choose a USB or other connection from the connection panel"
echo "  - Choose a fixed Baudrate if necessary for your 3D printer (the baudrate is USUALLY 250000--check with your 3D printer manufacturer!)."
echo "  - For convenience, I suggest checking 'Save connection settings' and 'Auto-connect on server startup' before clicking connect."
echo "* See also: [A Guide To Safe Remote Access of OctoPrint](https://octoprint.org/blog/2018/09/03/safe-remote-access/)"
