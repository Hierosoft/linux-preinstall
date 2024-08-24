#!/bin/bash
if [ ! -d "utilities/find_linuxpreinstall" ]; then
    echo "Error: utilities/find_linuxpreinstall is not a directory in `pwd`"
fi
meldq utilities/find_linuxpreinstall utilities-server/find_linuxpreinstall utilities-developer/find_linuxpreinstall
code=$?
if [ $code -ne 0 ]; then echo "meldq returned error $code"; exit $code; fi

echo "launching meld */find_linuxpreinstall via meldq..."
