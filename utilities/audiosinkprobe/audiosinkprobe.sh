#!/bin/bash

echo
echo
this_pa="/etc/pulse/default.pa"
for x in 0 1 2 3; do
    for y in 0 1 2 3; do
        sudo ./subroutine.sh $x $y
        echo "  - playing sound as $USER..."
        nohup cvlc "349312__newagesoup__pink-noise-10s.wav" &
        sleep 1
        killall cvlc
        echo "  - stopped playback on purpose ($x,$y)"
    done
done
