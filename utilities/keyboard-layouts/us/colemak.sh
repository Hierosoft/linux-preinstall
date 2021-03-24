#!/bin/bash
# not  ! / b i n / s h:
# ^ - Using sh makes `source` fail on Debian
#   - On Ubuntu, dash shell doesn't support `source`.

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_DIR="../../.."
FLAG_SUB="utilities/keyboard-layouts"
echo "* Detecting linux-preinstall layouts..."
if [ ! -d "$REPO_DIR/$FLAG_SUB" ]; then
    echo "  * The layouts directory is not \"$REPO_DIR/$FLAG_SUB\"..."
    for try_layouts in "$HOME/git/linux-preinstall/utilities/keyboard-layouts" "./linux-preinstall/utilities/keyboard-layouts" "./linux-preinstall/utilities/keyboard-layouts" "$MY_DIR/.."
    do
        if [ -d "$try_layouts/$FLAG_SUB" ]; then
            layouts="$try_layouts/$FLAG_SUB"
            echo "  * The layouts directory is \"$try_layouts\"."
            break
        else
            echo "  * The layouts directory is not \"$try_layouts\"..."
        fi
    done
fi
layouts="$REPO_DIR/$FLAG_SUB"

echo "* adding Colemak for command line interface:"

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

# --no-convert
#            If set-keymap or set-x11-keymap is invoked and this option is passed, then the keymap will not be
#            converted from the console to X11, or X11 to console, respectively.
# from <https://www.linux.org/docs/man1/localectl.html>

printf "    * Checking $kb_conf..."
kb_conf="/etc/X11/xorg.conf.d/00-keyboard.conf"
line=
if [ -f "$kb_conf" ]; then
    line="`cat $kb_conf | grep colemak`"
fi
if [ -z "$line" ]; then
    localectl set-x11-keymap us pc104 colemak
    echo "OK (set temporarily since not present in conf)"
else
    echo "OK ($kb_conf already contains a colemak setting, skipping)"
fi
# check result via:
# cat /etc/X11/xorg.conf.d/00-keyboard.conf


echo "  * adding x11 Colemak startup setting..."
# setxkbmap -model pc104 -layout cz,us -variant ,dvorak -option grp:alt_shift_toggle
# localectl set-keymap --no-convert us-colemak
# localectl set-keymap --no-convert us-colemak
# 101 + Super keys = 104
# colemak_x_cmd="setxkbmap -model pc104 -layout us -variant colemak"
# colemak_x_cmd="setxkbmap us -variant colemak"
#try_layouts="$HOME/git/linux-preinstall/utilities/keyboard-layouts"
#if [ ! -d "try_layouts" ]; then
#fi

if [ ! -d "$layouts" ]; then
    echo
    echo
    echo "Error:"
    echo "The keyboard-layouts directory is not $layouts nor any known location such as \"..\"."
    echo
    exit 1
else
    echo "* Using layouts directory \"$layouts\"..."
fi

colemak_x_src="$layouts/us/bin/colemak_x.sh"
colemak_x_dst="/usr/local/bin/colemak_x.sh"
echo "* Running \"$colemak_x_src\"..."
sh $colemak_x_src
if [ ! -f "$colemak_x_dst" ]; then
    if [ -f "$colemak_x_src" ]; then
        cp -f "$colemak_x_src" "$colemak_x_dst"
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
        cp -f "$colemak_desktop_src" "$colemak_desktop_dst"
         chmod 644 "$colemak_desktop_dst"
    else
        echo "    - ERROR: missing $colemak_desktop_src"
    fi
else
    echo "    - $colemak_desktop_dst - is already present, skipping"
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

END

source /etc/os-release
if [ -f "`command -v keyboardctl`" ]; then
    echo "  * Manjaro keyboardctl was detected."
    echo "    * setting system to Colemak..."
    keyboardctl -l us colemak
elif [ ! -z "$ID_LIKE" ]; then
    if [[ $ID_LIKE == *arch* ]]; then
        cat <<END
On Arch-based distros, alternate TTYs may not respect '$kb_conf',
so you may need to check respective forums for any solutions.

This script can use Manjaro keyboardctl when present but it was not.

END
    fi
fi

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
    #cp -f "$HOME/Download/$colemak_unz/$colemak_map_rel" "$colemak_map_dst"
#fi
#loadkeys -b "$colemak_map_dst" || echo "* Loading '$colemak_map_dst' failed."
## WARNING: If the command above fails, it resets the x11 layout to Qwerty!
echo "* Next, you must install xdotool to ensure that the UN-CAPSLOCK script works when alternatives are not available to the Python script."
echo "Done."
echo
echo
