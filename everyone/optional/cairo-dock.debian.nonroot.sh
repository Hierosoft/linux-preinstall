#!/bin/bash
me=cairo-dock.debian.nonroot.sh
mkdir -p ~/.config/autostart
# cairo_dock_line="cairo-dock &"
cairo_dock_line="cairo-dock -w 5 >& ~/cairo-dock.log &"
#if [ -f "`command -v nohup`" ]; then
#    cairo_dock_line="nohup cairo-dock >& $HOME/cairo-dock.log &"
#    echo "* using nohup for '$cairo_dock_line'..."
#else
#    echo "* nohup is not available, so the output of $cairo_dock_line will not be logged."
#fi
#compositor_line="$compositor --replace &"
if [ ! -z "$1" ]; then
    DIR_HANDLER="$1"
    echo "* detected first param. Set DIR_HANDLER to $DIR_HANDLER."
fi

if [ ! -z "$2" ]; then
    COMPOSITOR="$2"
    echo "* detected first param. Set COMPOSITOR to $COMPOSITOR."
fi


TRY_THUNAR="/usr/share/applications/$DIR_HANDLER"
TRY_NEMO="/usr/share/applications/nemo.desktop"
if [ -z "$DIR_HANDLER" ]; then
    if [ "$XDG_CURRENT_DESKTOP" = "LXDE" ]; then
        DIR_HANDLER=pcmanfm.desktop
        echo "* using $DIR_HANDLER for DIR_HANDLER since XDG_CURRENT_DESKTOP is $XDG_CURRENT_DESKTOP"
    elif [ "$XDG_CURRENT_DESKTOP" = "X-Cinnamon" ]; then
        DIR_HANDLER=nemo.desktop
        echo "* using $DIR_HANDLER for DIR_HANDLER since XDG_CURRENT_DESKTOP is $XDG_CURRENT_DESKTOP"
    elif [ "$XDG_CURRENT_DESKTOP" = "MATE" ]; then
        # DIR_HANDLER=caja.desktop
        DIR_HANDLER=caja-folder-handler.desktop
        echo "* using $DIR_HANDLER for DIR_HANDLER since XDG_CURRENT_DESKTOP is $XDG_CURRENT_DESKTOP"
    elif [ "$XDG_CURRENT_DESKTOP" = "XFCE" ]; then
        DIR_HANDLER=Thunar-folder-handler.desktop
    elif [ "$XDG_CURRENT_DESKTOP" = "LXQt" ]; then
        DIR_HANDLER=pcmanfm-qt.desktop
        if [ -f "$TRY_THUNAR" ]; then
            DIR_HANDLER=Thunar-folder-handler.desktop
            cat <<END
* DIR_HANDLER will be $DIR_HANDLER since XDG_CURRENT_DESKTOP is
  $XDG_CURRENT_DESKTOP but you have $TRY_THUNAR and therefore you seem
  to prefer it. To override this, set the DIR_HANDLER environment
  variable or the first argument such as via:
    ./$me Thunar-folder-handler.desktop $2
END
        else
            cat <<END
* using $DIR_HANDLER for DIR_HANDLER since XDG_CURRENT_DESKTOP is
  $XDG_CURRENT_DESKTOP and $TRY_THUNAR doesn't exist
END
        fi
    elif [ "$XDG_CURRENT_DESKTOP" = "GNOME" ]; then
        DIR_HANDLER=org.gnome.Nautilus.desktop
        if [ -f "$TRY_NEMO" ]; then
            DIR_HANDLER=nemo.desktop
            cat <<END
* DIR_HANDLER will be $DIR_HANDLER since XDG_CURRENT_DESKTOP is
  $XDG_CURRENT_DESKTOP but you have $TRY_THUNAR and therefore you seem
  to prefer it. To override this, set the DIR_HANDLER environment
  variable or the first argument such as via:
    ./$me org.gnome.Nautilus.desktop $2
END
        else
            cat <<END
* using $DIR_HANDLER for DIR_HANDLER since XDG_CURRENT_DESKTOP is
  $XDG_CURRENT_DESKTOP and $TRY_THUNAR doesn't exist
END
        fi
    else
        cat<<END

Error: This script's DIR_HANDLER cases don't account for $XDG_CURRENT_DESKTOP as
XDG_CURRENT_DESKTOP, so DIR_HANDLER cannot be detected. Try setting
the DIR_HANDLER environment variable or the first argument such as
via:
  ./$me Thunar-folder-handler.desktop $2

END
        exit 1
    fi
fi
COMPOSITOR_IS_ON=
COMPOSITOR_IS_ON_LINE="gsettings get org.mate.Marco.general compositing-manager"
if [ -z "$COMPOSITOR_IS_ON_BY_DEFAULT" ]; then
    COMPOSITOR_IS_ON_BY_DEFAULT=false
    if [ "$XDG_CURRENT_DESKTOP" = "X-Cinnamon" ]; then
        COMPOSITOR_IS_ON_BY_DEFAULT=true
    elif [ "$XDG_CURRENT_DESKTOP" = "GNOME" ]; then
        COMPOSITOR_IS_ON_LINE="# <https://askubuntu.com/questions/80578/is-there-a-settings-manager-available-for-mutter>"
        COMPOSITOR_IS_ON=" compositing is always on in mutter."
        COMPOSITOR_IS_ON_BY_DEFAULT=true
        # COMPOSITOR=metacity
        # ^ metacity is only for GNOME 2, mutter is for 3
        # COMPOSITOR=mutter
    elif [ "$XDG_CURRENT_DESKTOP" = "MATE" ]; then
        COMPOSITOR_IS_ON="`gsettings get org.mate.Marco.general compositing-manager`"
        if [ $? -ne 0 ]; then
            cat <<END
Error: This script requires gsettings when it detects MATE but
'gsettings get org.mate.Marco.general compositing-manager'
failed. Try setting:
  COMPOSITOR_IS_ON_BY_DEFAULT=true
  # or
  COMPOSITOR_IS_ON_BY_DEFAULT=false
in the environment then run this script again if you are sure whether
compositing is enabled.
END
            exit 1
        fi
        if [ "@$COMPOSITOR_IS_ON" = "@true" ]; then
            COMPOSITOR_IS_ON_BY_DEFAULT=true
        # elif [ "@$COMPOSITOR_IS_ON" = "@false" ]; then
        else
            COMPOSITOR_IS_ON_BY_DEFAULT=false
cat <<END
Error:
The value for
  gsettings get org.mate.Marco.general compositing-manager
is \"$COMPOSITOR_IS_ON_BY_DEFAULT\", but you should probably use
XDG_CURRENT_DESKTOP's compositor. Try running:
  gsettings get org.mate.Marco.general compositing-manager true
and then running this script again.
Otherwise, run this script with the environment variable:
  COMPOSITOR_IS_ON_BY_DEFAULT=true
if you are sure that a compositor is running.
END
            exit 1
        fi
    fi
fi

if [ -z "$COMPOSITOR" ]; then
    if [ "$XDG_CURRENT_DESKTOP" = "LXQt" ]; then
        COMPOSITOR=compton
        if [ ! -f "`command -v compton`" ]; then
            cat <<END

Error: Your XDG_CURRENT_DESKTOP is $XDG_CURRENT_DESKTOP so you must
first install compton before running this script.

To override detection, use the COMPOSITOR environment variable before
running this script or set the second argument to override that such as
via:

  ./$me $1 mutter
  # or if your compositor runs automatically and you don't it scripted:
  # ./$me $1 none

END
            exit 1
        fi
        echo "* using $COMPOSITOR as COMPOSITOR since XDG_CURRENT_DESKTOP is $XDG_CURRENT_DESKTOP"
    elif [ "@$COMPOSITOR_IS_ON_BY_DEFAULT" = "@true" ]; then
        COMPOSITOR=none
        cat <<END
* Setting COMPOSITOR to "$COMPOSITOR" since you are using
  $XDG_CURRENT_DESKTOP for XDG_CURRENT_DESKTOP
END
        if [ -z "COMPOSITOR_IS_ON" ]; then
            cat <<END
  and that usually runs
  its own (compositing is enabled by default--if you get a black
  outline around cairo-dock, you'll have to enable compositing manually
  then log out or restart cairo-dock).
END
        else
            echo "  and:"
            echo "    $COMPOSITOR_IS_ON_LINE"
            echo "  said: $COMPOSITOR_IS_ON"
        fi
    elif [ -f "`command -v compiz`" ]; then
        COMPOSITOR=compiz
        cat <<END
* You have compiz installed and $XDG_CURRENT_DESKTOP for
  XDG_CURRENT_DESKTOP isn't handled by this script's COMPOSITOR cases,
  so it is falling back to compiz.
END
    else
        cat <<END
* This script's COMPOSITOR cases don't account for $XDG_CURRENT_DESKTOP
  as XDG_CURRENT_DESKTOP. Install compiz and try again, or ensure that
  compositing is enabled if you are running metacity or another
  compositor that starts automatically then set COMPOSITOR to "none":
    ./$me "$1" none
END
        exit 1
    fi

fi

if [ -z "$COMPOSITOR" ]; then
    echo "The COMPOSITOR command couldn't be detected. Try setting the 'COMPOSITOR' environment variable first."
    exit 1
fi
if [ -z "$DIR_HANDLER" ]; then
    cat <<END
The DIR_HANDLER couldn't be detected. Try setting the 'DIR_HANDLER'
environment variable to a filename that exists in an XDG shortcuts
location such as /usr/share/applications.
END
    exit 1
fi
if [ ! -f "/usr/share/applications/$DIR_HANDLER" ]; then
    if [ ! -f "/usr/local/share/applications/$DIR_HANDLER" ]; then
        if [ ! -f "$HOME/.local/share/applications/$DIR_HANDLER" ]; then
            cat <<END
Error: $DIR_HANDLER is not in a known XDG location such as
/usr/share/applications, /usr/local/share/applications, nor
$HOME/.local/share/applications and therefore probably won't be
accessible to gio nor to software reading
$HOME/.local/share/applications/defaults.list
END
            exit 1
        fi
    fi
fi
compositor_line="$COMPOSITOR >& ~/compositor.log &"
if [ "@$COMPOSITOR" = "@none" ]; then
    compositor_line="# no compositor"
fi
#if [ -f "`command -v nohup`" ]; then
#    compositor_line="nohup $COMPOSITOR --replace >& $HOME/compositor.log &"
#    echo "* using nohup for '$compositor_line'..."
#else
#    echo "* nohup is not available, so the output of $compositor_line will not be logged."
#fi

appendif(){
    line="$1"
    line_flag="$2"
    file="$3"
    if [ -z "$line" ]; then
        echo "[appendif] You must specify a line such as Exec=blender as the 1st param."
    fi
    if [ -z "$line_flag" ]; then
        echo "[appendif] You must specify a line_flag such as Exec= as the 2rd param."
        exit 1
    fi
    if [ -z "$file" ]; then
        echo "[appendif] You must specify a file as the 3rd param."
        exit 1
    fi
    old_line="`cat $file | grep "$line_flag"`"
    if [ ! -z "$old_line" ]; then
        echo "* skipping \"$line\""
        echo "  since \"$file\" already contains"
        echo "  \"$line_flag\""
        echo "  (\"$old_line\")"
    else
        echo "* adding \"$line\" to \"$file\" (since it has no \"$line_flag\")"
        echo "$line" >> "$file"
    fi
}

autostart_dir=~/.config/openbox
autostart_path=~/.config/openbox/autostart.sh
# if [ -d "$autostart_dir" ]; then
if [ -f "$autostart_path" ]; then
    # echo "* \"$autostart_dir\" was present so that will be used instead of X-GNOME- variables in shortcuts."
    # autostart_path=~/.config/openbox/autostart.sh
    echo "* \"$autostart_path\" was present so that will be used instead of X-GNOME- variables in shortcuts."

    echo "* checking \"$autostart_path\""
    touch "$autostart_path"
    has_cairo_dock=false
    if [ ! -z "`cat $autostart_path | grep cairo-dock`" ]; then
        has_cairo_dock=true
    fi
    has_compositor=false
    # if [ "@$COMPOSITOR" != "@none" ]; then
    if [ ! -z "`cat $autostart_path | grep $COMPOSITOR`" ]; then
        has_compositor=true
    else
        if [ "@$has_cairo_dock" = "@true" ]; then
            cat <<END
Error: This script cannot handle the situation where
\"$autostart_path\" already has cairo-dock but not the COMPOSITOR
$COMPOSITOR, so you must manually add the following before cairo-dock:"
  $cairo_dock_line
END
            exit 1
        fi
    fi
    if [ "@$COMPOSITOR" = "@none" ]; then
        if [ -z "`cat $autostart_path | grep $COMPOSITOR`" ]; then
            echo "rm ~/compositor.log"  >> "$autostart_path"
            echo "  * writing '$compositor_line'"
        else
            echo "* $COMPOSITOR is already in \"$autostart_path\"."
        fi
    else
        if [ -z "`cat $autostart_path | grep $compositor_line`" ]; then
            echo "rm ~/compositor.log"  >> "$autostart_path"
            echo "$compositor_line" >> "$autostart_path"
            # ^ ok even if "$COMPOSITOR" = "none" since compositor_line will be a comment in that case
        else
            echo "* $compositor_line is already in \"$autostart_path\"."
        fi
    fi
    # else
    #     echo "* COMPOSITOR is \"$COMPOSITOR\" so it will not be added to startup."
    # fi
    if [ -z "`cat $autostart_path | grep cairo-dock`" ]; then
        echo "rm ~/cairo-dock.log" >> "$autostart_path"
        echo "  * writing '$cairo_dock_line'"
        echo "$cairo_dock_line" >> "$autostart_path"
    else
        echo "* cairo-dock is already in \"$autostart_path\""
    fi
    echo "* $HOME/.config/openbox/autostart.sh ran `date`" > ~/autostart-openbox.log
    exit 0
else
    echo "* skipping \"$autostart_path\" since not present."
fi
mkdir -p $HOME/.local/bin/
launchboth="$HOME/.local/bin/compositor+cairo-dock.sh"
printf "* writing \"$launchboth\"..."
cat > "$launchboth" <<END
#!/bin/bash
# This file was generated by $me from https://github.com/poikilos/linux-preinstall
echo date="\`date\`" > \$HOME/compositor+cairo-dock.log
echo USER="\$USER" >> \$HOME/compositor+cairo-dock.log
me=compositor+cairo-dock.sh
rm "\$HOME/compositor.log"
rm "\$HOME/cairo-dock.log"
COMPOSITOR=$COMPOSITOR
if [ ! -z "\$1" ]; then
    COMPOSITOR="\$1"
fi
if [ "@\$COMPOSITOR" != "@none" ]; then
    if [ -z "\`ps -e | grep \$COMPOSITOR | grep -v compositor+cairo\`" ]; then
        # don't use grep -v \$me if using -e, since output is like "4038 ?        00:00:00 compositor+cairo-do"
        echo "compositor_line=\"$compositor_line\"" > ~/compositor.log
        # \$COMPOSITOR >>& ~/compositor.log &
        $compositor_line
    else
        echo "* \$COMPOSITOR was already running:" > "\$HOME/compositor.log"
        echo "\`ps -e | grep \$COMPOSITOR\`" >> "\$HOME/compositor.log"
        echo "  * details:" >> "\$HOME/compositor.log"
        echo "\`ps aux | grep \$COMPOSITOR | grep -v grep | grep -v \$me\`" >> "\$HOME/compositor.log"
    fi
else
    echo "COMPOSITOR was $COMPOSITOR so \$me didn't attempt to start a compositor." > ~/compositor.log
fi
# sleep 2
# ^ not necessary since has a wait argument now (-w 15 is recommended by the recurring problems sticky post on the forum)

if [ -z "\`ps -e | grep cairo-dock\`" ]; then
    $cairo_dock_line
else
    echo "* cairo-dock was already running:" > "\$HOME/cairo-dock.log"
    echo "\`ps aux | grep cairo-dock | grep -v grep\`" >> "\$HOME/cairo-dock.log"
fi


END
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
else
    echo "OK"
fi
chmod +x "$launchboth"
launchboth_dt="$HOME/.config/autostart/linux-preinstall-compositor+cairo-dock.desktop"
printf "* writing \"$launchboth_dt\"..."
# cat > $HOME/.config/autostart/linux-preinstall-COMPOSITOR.desktop <<END
cat > $launchboth_dt <<END
[Desktop Entry]
Type=Application
Name=Run both $COMPOSITOR and cairo-dock
Comment=generated by $me
Exec=$launchboth
NoDisplay=true
X-GNOME-Autostart-Phase=WindowManager
X-GNOME-Provides=windowmanager
X-GNOME-Autostart-Notify=true
END
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
else
    echo "OK"
    echo "Logout for changes to take effect."
fi


#echo "* writing \"$HOME/.config/autostart/linux-preinstall-cairo-dock.desktop\"..."

# cat > $HOME/.config/autostart/linux-preinstall-cairo-dock.desktop <<END
cat > /dev/null <<END
[Desktop Entry]
Type=Application
Name=Cairo-Dock
Comment=generated by $me
Exec=/usr/bin/cairo-dock
NoDisplay=true
#X-GNOME-Autostart-Phase=WindowManager
X-GNOME-Requires=windowmanager
X-GNOME-Autostart-Notify=true
END

appendif x-scheme-handler/file=$DIR_HANDLER x-scheme-handler/file /home/owner/.local/share/applications/defaults.list
appendif inode/directory=$DIR_HANDLER inode/directory /home/owner/.local/share/applications/defaults.list
appendif x-directory/normal=$DIR_HANDLER x-directory/normal /home/owner/.local/share/applications/defaults.list

cat <<END
* If you can't open directories using the Cairo-Dock shortcuts, see
  <https://glx-dock.org/ww_page.php?p=Recurrents%20problems&lang=en#24-The%20dock%20doesn%27t%20launch%20the%20right%20files%20manager,%20images%20viewer,%20etc>
  - You must restart after following certain steps regarding defaults.
    Submit a pull request for this script a certain additional step
    worked.
  - Alternatively, install a integration package such as:
    - output of apt list cairo-dock-*-integration-plug-in:
END
apt list cairo-dock-*-integration-plug-in
echo
if [ -f $launchboth.bak ]; then
    echo "See also meld $launchboth $launchboth.bak"
fi
echo
echo Done
