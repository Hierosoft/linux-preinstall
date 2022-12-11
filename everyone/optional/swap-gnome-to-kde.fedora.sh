#!/bin/bash
# For further documentation and comments, see swap-gnome-to-cinnamon.fedora.sh
echo "This script was not tested with KDE. Only the cinnamon version was tested."
echo "If you're not sure what you're doing or are in a GUI Terminal application press Ctrl+C to cancel!"
echo "5 seconds left to cancel..."
sleep 5
sudo dnf install -y sddm
sudo mkdir /etc/dnf/protected.d-unprotected-by-linux-preinstall
sudo mv /etc/dnf/protected.d/fedora-workstation.conf /etc/dnf/protected.d-unprotected-by-linux-preinstall/
# ^ has NetworkManager & gnome-shell, but cinnamon uses NetworkManager:
echo "NetworkManager" | sudo tee /etc/dnf/protected.d/cinnamon-fedora-workstation-linux-preinstall.conf
sudo dnf groupremove "GNOME desktop Environment"
echo "Only say 'y' to the following if you're really sure and you are in a text-mode tty, *not* a GUI terminal!"
# Remove extras that will block gnome-shell uninstall:
sudo dnf remove "gnome-shell-*"
# swap avoids removing packages that both use:
sudo dnf swap gnome-shell @kde-desktop-environment
# ^ includes the KDE (K Desktop Environment) (kde-desktop) group.
#   For everything kde-desktop-environment gets, run:
#   dnf groupinfo kde-desktop-environment
sudo systemctl enable sddm
