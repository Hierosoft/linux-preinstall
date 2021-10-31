#!/bin/bash
# This script can be run as root or as a sudoer.

# sudo apt-get install -y libpulse-dev libnotify-dev
# REPO_USER=window-maker
# ^ The upstream window-maker copy has problems with wmglobe (Makefile uses 'ld -lungif' but should use 'ld -lgif' on probably most distros)
REPO_USER=poikilos
REPO_NAME=dockapps

# REPO_USER=crmafra
# REPO_URL=https://repo.or.cz/dockapps.git

REPO_URL=https://github.com/$REPO_USER/$REPO_NAME.git

mkdir -p "$HOME/Downloads/git/$REPO_USER"
cd "$HOME/Downloads/git/$REPO_USER"
if [ $? -ne 0 ]; then
    echo "Error: 'cd $HOME/Downloads/git/$REPO_USER' failed."
    exit 1
fi
if [ ! -d "$REPO_NAME" ]; then
    git clone $REPO_URL
    if [ $? -ne 0 ]; then
        echo "Error: 'git clone $REPO_URL' failed in \"`pwd`\"."
        exit 1
    fi
    cd $REPO_NAME
else
    cd $REPO_NAME
    git pull
    if [ $? -ne 0 ]; then
        echo "Warning: 'git pull' failed in \"`pwd`\"."
    fi
fi

MULTI_APPS_DIR="`pwd`"
cat > /dev/null <<END
$ls
AlsaMixer.app	 wmbutton	wmfu	     wmmisc	     wmsupermon
asbeats		 wmcalc		wmget	     wmmixer	     wmswallow
ascd		 wmCalClock	wmglobe      wmmixer-alsa    wmtetris
asmon		 wmcalclockkbd	wmgrabimage  wmmon	     wmthemech
buttonmaker	 wmcalendar	wmgtemp      wmmoonclock     wmthrottle
cnslock		 wmcapshare	wmhdplop     wmmp3	     wmtictactoe
cputnik		 wmcdplay	wmhexaclock  wmnet	     wmtime
fookb		 wmckgmail	wmifinfo     wmomikuzi	     wmtop
libdockapp	 wmcliphist	wmifs	     wmpager	     wmtrash
pclock		 wmclock	wmisdn	     wmpop3	     wmtunlo
Temperature.app  wmcore		wmitime      wmpop3lb	     wmtv
washerdryer	 wmcp		wmix	     wmpower	     wmtz
wmacpi		 wmcpufreq	wmjiface     wmppp.app	     wmusic
wmacpiload	 wmcpuload	wmjmail      wmradio	     wmwebcam
wmail		 wmcube		wmkeys	     wmressel	     wmwifi
wmapm		 wmdonkeymon	wmload	     wmshutdown      wmwlmon
wmappkill	 wmdots		wmlongrun    wmsm.app	     wmwork
wmArchUp	 wmfemon	wmMatrix     wmsmixer	     wmxres
wmbatteries	 wmfortune	wmmemfree    wmSMPmon	     wmxss
wmbattery	 wmframepic	wmmemload    wmspaceweather  wmymail
wmbiff		 wmfsm		wmmenu	     wmsun	     yawmppp
END

cd wmglobe
make
if [ $? -ne 0 ]; then
    cat <<END
- If the error is "src/wmglobe.h:41:10: fatal error: X11/xpm.h: No such file or directory"
  then ensure that the libxpm development library is installed such as:
  - sudo apt-get install -y libxpm-dev # on deb-based distros such as Ubuntu, Debian, or Devuan
  - sudo yum install -y libXpm-devel # on Fedora etc (See https://titanwolf.org/Network/Articles/Article?AID=cf468b4d-aaba-424f-8eeb-2d24e0b8620f#gsc.tab=0)
- If the error is "src/wmglobe.h:48:10: fatal error: wraster.h: No such file or directory"
  then ensure that the wraster development library is installed such as:
  - sudo apt-get install libwraster-dev
- If the error is "/usr/bin/ld: cannot find -lungif"
  (sudo apt-get install -y libgif-dev may be necessary too but doesn't resolve the issue.
  ld -lungif --verbose
  says it is looking for ungif.a and libungif.so
  apt-file search libungif.so
  apt-file search ungif.a
  both show no results.
  autoreconf -fvi
  doesn't do anything ("autoreconf: 'configure.ac' or 'configure.in' is required")
  )
END
    exit 1
fi


installdockapp(){
    if [ "@$1" = "@" ]; then
        echo "Error: The installdockapp function of $0 requires an app name."
        exit 1
    fi
    DA_NAME=$1
    DA_SRC="$MULTI_APPS_DIR/$DA_NAME"
    if [ ! -d "$DA_SRC" ]; then
        echo "Error in installdockapp function in $0: The directory $DA_NAME doensn't exist in the dockapps dir (MULTI_APPS_DIR) $MULTI_APPS_DIR"
        exit 1
    fi
    cd "$DA_SRC"
    if [ $? -ne 0 ]; then
        echo "Error: 'cd $DA_SRC' failed in installdockapp function in $0."
        exit 1
    fi
    ./autogen.sh
    ./configure
    if [ $? -ne 0 ]; then
        echo "Warning: './configure' failed in \"`pwd`\"."
    fi
    make
    if [ $? -ne 0 ]; then
        echo "Warning: 'make' failed in \"`pwd`\"."
    fi
    sudo make install
}

installdockapp wmglobe
