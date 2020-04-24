#!/bin/bash
REPO_FLAG_FILE=src/goxel.h
_GIT_URL="https://github.com/guillaumechereau/goxel.git"
_GOT_NAME=goxel
EXE_NAME=goxel
if [ -z "$REPOS_PATH" ]; then
    REPOS_PATH=~/Downloads/git/guillaumechereau
    if [ ! -d ~/Downloads/git/guillaumechereau ]; then
        mkdir -p ~/Downloads/git/guillaumechereau
    fi
fi
echo
echo
customDie() {
    echo
    errorLevel=1
    if [ -z "$2" ]; then
        errorLevel=$2
    fi
    if [ -z "$1" ]; then
        echo "Unknown error."
    else
        echo "ERROR:"
        # echo "$1" >> "$err_txt"
        echo "$1"
    fi
    exit $errorLevel
}

if [ ! -f "$REPO_FLAG_FILE" ]; then
    if [ -f "`command -v git`" ]; then
        if [ -d "$_GOT_NAME" ]; then
            cd "$_GOT_NAME"
            echo "* updating `pwd` via git pull..."
            git pull || customDie "git pull failed in `pwd`"
        else
            git clone $_GIT_URL "$_GOT_NAME" || customDie "git clone $_GIT_URL failed in `pwd`"
            cd "$_GOT_NAME" || customDie "git clone $_GIT_URL did not result in `pwd`/$_GOT_NAME"
        fi
    else
        customDie "You need git unless you run this script from a directory containing \"$REPO_FLAG_FILE\"."
    fi
fi
if [ ! -f "$REPO_FLAG_FILE" ]; then
    if [ ! -f "`command -v git`" ]; then
        customDie "You must have git or run this from inside of the goxel source directory containing $REPO_FLAG_FILE."
    fi
fi
echo "Running make in `pwd`..."
make release || customDie "Building failed. See errors above."
echo
echo
echo "Now run the program from \"`pwd`\""
echo
echo "or install via:"
echo "cd \"`pwd`\" && install_any.py $EXE_NAME --move"
