#!/bin/sh
source $HOME/.config/linux-preinstall/globals.rc
if [ $? -ne 0 ]; then
    echo "ERROR: 'source $HOME/.config/linux-preinstall/globals.rc' failed."
    echo "You must run linux-preinstall/setup.sh first."
    exit 1
fi
source $LINUX_PREINSTALL/api.rc
if [ $? -ne 0 ]; then
    echo "ERROR: 'source $LINUX_PREINSTALL/api.rc' failed."
    echo "You must run linux-preinstall/setup.sh first."
    exit 1
fi

$INSTALL_CMD gnome-system-monitor xfsprogs treil
sudo ufw-enable

cat <<END
treil: graphical folder space usage display similar to windirstat (example: sudo treil -o ~/usage-slash.png /)
END
