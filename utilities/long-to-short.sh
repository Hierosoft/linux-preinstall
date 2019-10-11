#!/bin/sh
if [ ! -f "$1" ]; then
    echo "You must specify a file."
    exit 1
fi
awk '{ print length($0) " " $0; }' "$1" | sort -r -n | cut -d ' ' -f 2-
