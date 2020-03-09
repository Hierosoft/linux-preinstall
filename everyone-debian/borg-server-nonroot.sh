#!/bin/bash
customDie() {
    echo
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
sudo ./borg.sh server || customDie "You must be in the directory as borg.sh such as linux-preinstall/."
# borgmatic init --encryption repokey
