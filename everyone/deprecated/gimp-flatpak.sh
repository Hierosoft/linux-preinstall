#!/bin/sh

# DEPRECATED
# A flatpak version of GIMP is not needed--Fedora 29's version is 2.10
# (The idea that 2.10 has "better support for graphic tablets" is a
# misreading of the release notes. That phrase is actually under the
# "what's next" section, where the enhancement is planned for GIMP 3.0.


icon_name="gimp-2.10-flatpak.desktop"
icon_path="$HOME/ownCloud/Linux/AlwaysInstall/HOME/Desktop/$icon_name"
if [ -f "$icon_name" ]; then
  icon_path="$icon_name"
fi


# flatpak remove org.gimp.GIMP
flatpak install https://flathub.org/repo/appstream/org.gimp.GIMP.flatpakref

if [ -f "$icon_path" ]; then

else
  echo "Icon could $icon_name could not be found. The flatpak version of GIMP can be run (or icon can be created to execute) as follows:"
  echo "flatpak run org.gimp.GIMP//stable"
  sleep 5
fi
dest_icon="/var/lib/flatpak/app/org.gimp.GIMP/current/active/export/share/applications/org.gimp.GIMP.desktop"
if [ -f "$dest_icon" ]; then
  echo "the Flatpak successfully installed an icon at: $dest_icon (this path should automatically be scanned by your Desktop--if not, report this issue to your Desktop's maintainers--it is known to work in KDE Plasma)"
else
  echo "Flatpak has not installed an icon at a known location"
fi

echo 'If colors are flagged with magenta, try to turn off "Mark out of gamut colors" in Edit, Preferences, Color Managmement'
echo "(doesn't seem to turn off in GIMP 2.10.8)"

