#!/bin/sh
echo "* setting console to QWERTY..."
# sudo loadkeys us
localectl set-x11-keymap us
localectl set-keymap us

if [ -f "`command -v keyboardctl`" ]; then
    echo "* Manjaro keyboardctl detected, setting system to Qwerty..."
    keyboardctl -l us
fi

kb_conf="/etc/X11/xorg.conf.d/00-keyboard.conf"
printf "  * Checking $kb_conf..."
line=
if [ -f "$kb_conf" ]; then
    line="`cat $kb_conf | grep colemak`"
fi
if [ -z "$line" ]; then
    echo "OK ($kb_conf does not contain a colemak setting)"
else
    echo "$kb_conf contains a colemak setting."
    echo "    You must remove it manually."
    echo
fi

printf "* checking for x autostart for all users..."
colemak_desktop_dst="/etc/xdg/autostart/colemak_x.desktop"
if [ -f "$colemak_desktop_dst" ]; then
    echo "found $colemak_desktop_dst:"
    cat "$colemak_desktop_dst"
    echo "END"
    echo
    printf "  * removing \"$colemak_desktop_dst\"..."
    rm "$colemak_desktop_dst"
    if [ $? -eq 0 ]; then
        echo "OK"
    else
        echo "FAILED"
    fi
fi

if [ -f "`command -v keyboardctl`" ]; then
    echo "  * Manjaro keyboardctl was detected."
    echo "    * setting system to QWERTY..."
    keyboardctl -l us qwerty
elif [ ! -z "$ID_LIKE" ]; then
    if [[ $ID_LIKE == *arch* ]]; then
        cat <<END
On Arch-based distros, alternate TTYs may not respect '$kb_conf',
so you may need to check respective forums for any solutions.

This script can use Manjaro keyboardctl when present but it was not.

END
    fi
fi

