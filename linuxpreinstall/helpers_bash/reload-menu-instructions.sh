#!/bin/bash

# For example, instead of using this script, do:
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CAT_DIR="`dirname $SCRIPT_DIR`"
REPO_DIR="`dirname $CAT_DIR`"
# bash $REPO_DIR/linuxpreinstall/helpers_bash/reload-menu-instructions.sh

# See also linuxpreinstall.helpers.reload_menu
# For example, instead of using this script, do:
# python -c 'from linuxpreinstall.helpers.reload_menu import main; main()'

# Function to check if a service is running
is_service_running() {
    systemctl is-active --quiet "$1"
}

# Function to check if a process is running
is_process_running() {
    pgrep -x "$1" > /dev/null
}

# Detect the Desktop Environment
if is_process_running "cinnamon"; then
    echo "Cinnamon detected."
    echo "You may have to restart your DE such as via Alt+F2, cinnamon --replace."
elif is_process_running "mate-panel"; then
    echo "MATE detected."
    echo "You may need to restart your DE such as via Alt+F2, mate-panel --replace."
elif is_process_running "plasmashell"; then
    echo "KDE detected."
    echo "You may need to restart your DE such as via Alt+F2, kquitapp5 plasmashell && kstart5 plasmashell."
elif is_process_running "gnome-shell"; then
    echo "GNOME detected."
    echo "You may need to restart your DE such as via Alt+F2, r."
else
    echo "No recognized Desktop Environment detected."
    exit 1
fi
