#!/bin/bash
if [ -z "$1" ]; then
    echo "Error: Specify a decimal value (1.25 for 125%), usually between 1.0 and 2.0"
    exit 1
fi
if [ ! -z "$2" ]; then
    echo "Error: Expected decimal value, got extra arg '$2'"
    exit 1
fi
dconf write /org/cinnamon/desktop/interface/text-scaling-factor $1
