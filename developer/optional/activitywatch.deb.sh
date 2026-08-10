#!/bin/bash
sudo apt install -y libxcb-cursor0
# ^ Prevents false start:
#qt.qpa.plugin: From 6.5.0, xcb-cursor0 or libxcb-cursor0 is needed to load the Qt xcb platform plugin.
#qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
#This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
#
#Available platform plugins are: xcb, vkkhrdisplay, minimal, linuxfb, wayland, wayland-egl, minimalegl, vnc, offscreen.


if [ ! -f /opt/activitywatch/aw-qt ]; then
	>&2 echo "No /opt/activitywatch/aw-qt. Try installing the deb package manually from https://github.com/ActivityWatch/activitywatch/releases"
	exit 1
fi
