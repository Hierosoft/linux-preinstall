#!/bin/sh
echo "Console:"

# localectl subcommands:

# $ localectl list-x11-keymap-models
# ...
# pc101
# pc102
# pc104
# pc105
# ...

# $ localectl list-x11-keymap-variants
# ...
# colemak
# ...

# $ localectl list-x11-keymap-layouts
# ...
# us
# ...

# $ localectl list-locales
# ...
# en_US
# en_US.iso88591
# en_US.iso885915
# en_US.utf8
# ...

# set-x11-keymap LAYOUT [MODEL [VARIANT [OPTIONS]]]

echo "* settings console to Colemak..."
kb_conf="/etc/X11/xorg.conf.d/00-keyboard.conf"
line=
if [ -f "$kb_conf" ]; then
    line="`cat $kb_conf | grep colemak`"
fi
if [ -z "$line" ]; then
    sudo localectl set-x11-keymap us pc104 colemak
else
    echo "  - $kb_conf already contains a colemak setting, skipping"
fi
# check result via:
# cat /etc/X11/xorg.conf.d/00-keyboard.conf


echo "* adding x11 Colemak startup setting..."
# setxkbmap -model pc104 -layout cz,us -variant ,dvorak -option grp:alt_shift_toggle
# sudo localectl set-keymap --no-convert us-colemak
# sudo localectl set-keymap --no-convert us-colemak
# 101 + Super keys = 104
# colemak_x_cmd="setxkbmap -model pc104 -layout us -variant colemak"
# colemak_x_cmd="setxkbmap us -variant colemak"
try_layouts="$HOME/git/linux-preinstall/utilities/keyboard-layouts"
layouts=..
if [ -d "$try_layouts" ]; then
    layouts="$try_layouts"
fi
colemak_x_src="$layouts/us/bin/colemak_x.sh"
colemak_x_dst="/usr/local/bin/colemak_x.sh"
sh $colemak_x_src
if [ ! -f "$colemak_x_dst" ]; then
    if [ -f "$colemak_x_src" ]; then
        sudo cp -f "$colemak_x_src" "$colemak_x_dst"
    else
        echo "  - ERROR: missing $colemak_x_src"
    fi
else
    echo "  - $colemak_x_dst - is already present, skipping"
fi
colemak_desktop_src="$layouts/us/etc/xdg/autostart/colemak_x.desktop"
colemak_desktop_dst="/etc/xdg/autostart/colemak_x.desktop"
if [ ! -f "$colemak_desktop_dst" ]; then
    if [ -f "$colemak_desktop_src" ]; then
        sudo cp -f "$colemak_desktop_src" "$colemak_desktop_dst"
        sudo chmod 644 "$colemak_desktop_dst"
    else
        echo "  - ERROR: missing $colemak_desktop_src"
    fi
else
    echo "  - $colemak_desktop_dst - is already present, skipping"
fi

cat <<END

If you use GNOME, manual steps are needed
to prevent GNOME settings daemon from changing the settings back when
switching back to the GUI (even though they are set on each startup):
- Run:
  ./colemak-nonroot.sh
- Using the top bar of GNOME, click "en" and choose "Colemak"

For changes to '$kb_conf'
to be applied to TTYs and GUI login, you must reboot.

On Arch-based distros, alternate TTYs may not respect '$kb_conf',
so you may need to check respective forums for any solutions.

END

# below doesn't work on Fedora 29:
#colemak_arc=colemak-1.0.tar.gz
#colemak_unz=colemak-1.0
#colemak_map=colemak.iso15.kmap
#colemak_map_rel="linux_console/$colemak_map"
#colemak_map_dst="/etc/$colemak_map"
#if [ ! -f "$colemak_map_dst" ]; then
    #if [ ! -d "$HOME/Download" ]; then
        #mkdir "$HOME/Download"
    #fi
    #if [ ! -d "$HOME/Download/$colemak_unz" ]; then
        #if [ ! -f "$HOME/Download/$colemak_arc" ]; then
            #wget -O "$HOME/Download/$colemak_arc" https://colemak.com/pub/unix/colemak-1.0.tar.gz
        #fi
        #pushd "$HOME/Download"
        #tar xzf "$HOME/Download/$colemak_arc"
        #popd
    #fi
    #sudo cp -f "$HOME/Download/$colemak_unz/$colemak_map_rel" "$colemak_map_dst"
#fi
#sudo loadkeys -b "$colemak_map_dst" || echo "* Loading '$colemak_map_dst' failed."
## WARNING: If the command above fails, it resets the x11 layout to Qwerty!
