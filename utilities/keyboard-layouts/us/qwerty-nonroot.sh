#!/bin/sh
echo "* setting x to Qwerty..."
setxkbmap us
# setxkbmap -model pc104 -layout us

if [ -f "`command -v gsettings`" ]; then
    printf "* setting Gnome to Qwerty..."
    gsettings set org.gnome.desktop.input-sources sources "[('xkb','us')]"
    if [ $? -eq 0 ]; then
        printf "OK "
    else
        echo "FAILED "
    fi
    gsettings get org.gnome.desktop.input-sources sources
fi
