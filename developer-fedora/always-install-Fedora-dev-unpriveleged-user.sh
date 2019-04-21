config_gimp="$HOME/.var/app/org.gimp.GIMP/config/GIMP/2.10"

dl_name=savearea.scm
wget -O $HOME/Downloads/$dl_name http://people.ds.cam.ac.uk/ssb22/notes/savearea.scm
if [ ! -d $HOME/.gimp-2.10/plug-ins ]; then
  mkdir -p $HOME/.gimp-2.10/plug-ins
fi
mv $dl_name $HOME/.gimp-2.10/plug-ins/

echo "Installing Ps-style shortcuts for GIMP..."

if [ ! -d "./AlwaysInstall/HOME/.gimp-2.10" ]; then
  mkdir -p "./AlwaysInstall/HOME/.gimp-2.10"
fi
ps_menurc=./AlwaysInstall/HOME/.gimp-2.10/ps-menurc
if [ ! -f "$ps_menurc" ]; then
  wget -O "$ps_menurc" http://epierce.freeshell.org/gimp/ps-menurc
fi
if [ -f "$config_gimp/menurc" ]; then
  if [ ! -f "$config_gimp/menurc.1st" ]; then
    mv "$config_gimp/menurc" "$config_gimp/menurc.1st"
  fi
fi
cp $ps_menurc "$config_gimp/"
cp -f "$config_gimp/ps-menurc" "$config_gimp/menurc"


if [ -f "$icon_src" ]; then
  if [ ! -d "$HOME/Desktop" ]; then
    mkdir -p "$HOME/Desktop"
  fi
  cp "$icon_src" "$HOME/Desktop/"
else
  echo "ERROR: Missing '$icon_src' so can't install Desktop icon automatically"
  echo "(The icon will appear in the application menu if flatpak configured your Desktop to use the flatpak applications directory /var/lib/flatpak/exports/share/applications)."
fi


echo "Qt Creator:"
echo "Possible ways to fix missing output from qDebug(), qInfo(), and qWarning() streams and possibly others in Qt Creator"
echo "* (didn't work <https://dev.getsol.us/T4667>) Tools, Options, Environment, System, change Terminal to to '/usr/bin/gnome-terminal --' (can be set back to /usr/bin/xterm -e by pressing Reset) [you can pick a terminal such as '/usr/bin/konsole -e' from the list to get the correct options]"
echo "* [SOLVED] <https://bugs.archlinux.org/task/40583>: Project, Build & Run, Run, check 'Run in Terminal'"
echo "  * also consider '/usr/bin/xterm -fg gray -bg black -geometry 200x10+0+900 -e'"

#icon_src="./AlwaysInstall/HOME/Desktop/gimp-2.10-flatpak.desktop"
# NOTE: placing in $HOME/.local/share/applications is not needed since already in /var/lib/flatpak/exports/share/applications
# and that directory is used by the system in addition to $PREFIX/share/applications
# if flatpak correctly appended the setting to your system menu software
#if [ -f "$icon_src" ]; then
#  if [ ! -d "$HOME/.local/share/applications" ]; then
#    mkdir -p "$HOME/.local/share/applications"
#  fi
#  cp "$icon_src" "$HOME/.local/share/applications/"
#else
#  echo "ERROR: Missing '$icon_src' so can't install icon automatically, so from now on you would run the flatpak version of gimp (or create icon for it) manually, with the following command:"
#  echo
#  echo "  flatpak run org.gimp.GIMP//stable"
#  echo
#  echo
#  sleep 4
#fi

