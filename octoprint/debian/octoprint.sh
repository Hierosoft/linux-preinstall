#!/bin/bash

source include/octoprint.rc || customDie "octoprint.rc must be in the same directory from which you run $0."
if [ -z "$UNPRIV_USER" ]; then
    customDie "You must set UNPRIV_USER in 'octoprint.rc'."
fi
if [ ! -d "/home/$UNPRIV_USER" ]; then
    sudo /usr/sbin/useradd -m -p changeThisPwd1 -s /bin/bash $UNPRIV_USER
fi

apt update
apt -y install python-pip python-dev python-setuptools python-virtualenv git libyaml-dev build-essential
usermod -a -G tty $UNPRIV_USER
usermod -a -G dialout $UNPRIV_USER

disposeTemps() {
    rm "$temps/include/octoprint.rc"
    rm "$temps/include/octoprint-as-pi.sh"
    rmdir "$temps/include"
    rmdir "$temps"
}

temps="/tmp/linux_preinstall_octoprint"
if [ -d "$temps" ]; then
    disposeTemps
fi
mkdir -p $temps/include
tmp_sh=$temps/include/octoprint-as-pi.sh
cp -f "`pwd`/include/octoprint.rc" "$temps/include/"
cp -f "`pwd`/include/octoprint-as-pi.sh" "$temps/include/"
chown -R $UNPRIV_USER "$temps"
chgrp -R $UNPRIV_USER "$temps"
chmod +x "$tmp_sh"
/bin/su -c "$tmp_sh" - pi
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
grep -v "OCTOPRINT_USER=pi" /etc/default/octoprint | grep -v "$OCTOPRINT_USER_comment" > octoprint.default.tmp
echo "# $OCTOPRINT_USER_comment." >> octoprint.default.tmp
echo "OCTOPRINT_USER=$UNPRIV_USER" >> octoprint.default.tmp
mv octoprint.default.tmp /etc/default/octoprint || customDie "'mv octoprint.default.tmp /etc/default/octoprint' failed in `pwd`"
rm octoprint.default || customDie "'rm octoprint.default' failed in `pwd`"
chmod +x /etc/init.d/octoprint
# Usually 'DAEMON=/home/pi/OctoPrint/bin/octoprint':
echo "DAEMON=`pwd`/venv/bin/octoprint" >> /etc/default/octoprint
echo "OCTOPRINT_USER=$UNPRIV_USER" >> /etc/default/octoprint
systemctl enable octoprint
# apt -y install ffmpeg  # not unless your main drive is > 2 GB (adds 391MB, which is approximately all of your remaining space if you have a 2GB drive)
echo
echo "* Next, you must manually set a password for pi by typing:"
echo "  passwd pi"
echo
echo "* You can check the status after reboot by typing any of the following:"
echo "  sudo service octoprint status"
echo "  sudo lsof -i -P -n | grep LISTEN"
echo "  ss -tulw"
