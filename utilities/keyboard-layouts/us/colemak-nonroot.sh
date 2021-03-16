#!/bin/sh
colemak_x_dst="/usr/local/bin/colemak_x.sh"
if [ -f "$colemak_x_dst" ]; then
    sh $colemak_x_dst
else
    echo "* ERROR: missing $colemak_x_dst - run colemak.sh first"
fi
if [ -f "`command -v gsettings`" ]; then
    printf "* setting Gnome to Colemak..."
    gsettings set org.gnome.desktop.input-sources sources "[('xkb','us+colemak')]"
    gsettings set org.gnome.desktop.input-sources sources "[('xkb','us+colemak'),('xkb','us')]"
    if [ $? -eq 0 ]; then
        printf "OK "
    else
        echo "FAILED "
    fi
    gsettings get org.gnome.desktop.input-sources sources
    echo "To have only Colemak available in Gnome, type:"
    echo "  gsettings set org.gnome.desktop.input-sources sources \"[('xkb','us+colemak')]\""
fi
