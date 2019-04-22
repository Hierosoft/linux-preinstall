#!/bin/sh
cat /proc/asound/cards
echo "now do pacmd set-default-sink x"
echo "where x is the default soundcard you want for pulseaudio."
echo "(changes should take effect immediately even in open programs."
