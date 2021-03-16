#!/bin/sh
echo "* setting x to Qwerty..."
setxkbmap us
# setxkbmap -model pc104 -layout us

if [ -f "`command -v gsettings`" ]; then
    echo "* setting Gnome to Qwerty..."
    gsettings set org.gnome.desktop.input-sources sources "[('xkb','us')]"
fi
