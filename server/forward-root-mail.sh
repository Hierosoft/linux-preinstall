#!/bin/sh
sudo su -
if [ -z "$1" ]; then
    echo "You must specify an e-mail address that should receive root's mail."
    exit 1
fi
echo $1 > /root/.forward
