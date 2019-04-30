#!/bin/sh
echo "* setting x to Qwerty..."
setxkbmap us
#setxkbmap -model pc104 -layout us
echo "* setting console to Qwerty..."
# sudo loadkeys us
sudo localectl set-x11-keymap us
sudo localectl set-keymap us
