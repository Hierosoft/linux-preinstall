#!/bin/sh
echo "xset s 0 0"
xset s 0 0

cat <<END

If your screen still locks, you may have to uncheck "Lock Screen After"
using the "Change screensaver properties" application:
  xscreensaver-demo

If screen locks after that, you can try adding the following to the
ServerOptions section of /etc/X11/xorg.conf:
    Option          "BlankTime"     "0"
    Option          "StandbyTime"   "0"
    Option          "SuspendTime"   "0"
    Option          "OffTime"       "0"

END

echo "See also https://askubuntu.com/questions/544818/how-do-i-disable-automatic-screen-locking-in-xubuntu/1125935#1125935"
echo
echo
