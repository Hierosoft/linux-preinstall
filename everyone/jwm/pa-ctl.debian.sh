#!/bin/bash
# This script can be run as root or as a sudoer.

sudo apt-get install -y libpulse-dev libnotify-dev
REPO_USER=fernandotcl
REPO_NAME=pa-applet
REPO_URL=https://github.com/$REPO_USER/$REPO_NAME.git

mkdir -p "$HOME/Downloads/git/$REPO_USER"
cd "$HOME/Downloads/git/$REPO_USER"
if [ $? -ne 0 ]; then
    echo "Error: 'cd $HOME/Downloads/git/$REPO_USER' failed."
    exit 1
fi
if [ ! -d "$REPO_NAME" ]; then
    git clone $REPO_URL
    if [ $? -ne 0 ]; then
        echo "Error: 'git clone $REPO_URL' failed in \"`pwd`\"."
        exit 1
    fi
    cd $REPO_NAME
else
    cd $REPO_NAME
    git pull
    if [ $? -ne 0 ]; then
        echo "Warning: 'git pull' failed in \"`pwd`\"."
    fi
fi

./autogen.sh
./configure
if [ $? -ne 0 ]; then
    echo "Warning: './configure' failed in \"`pwd`\"."
fi
make
if [ $? -ne 0 ]; then
    echo "Warning: 'make' failed in \"`pwd`\"."
fi
sudo make install
