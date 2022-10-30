#!/bin/bash
# Symptom 1: HDMI audio gets deselected as default
# Symptom 2: HDMI audio disappears after Sleep
# See <https://archived.forum.manjaro.org/t/audio-sink-for-hdmi-audio-disappears-after-screen-sleeps/133981/18>
enable_restart=true

for i in 1 2 3 4 5 6 7 8 9 10
do
	# pacmd set-default-sink "alsa_output.pci-0000_01_00.1.hdmi-stereo"
	# ^ dynamically named :( so parse output of `pacmd list-sinks | grep 'name: <'` :( :
	# select_audio_script="$HOME/.local/select-audio-device.py"
	if [ -f "`which selectoutput`" ]; then
		# ^ The linuxpreinstall package provides this command.
		selectoutput hdmi
		if [ $? -eq 0 ]; then
			break
		fi
		if [ "x$enable_restart" = "xtrue" ]; then
			enable_restart=false
			pulseaudio -k
		fi
		echo "."
		sleep 1
	else
		echo "Error: selectoutput is not available. Install linuxpreinstall (using 'pip install linux-preinstall' or setup.py)."
		exit 1
	fi
done
if [ "x$enable_restart" = "xfalse" ]; then
	# Wait so output is visible.
	sleep 3
fi
