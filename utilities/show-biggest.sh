#!/bin/sh
BIG_LIST_FILE=~/biggest.txt
THIS_CMD_PREFIX=
if [ ! -z "$1" ]; then
    BIG_DIR="$1"
fi
if [ -z "$BIG_DIR" ]; then
    BIG_DIR=/
    THIS_CMD_PREFIX=sudo
fi
$THIS_CMD_PREFIX du -Sh "$BIG_DIR" | sort -rh | head -n 100 > $BIG_LIST_FILE
echo
echo
echo "Done (see $BIG_LIST_FILE)."
echo "If it is empty, try:"
echo "  rm '$BIG_LIST_FILE'"
echo "- Then run this script as root."
echo
echo
