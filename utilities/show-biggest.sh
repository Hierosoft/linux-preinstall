#!/bin/sh
outfile=~/biggest.txt
sudo du -Sh / | sort -rh | head -n 100 > $outfile
echo
echo
echo "Done (see $outfile)."
echo "If it is empty, try:"
echo "  rm '$outfile'"
echo "- Then run this script as root."
echo
echo
