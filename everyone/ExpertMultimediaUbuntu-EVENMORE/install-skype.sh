#!/bin/sh

#tar -xjvf skype*
#cd skype*
#sudo chmod a+x skype
#sudo cp skype /usr/bin/
#sudo mkdir /usr/share/skype
#sudo cp * -Rvf /usr/share/skype/
#cp -f skype.desktop ~/Desktop/
#NOTE: the desktop file says Icon=skype.png but should be Icon=/usr/share/skype/icons/SkypeBlue_128x128.png


#THE ABOVE FAILS because of missing libQtDBus.so.4

#so instead (adding partner repo and installing worked fine without doing these commented steps),
#GreyGeek on kubuntuforums.net <https://www.kubuntuforums.net/showthread.php?58107-Skype-error-error-while-loading-shared-libraries-libQtDBus-so-4> says:
#(quoting Julian Taylor <https://bugs.launchpad.net/ubuntu/+source/ia32-libs/+bug/830440/comments/4>
#"'libxss1 and a few other libreries has been removed from ia32libs you need to enable multiarch and install the 32 bit libraries:'"
#echo foreign-architecture i386 | sudo tee /etc/dpkg/dpkg.cfg.d/multiarchsudo
#apt-get install libxss1:i386 libqtcore4:i386 libqt4-dbus:i386
#THEN (or skip the above which may be ok and do this next part only):
sudo sed -i "/^# deb .*partner/ s/^# //" /etc/apt/sources.list 
sudo apt-get update
sudo apt-get install skype
cp skype.desktop ~/Desktop/
