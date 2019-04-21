#!/bin/sh
customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
#USERNAMEDEST=officetv@FBM
if [ -z "$USERNAMEDEST" ]; then
	echo "You must edit this script and set USERNAMEDEST"
    exit 1
fi
cp update-pictures.sh /home/$USERNAMEDEST/Documents
chmod +x /home/$USERNAMEDEST/Documents/update-pictures.sh
cp "Update Pictures Slideshow.desktop" /home/$USERNAMEDEST/Desktop/
cp "Update Pictures Slideshow.desktop" /home/$USERNAMEDEST/.config/autostart
if [ -d "$DIRECTORY" ]; then
	sudo yum erase gnome-screensavers
	sudo wget https://copr.fedorainfracloud.org/coprs/shassard/xscreensaver-epel-7.repo
	sudo mv shassard-xscreensaver-epel-7.repo /etc/yum.repos.d/
	sudo yum install xscreensaver
	#to configure using GUI:
	sudo xscreensaver-demo

	#NOTE: you have to manually:
	#* Set Advanced to Random then choose ~/Pictures/Slideshow
	#* Choose GLSlideshow
	#* Set Zoom&Pan time longer than change picture time.
fi
