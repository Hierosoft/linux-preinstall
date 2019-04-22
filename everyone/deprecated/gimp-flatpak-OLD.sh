# IF GIMP 2.9.8 (works with stylus better supposedly--see https://www.daviesmediadesign.com/project/set-wacom-drawing-tablet-gimp-2018/) is not yet available on your distro's repo (such as Fedora 28 Jan 2018), install the flatpak:
# above is INCORRECT: That is a misreading of the Gimp 2.10 release notes. The notes say that better graphics tablet support is planned for 3.0.
# dnf -y remove gimp
# BUT that will sacrifice all plugins installed above, so reinstall them (see always-install-Fedora-dev-unpriveleged-user.sh)
echo
echo
echo "Installing GIMP flatpak (for more recent version) will require privs to install the repo itself, but GIMP can be still installed as unpriveleged user."
echo
flatpak_icons="/var/lib/flatpak/exports/share/applications"
flatpak_icons_gimp="$flatpak_icons/org.gimp.GIMP.desktop"
flatpak_gimp="/var/lib/flatpak/app/org.gimp.GIMP"
flatpak_gimp_icons="$flatpak_gimp/current/active/export/share/applications"
flatpak_gimp_icon="$flatpak_gimp_icons/org.gimp.GIMP.desktop"
if [ -d "$var_gimp_overlay_dir" ]; then
  echo "WARNING: $var_gimp_overlay_dir already exists. Installing flatpak over it (Ctrl C to cancel)..."
  echo "3..."
  sleep 1
  echo "2..."
  sleep 1
  echo "1..."
  sleep 1
fi
flatpak install https://flathub.org/repo/appstream/org.gimp.GIMP.flatpakref
if [ ! -d "$var_gimp_overlay_dir" ]; then
  echo "ERROR: installing flatpak did not result in '$var_gimp_overlay_dir' for user."
else
  echo "Installed to $var_gimp_overlay_dir"
fi

var_gimp_overlay_dir="$HOME/.var/app/org.gimp.GIMP"
if [ ! -d "$var_gimp_overlay_dir" ]; then
  echo "ERROR: installing flatpak did not result in '$var_gimp_overlay_dir' for user."
else
  echo "Installed to $var_gimp_overlay_dir"
fi
usr_icons="/usr/share/applications"
usr_gimp_icon="$usr_icons/gimp.desktop"
if [ -f "$usr_gimp_icon" ];then
  echo "WARNING: $usr_gimp_icon already exists, so flatpak version will appear alongside it in the application menu"
  echo "since icons in /var/lib/flatpak/exports/share/applications are used by your desktop in addition to $usr_icons (if configured automatically by your version of flatpak)."
fi
usr_icons="/usr/local/share/applications"
usr_gimp_icon="$usr_icons/gimp.desktop"
if [ -f "$usr_gimp_icon" ];then
  echo "WARNING: $usr_gimp_icon already exists, so flatpak version will appear alongside it in the application menu since icons in"
  echo " '/var/lib/flatpak/exports/share/applications' are used by your desktop in addition to $usr_icons (if configured automatically by your version of flatpak)."
  echo " You can manually edit $flatpak_gimp_icon (symlink to it is $flatpak_icons_gimp)"
fi
