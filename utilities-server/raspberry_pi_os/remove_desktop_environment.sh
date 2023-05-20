#!/bin/bash
sudo apt update
# Use raspi-config & to configure OS to not start graphical DE
# or:
# See <https://forums.raspberrypi.com/viewtopic.php?p=1504837&sid=18c7b67ce1f94734a9d96c272bb70122#p1504837>:
# sudo apt purge xserver* lightdm* raspberrypi-ui-mods
# See <https://forums.raspberrypi.com/viewtopic.php?p=1755185#p1755185>:
# Here is a more complete command:
sudo apt purge -y xserver* lightdm* raspberrypi-ui-mods vlc* lxde* chromium* desktop* gnome* gstreamer* gtk* hicolor-icon-theme* lx* mesa* \
    libreoffice* xterm xbitmaps libutempter0 libjavascriptcoregtk-* libpulse* libqt5gui5 pulseaudio-* uno-libs* ure
# ^ installed libreoffice :/ unless I added the second line (last time afterward I did:
#   sudo apt purge libreoffice* libqt5gui* xterm pulseaudio* libjavascriptcoregtk* libpulse*
#   - See https://pastebin.com/4q9yYgbh or ~/Nextcloud/1.Tickets/atomklipper/2023-05-14/purge_guy_step1.txt
#   - See https://pastebin.com/xVWf60TH or ~/Nextcloud/1.Tickets/atomklipper/2023-05-14/purge_guy_step2.txt
sudo apt autoremove -y
sudo reboot
