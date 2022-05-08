#!/bin/bash
# Symptom 1: HDMI audio gets deselected as default
# Symptom 2: HDMI audio disappears after Sleep
# See <https://archived.forum.manjaro.org/t/audio-sink-for-hdmi-audio-disappears-after-screen-sleeps/133981/18>
pulseaudio -k
echo "* waiting 10 seconds for pulseaudio..."
sleep 10
# pacmd set-default-sink "alsa_output.pci-0000_01_00.1.hdmi-stereo"
# ^ dynamically named :( so parse output of `pacmd list-sinks | grep 'name: <'` :( :
# select_audio_script="$HOME/.local/select-audio-device.py"
if [ -f "`which selectoutput`" ]; then
    # ^ Installing the linuxpreinstall package via pip provides
    #   this command.
    selectoutput hdmi
fi
sleep 5
