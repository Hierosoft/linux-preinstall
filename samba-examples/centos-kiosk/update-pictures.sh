#!/bin/sh
#mkdir ~/h

customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
#gnautilus smb://fcafiles/Home/officetv
#smbmount //fcafiles/ samba/ -o rw
#mkdir ~/Pictures/Slideshow
#cp smb://fcafiles/Home/officetv/Slideshow ~/Pictures/
#cp ~/h/Slideshow ~/Pictures/
#HOMEDIRS=//fcafiles/Home
if [ -z "$HOMEDIRS" ]; then
	echo "You must edit this script and set HOMEDIRS"
    exit 1
fi

#USERNAMEDEST=officetv@FBM
if [ -z "$USERNAMEDEST" ]; then
	echo "You must edit this script and set USERNAMEDEST"
    exit 1
fi
#HOMEDIR=officetv
if [ -z "$HOMEDIR" ]; then
	echo "You must edit this script and set HOMEDIR"
    exit 1
fi

if [ -z "$password" ]; then
    echo "You must edit this script and set the password!"
fi
TARGET=~/Pictures/Slideshow
mkdir "$TARGET"
cd "$TARGET"
rm "$TARGET/*"

#smbclient commands (used after -c, semicolon separated):
#prompt: turns off interactive mode & assumes yes to prompts
pkg install samba-smbclient

smbclient $HOMEDIRS $password -c "cd $HOMEDIR\Slideshow; prompt; mget *.* /home/$USERNAMEDEST/Pictures/" || customDie "You must add $USERNAMEDEST to the server and to CentOS users, create the directory $HOMEDIR/Slideshow in $HOMEDIRS, and ensure that /home/$USERNAMEDEST/Pictures/ exists."
rm "$TARGET/Thumbs.db"
