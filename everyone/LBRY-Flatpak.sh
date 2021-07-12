#!/bin/bash

mkdir -p ~/tmp
cd ~/tmp
fname=io.lbry.lbry-app.flatpakref
wget -O $fname https://dl.flathub.org/repo/appstream/$fname

flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
# ^ as per <https://flatpak.org/setup/Fedora/>
# ^ Use system rather than `--user` for *everything* in linux-preinstall to avoid doubling up on dependencies.

flatpak install -y flathub io.lbry.lbry-app
# ^ as per <https://flathub.org/apps/details/io.lbry.lbry-app> + -y
if [ $? -ne 0 ]; then
    echo "The flatpak install command failed as $USER."
    echo "Try the following (if no sudo run as root) then try again:"
    echo "sudo chown -R $USER:$USER $HOME/.local/share/flatpak"
    exit 1
fi

flatpak update -y io.lbry.lbry-app

# The following is not necessary since flatpak makes an icon
# (~/.local/share/flatpak/exports/share/applications/io.lbry.lbry-app.desktop):
#ICON=~/.local/share/applications/LBRY.flatpak.desktop
#cat > $ICON << END
#[Desktop Entry]
#Version=1.0
#Type=Application
#Name=LBRY (Flatpak)
#GenericName=LBRY
#Comment=
#Exec=flatpak run io.lbry.lbry-app
#Icon=
#Terminal=false
#StartupNotify=false
#END
