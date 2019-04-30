#!/bin/sh
echo "* setting console to Qwerty..."
# sudo loadkeys us
localectl set-x11-keymap us
localectl set-keymap us

if [ -f "`command -v keyboardctl`" ]; then
    echo "* Manjaro keyboardctl detected, setting system to Qwerty..."
    keyboardctl -l us
fi
