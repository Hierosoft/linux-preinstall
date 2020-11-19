#!/bin/bash
# See https://github.com/linuxwacom/xf86-input-wacom/wiki/Dual-and-Multi-Monitor-Set-Up-II
xrandr
xsetwacom --list
echo
input_device="Wacom Graphire2 4x5 Pen"
input_device1="Wacom Graphire2 4x5 Pen stylus"
input_device2="Wacom Graphire2 4x5 Pen eraser"
input_device3="Wacom Graphire2 4x5 Pen cursor"
output_device="HDMI-1"
echo
echo
echo "Using the information above, run the following commands, but replace $input_device with your input device listed above, and replace $output_device with your output device listed further up:"
echo
echo "xsetwacom set \"$input_device1\" MapToOutput $output_device"
echo "xsetwacom set \"$input_device2\" MapToOutput $output_device"
echo "xsetwacom set \"$input_device3\" MapToOutput $output_device"
echo
echo "You only need to run xsetwacom on your wacom inputs if you have multiple monitors. Doing so will map your digitizing tablet to that monitor, so that the cursor will move at the same speed in the x and y direction, given that your tablet's aspect ratio is the same as your screen's."
echo
echo

# Other method (choose a display and input device): See tablet-map-to-monitor.txt
