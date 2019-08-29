#!/bin/bash
user="caelestis"
echo
echo
#echo "* make sure you have root permissions"
customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
this_pa="/etc/pulse/default.pa"
x=$1
y=$2
        
line1flag="load-module module-alsa-sink"
line1="load-module module-alsa-sink device=hw:$x,$y"
line2flag="set-default-sink"
line2="#set-default-sink output 1"
line3flag="load-module module-combine-sink"
line3="load-module module-combine-sink sink_name=combined"
line4flag="set-default-sink combined"
line4="set-default-sink combined"

echo "* trying: $line"
if [ ! -f "$this_pa.1st" ]; then
    cp $this_pa $this_pa.1st || customDie "cp $this_pa $this_pa.1st failed."
fi
mv $this_pa $this_pa.tmp || customDie "mv $this_pa $this_pa.tmp failed."
cat $this_pa.tmp | grep -v "^$line1flag" | grep -v "$line2flag" | grep -v "$line3flag" | grep -v "$line4flag" > $this_pa
echo "$line1" >> $this_pa
echo "$line2" >> $this_pa
echo "$line3" >> $this_pa
echo "$line4" >> $this_pa
echo "  - restarting pulseaudio..."
killall pulseaudio
sleep 3
