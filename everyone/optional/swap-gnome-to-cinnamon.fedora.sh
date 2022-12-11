#!/bin/bash
echo
echo
echo "This file must run in test mode since removing gdm exits the desktop environment!"
echo
echo "If you're in a GUI Terminal application press Ctrl+C to cancel!"
echo "5..."
sleep 1
echo "4..."
sleep 1
echo "3..."
sleep 1
echo "2..."
sleep 1
echo "1..."
sleep 1
sudo dnf install -y lightdm
# sudo systemctl disable gdm
# ^ gdm will be removed later


sudo mkdir /etc/dnf/protected.d-unprotected-by-linux-preinstall
sudo mv /etc/dnf/protected.d/fedora-workstation.conf /etc/dnf/protected.d-unprotected-by-linux-preinstall/
# ^ contains NetworkManager and gnome-shell, and
#   cinnamon network applet uses NetworkManager, so:
echo "NetworkManager" | sudo tee /etc/dnf/protected.d/cinnamon-fedora-workstation-linux-preinstall.conf

# Now the hard part is separating required fedora-like stuff from gnome itself:
cat >/dev/null <<END
sudo dnf group info "Fedora Workstation"
Last metadata expiration check: 2:18:53 ago on Sat 10 Dec 2022 04:49:47 PM EST.
Environment Group: Fedora Workstation
 Description: Fedora Workstation is a user friendly desktop system for laptops and PCs.
no group 'arm-tools' from environment 'workstation-product-environment'
 Mandatory Groups:
   Common NetworkManager Submodules
   Container Management
   Core
   Fedora Workstation product core
   Firefox Web Browser
   Fonts
   GNOME Desktop Environment
   Guest Desktop Agents
   Hardware Support
   LibreOffice
   Multimedia
   Printing Support
   base-x
END

sudo dnf groupremove "GNOME desktop Environment"
# ^ says not installed on mine, but gnome-shell is still installed, so try:

echo "Only say 'y' to the following if you're really sure and you are in a text-mode tty, *not* a GUI terminal!"

# sudo dnf swap gnome-shell @cinnamon-desktop
# says:
#```
#No match for group package "imsettings-systemd"
#Error:
# Problem: problem with installed package gnome-shell-extension-gamemode-8-1.fc37.noarch
#  - package gnome-shell-extension-gamemode-8-1.fc37.noarch requires gnome-shell >= 3.38, but none of the providers can be installed
#  - conflicting requests
#(try to add '--skip-broken' to skip uninstallable packages)
#```
#so try:
# Get the underlying name via:
sudo dnf grouplist --hidden -v
# Remove extras that will block gnome-shell uninstall:
sudo dnf remove "gnome-shell-*"
# swap avoids removing packages that both use:
sudo dnf swap gnome-shell @cinnamon-desktop
# The result looks good:
cat >/dev/null <<END
Removing:
 gnome-shell                     x86_64   43.2-1.fc37         @updates     10 M
Removing unused dependencies:
 adwaita-qt6                     x86_64   1.4.2-1.fc37        @anaconda   264 k
 bolt                            x86_64   0.9.2-1.fc36        @anaconda   523 k
 colord-gtk4                     x86_64   0.3.0-2.fc37        @anaconda    36 k
 freerdp-libs                    x86_64   2:2.8.1-1.fc37      @updates    3.0 M
 gcr                             x86_64   3.92.0-1.fc37       @anaconda   140 k
 gdm                             x86_64   1:43.0-3.fc37       @anaconda   5.1 M
 gnome-autoar                    x86_64   0.4.3-2.fc37        @anaconda   163 k
 gnome-bluetooth                 x86_64   1:42.4-3.fc37       @updates     99 k
 gnome-bluetooth-libs            x86_64   1:42.4-3.fc37       @updates    1.1 M
 gnome-control-center            x86_64   43.1-1.fc37         @anaconda    20 M
 gnome-remote-desktop            x86_64   43.1-1.fc37         @anaconda   936 k
 gnome-session                   x86_64   43.0-1.fc37         @anaconda   1.5 M
 gnome-session-wayland-session   x86_64   43.0-1.fc37         @anaconda    15 k
 gnome-session-xsession          x86_64   43.0-1.fc37         @anaconda    15 k
 gnome-tour                      x86_64   43.0-2.fc37         @updates    2.8 M
 gupnp-av                        x86_64   0.14.1-2.fc37       @anaconda   366 k
 gupnp-dlna                      x86_64   0.12.0-3.fc37       @anaconda   358 k
 libmediaart                     x86_64   1.9.6-2.fc37        @anaconda    88 k
 libwinpr                        x86_64   2:2.8.1-1.fc37      @updates    1.1 M
 malcontent                      x86_64   0.11.0-1.fc37       @anaconda   462 k
 malcontent-control              x86_64   0.11.0-1.fc37       @anaconda   124 k
 malcontent-ui-libs              x86_64   0.11.0-1.fc37       @anaconda   117 k
 power-profiles-daemon           x86_64   0.12-2.fc37         @anaconda   135 k
 qgnomeplatform-qt6              x86_64   0.9.0-5.fc37        @updates    519 k
 qt6-qtwayland                   x86_64   6.4.1-1.fc37        @updates    4.3 M
 rygel                           x86_64   0.40.4-2.fc37       @anaconda   4.6 M
 switcheroo-control              x86_64   2.6-2.fc37          @anaconda   103 k
Installing Groups:
 Cinnamon
END
# ^ The install list had no packages on mine since I had already installed the
#   group earlier, but the output demonstrates that packages that cinnamon
#   requires (and important stuff like xorg) is not uninstalled.
sudo systemctl enable lightdm
