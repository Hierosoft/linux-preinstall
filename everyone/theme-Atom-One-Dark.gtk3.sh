#!/bin/bash
# [Atom One Dark Theme](https://www.gnome-look.org/p/1622922/)
mkdir -p ~/.themes
if [ $? -ne 0 ]; then exit 1; fi
cd ~/.themes
if [ $? -ne 0 ]; then exit 1; fi
themeDirName="Atom One Dark"
if [ ! -d "$themeDirName" ]; then
    echo "* installing `pwd`/$themeDirName"
    git clone https://github.com/UnnatShaneshwar/AtomOneDarkTheme.git "$themeDirName"
    if [ $? -ne 0 ]; then exit 1; fi
    cd "$themeDirName"
else
    cd "$themeDirName"
    git pull --no-rebase --verbose
fi
if [ $? -ne 0 ]; then exit 1; fi
# echo "[SOLVED] [Even if the folder is renamed, there is an error saying the icon theme Atom One Dark is missing in MATE #1](https://github.com/UnnatShaneshwar/AtomOneDarkTheme/issues/1)"
mkdir -p ~/.local/share/icons
enable_clone=false
if [ $? -ne 0 ]; then exit 1; fi
if [ -d "$HOME/.local/share/icons/Atom One Dark" ]; then
    cd "$HOME/.local/share/icons/Atom One Dark"
    if [ $? -ne 0 ]; then
        git pull --no-rebase --verbose
        if [ $? -ne 0 ]; then
            cd ..
            if [ $? -ne 0 ]; then exit 1; fi
            if [ -d "Atom One Dark.1st" ]; then
                mv "Atom One Dark" "Atom One Dark.bak"
            else
                mv "Atom One Dark" "Atom One Dark.1st"
            fi
            enable_clone=true
        fi
    fi
else
    enable_clone=true
fi
if [ "@$enable_clone" = "@true" ]; then
    git clone https://github.com/UnnatShaneshwar/AtomOneDarkIcons.git "$HOME/.local/share/icons/Atom One Dark"
    if [ $? -ne 0 ]; then exit 1; fi
fi
