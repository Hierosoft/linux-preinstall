#!/bin/sh
colemak_x_dst="/usr/local/bin/colemak_x.sh"
if [ -f "$colemak_x_dst" ]; then
    sh $colemak_x_dst
else
    echo "* ERROR: missing $colemak_x_dst - run colemak.sh first"
fi
gsettings set org.gnome.desktop.input-sources sources "[('xkb','us+colemak'),('xkb','us')]"
