#!/bin/bash
apt-get update
apt-get install -y mate-indicator-applet mate-dock-applet
apt-get install -y mozo
# ^  The edit button on the Brisk Menu calls mozo (or calls menulibre multi-desktop editor).
if [ $? -ne 0 ]; then
    exit 1
fi
cat <<END
The following manual steps are necessary:
- Add "Brisk Menu" to the bottom left (similar to xfce4-whiskermenu).
- Remove "Classic Menu".
- Move the "Show Desktop" icon to the bottom right.
- Add "Indicator Applet Complete" (provided by the `mate-indicator-applet package`) to the left of "Show Desktop".
  - Fixes missing notification icons such as Bluetooth, Nextcloud, Strawberry, and Unity Hub.

Optional (effectiveness not verified):
- Add "XApp Status" to the bottom panel to the left of "Show Desktop".
- Add "Notifications" to the bottom panel to the left of "Show Desktop".
END
