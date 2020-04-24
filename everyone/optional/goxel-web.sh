#!/bin/bash
_WEB_INSTALL_URL=https://raw.githubusercontent.com/poikilos/linux-preinstall/master/install-via-web.sh
_GOOD_FLAG_FILE=~/Downloads/git/poikilos/linux-preinstall/install-via-web.sh
if [ ! -f "$_GOOD_FLAG_FILE" ]; then
    curl $_WEB_INSTALL_URL | bash
fi
if [ ! -f "$_GOOD_FLAG_FILE" ]; then
    echo "Piping $_WEB_INSTALL_URL to bash did not result in $_GOOD_FLAG_FILE"
    exit 1
fi
_PROGRAM_SRC_PATH=~/Downloads/git/guillaumechereau/goxel
_PROGRAM_SRC_BIN_FILE_PATH=~/Downloads/git/guillaumechereau/goxel/goxel
_CONFIGS_PATH=~/.config/linux-preinstall
mkdir -p $_CONFIGS_PATH
_GOXEL_DEPS_RESULT_PATH=$_CONFIGS_PATH/got_goxel_deps.txt
_GOXEL_DEPS_SCRIPT=~/Downloads/git/poikilos/linux-preinstall/everyone/optional/goxel.sh
if [ ! -f "$_GOXEL_DEPS_RESULT_PATH" ]; then
    echo "You must provide permission to allow installing dependencies via $_GOXEL_DEPS_SCRIPT."
    sudo $_GOXEL_DEPS_SCRIPT 1>$_GOXEL_DEPS_RESULT_PATH 2>&1
else
    # echo is necessary to ensure $? becomes 0:
    echo "* skipping $_GOXEL_DEPS_SCRIPT since detected $_GOXEL_DEPS_RESULT_PATH"
fi
if [ $? -eq 0 ]; then
    $HOME/Downloads/git/poikilos/linux-preinstall/everyone/optional/goxel-nonroot.sh
    if [ $? -eq 0 ]; then
        if [ -f "$_PROGRAM_SRC_BIN_FILE_PATH" ]; then
            $HOME/.local/bin/install_any.py $_PROGRAM_SRC_BIN_FILE_PATH --move
            if [ $? -eq 0 ]; then
                echo "The program and shortcut successfully installed."
            else
                echo "$HOME/.local/bin/install_any.py $_PROGRAM_SRC_BIN_FILE_PATH --move failed."
                exit 1
            fi
        else
            echo "$HOME/Downloads/git/poikilos/linux-preinstall/everyone/optional/goxel-nonroot.sh did not result in."
            exit 1
        fi
    else
        echo "$HOME/Downloads/git/poikilos/linux-preinstall/everyone/optional/goxel-nonroot.sh failed."
        exit 1
    fi
else
    rm "$_GOXEL_DEPS_RESULT_PATH"
    echo "sudo $_GOXEL_DEPS_SCRIPT failed."
    exit 1
fi
