#!/bin/bash
# python3 -m pip install --user youtube-dlg
# ^ fails (syntax errors indicate it needs python2)

LP_SUBDIR=$(dirname "$0")
# ^ The linux-preinstall subdirectory from which this script may run, such as from linux-preinstall/everyone
if [ -f "../utilities/python-venv.rc" ]; then
    LP_SUBDIR="."
fi
. $LP_SUBDIR/../utilities/python-venv.rc
if [ $? -ne 0 ]; then
    exit 1
fi
. $LP_SUBDIR/../utilities/git.rc
if [ $? -ne 0 ]; then
    exit 1
fi

REPO_NAME="youtube-dl-gui"
# REPO_USER="MrS0m30n3"
REPO_USER="oleksis"
# ^ The oleksis fork is far more updated: https://github.com/oleksis/youtube-dl-gui/network
echo
echo "WARNING: venv is recommended instead of using this script. See the readme."
echo "Press Ctrl+C to cancel within 5 seconds."
echo
sleep 5

REPO_URL="https://github.com/$REPO_USER/$REPO_NAME"
REPOS_PATH="$HOME/Downloads/git/$REPO_USER"
REPO_PATH="$REPOS_PATH/$REPO_NAME"

mkdir -p "$REPOS_PATH"
echo "* updating $REPO_PATH..."
update_repo $REPO_PATH $REPO_URL
if [ $? -ne 0 ]; then
    exit 1
fi
echo
mkdir -p ~/.local
echo "Next, you must manually do:"
echo "cd $REPO_PATH"
echo "python3 setup.py install --prefix ~/.local"
echo "# WARNING: ^ This compiles over 900 cxx and cpp files for several minutes :("
