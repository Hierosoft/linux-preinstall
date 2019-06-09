#!/bin/sh
sudo du -Sh / | sort -rh | head -n 100 > ~/biggest.txt
