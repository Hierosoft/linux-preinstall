#!/bin/sh
echo 'XDG_DATA_DIRS="$HOME/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:$XDG_DATA_DIRS"' | sudo tee -a /etc/environment
