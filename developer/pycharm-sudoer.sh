#!/bin/bash
me=pycharm.sh
DL_PATH_IS_CUSTOM=false
if [ ! -z "$1" ]; then
    DL_PATH="$1"
    DL_PATH_IS_CUSTOM=true
    echo "* using $DL_PATH as DL_PATH (pycharm tarball)."
fi
DL_DIR="$HOME/Downloads"
DL_NAME="pycharm-community-2021.1.tar.gz"
EX_NAME="pycharm-community-2021.1"
# ^ The extracted directory name is necessary creating a symlink later
#   (only if not using install_any.py)
if [ -z "$DL_PATH" ]; then
    DL_PATH="$DL_DIR/$DL_NAME"
else
    DL_PATH_IS_CUSTOM=true
fi

HTML_URL="https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=linux&code=PCC"
URL=https://download.jetbrains.com/python/$DL_NAME
if [ ! -f "$DL_PATH" ]; then
    if [ "@$DL_PATH_IS_CUSTOM" = "@true" ]; then
        echo "Error: You specified DL_PATH \"$DL_PATH\" but it doesn't exist."
        exit 1
    fi
    mkdir -p "$DL_DIR"
    wget -O $DL_PATH $URL
    if [ $? -ne 0 ]; then
        echo "Error: 'wget -O $DL_PATH $URL' failed."
        echo "You must first manually download PyCharm from $HTML_URL"
        echo " and/or specify a path to a pycharm tarball such as:"
        echo " $me $DL_PATH"
        exit 1
    fi
else
    echo "* using existing \"$DL_PATH\"..."
fi
# See https://www.lifewire.com/how-to-install-the-pycharm-python-ide-in-linux-4091033
# sudo tar xfz $DL_PATH -C /opt/
# code=$?
# if [ $code -ne 0 ]; then
#     echo "Error: Extracting $DL_PATH failed."
#     exit $code
# fi
INSTALL_ANY=install_any.py
if [ ! -f "`command -v install_any.py`" ]; then
    printf "install_any.py is not in the system path. Detecting current dir..."
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
    if [ $? -ne 0 ]; then
        echo "FAILED"
        exit 1
    fi
    printf "OK...getting linux-preinstall dir..."
    REPO_DIR="$( dirname "${DIR}")"
    if [ $? -ne 0 ]; then
        echo "FAILED"
        exit 1
    fi
    printf "OK...checking for install_any.py in $REPO_DIR..."
    TRY_PATH="$REPO_DIR/utilities/install_any.py"
    if [ ! -f "$TRY_PATH" ]; then
        echo "FAILED (missing)"
        exit 1
    else
        INSTALL_ANY="$TRY_PATH"
        echo "OK"
    fi
fi
$INSTALL_ANY "$DL_PATH"
