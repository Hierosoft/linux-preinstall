#!/bin/bash
if [ ! -f "linuxpreinstall/__init__.py" ]; then
    echo "Error: This script must run from the linux-preinstall repo directory containing the linuxpreinstall module directory."
    exit 1
fi
LINUX_PREINSTALL="$PWD"
echo "[$0] This file installs linux-preinstall in place (using $LINUX_PREINSTALL for all shortcuts!)."
echo "[$0] Running ./setup.sh first..."
./setup.sh "$@"
code=$?
if [ $code -ne 0 ]; then
    echo "Error: $0 will not continue since ./setup.sh failed."
    exit $code
fi


mkdir -p ~/.local/share/applications
code=$?
if [ $code -ne 0 ]; then exit $code; fi
rm ~/.local/share/applications/reconnect-audio.desktop >& /dev/null
# cp AlwaysAdd/replace_linux-preinstall_dir/.local/share/applications/reconnect-audio.desktop ~/.local/share/applications/
cp utilities/reconnect-audio.desktop ~/.local/share/applications/
# TODO: ^ ensure path is ok inside desktop file:
sed -i "s#\\\$LINUX_PREINSTALL#$LINUX_PREINSTALL#g" ~/.local/share/applications/reconnect-audio.desktop
# ^ \\ to send '\' to sed, then another \ to send $ to sed instead of processing it

mkdir -p ~/.local/bin
code=$?
if [ $code -ne 0 ]; then exit $code; fi

if [ ! -f ~/.local/bin/reconnect-audio.sh ]; then
    ln -s $LINUX_PREINSTALL/utilities/reconnect-audio.sh ~/.local/bin/reconnect-audio.sh
fi
if [ ! -f ~/.local/bin/selectoutput ]; then
    ln -s $LINUX_PREINSTALL/linuxpreinstall/selectoutput.py ~/.local/bin/selectoutput
fi
if [ ! -f ~/.local/bin/whichicon ]; then
    ln -s $LINUX_PREINSTALL/whichicon ~/.local/bin/whichicon
fi

if [ ! -f "$HOME/.local/bin/blnk" ]; then
    BLNK_GIT_URL="https://github.com/Poikilos/blnk"
    echo "* installing blnk from $BLNK_GIT_URL"
    if [ ! -d "$HOME/git/blnk" ]; then
        git clone $BLNK_GIT_URL $HOME/git/blnk
        code=$?
        if [ $code -ne 0 ]; then
            echo "Error: The blnk repo couldn't be cloned from $BLNK_GIT_URL, so installing it is not possible."
            exit $code
        fi
    fi
    if [ -f "$HOME/git/blnk/blnk" ]; then
        ln -s ~/git/blnk/blnk ~/.local/bin/blnk
        code=$?
        if [ $code -ne 0 ]; then
            echo "Error: '' failed."
            exit $code
        fi
    else
        echo "* This script will install a blnk command if ~/git/blnk has been downloaded, but it is not present."
    fi
else
    echo "* blnk is already installed."
fi
