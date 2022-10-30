#!/bin/bash
if [ ! -d "utilities/find_linuxpreinstall" ]; then
    echo "Error: utilities/find_linuxpreinstall is not a directory in `pwd`"
fi
meldq utilities/find_linuxpreinstall utilities-server/find_linuxpreinstall utilities-developer/find_linuxpreinstall
code=$?
if [ $code -ne 0 ]; then echo "meldq returned error $code"; exit $code; fi

echo "launching meld */find_linuxpreinstall via meldq..."

sleep 7
if [ ! -d "utilities/find_pycodetool" ]; then
    echo "Error: utilities/find_pycodetool is not a directory in `pwd`"
fi
meldq utilities/find_pycodetool utilities-server/find_pycodetool utilities-developer/find_pycodetool
code=$?
if [ $code -ne 0 ]; then echo "meldq returned error $code"; exit $code; fi
echo "launching meld */find_pycodetool via meldq..."
