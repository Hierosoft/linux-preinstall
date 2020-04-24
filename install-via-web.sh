#!/bin/bash

customDie() {
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
if [ -z "PROGRAMS_PATH" ]; then
    PROGRAMS_PATH=~/Downloads/git/poikilos
fi
if [ -z "PROGRAM_PATH" ]; then
    PROGRAM_PATH=~/Downloads/git/poikilos/linux-preinstall
fi
mkdir -p ~/Downloads/git/poikilos || customDie "mkdir -p ~/Downloads/git/poikilos failed."
cd ~/Downloads/git/poikilos || customDie "cd ~/Downloads/git/poikilos failed."
if [ ! -d "$PROGRAM_PATH" ]; then
    git clone https://github.com/poikilos/linux-preinstall $PROGRAM_PATH || customDie "git clone https://github.com/poikilos/linux-preinstall failed."
    cd linux-preinstall || customDie "cd linux-preinstall failed in `pwd`."
    echo "git pull finished cloning \"`pwd`\"."
else
    cd "$PROGRAM_PATH" || customDie "cd \"$PROGRAM_PATH\" failed in `pwd`."
    git pull || customDie "git pull failed in `pwd`."
    echo "git pull finished updating \"`pwd`\"."
fi
if [ ! -f "$HOME/.local/bin/install_any.py" ]; then
    if [ -f "$PROGRAM_PATH/install_any.py" ]; then
        if [ ! -d "$HOME/.local/bin" ]; then
            mkdir -p "$HOME/.local/bin"
        fi
        ln -s $PROGRAM_PATH/install_any.py $HOME/.local/bin/install_any.py
    fi
fi
