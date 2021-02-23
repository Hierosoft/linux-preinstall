#!/bin/bash

customExit() {
    errorCode=1
    if [ ! -z "$2" ]; then
        errorCode="$2"
    fi
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit $errorCode
}
if [ -z "$PROGRAMS_PATH" ]; then
    PROGRAMS_PATH=~/Downloads/git/poikilos
fi
if [ -z "$PROGRAM_PATH" ]; then
    PROGRAM_PATH=~/Downloads/git/poikilos/linux-preinstall
fi
if [ -d "$HOME/git/linux-preinstall" ]; then
    # Use the existing one if already somewhere else.
    PROGRAMS_PATH="$HOME/git"
    PROGRAM_PATH="$PROGRAMS_PATH/linux-preinstall"
fi
if [ ~ -d "$PROGRAMS_PATH" ]; then
    mkdir -p "$PROGRAMS_PATH" || customExit "mkdir -p ~/Downloads/git/poikilos failed."
fi
cd "$PROGRAMS_PATH" || customExit "cd ~/Downloads/git/poikilos failed."
if [ ! -d "$PROGRAM_PATH" ]; then
    echo "* cloning into $PROGRAM_PATH..."
    git clone https://github.com/poikilos/linux-preinstall $PROGRAM_PATH || customExit "git clone https://github.com/poikilos/linux-preinstall failed."
    cd "$PROGRAM_PATH" || customExit "cd linux-preinstall failed to create \"$PROGRAM_PATH\" via git clone in \"`pwd`\"."
    echo "git clone finished cloning \"`pwd`\"."
else
    cd "$PROGRAM_PATH" || customExit "cd \"$PROGRAM_PATH\" failed in `pwd`."
    git pull || customExit "git pull failed in `pwd`."
    echo "git pull finished updating \"`pwd`\"."
fi
./setup.sh
