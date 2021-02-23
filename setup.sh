#!/bin/bash
LINUX_PREINSTALL=""
echo
echo "linux-preinstall setup:"
if [ -f api.rc ]; then
    LINUX_PREINSTALL="`realpath .`"
else
    echo "You must run setup.sh from the linux-preinstall repo containing api.rc"
    exit 1
fi

if [ ! -f "$LINUX_PREINSTALL/api.rc" ]; then
    echo "* 'realpath api.rc' failed to get the full path of api.rc in \"`pwd`\"."
    exit 1
fi
L_P_CONFIG_DIR=$HOME/.config/linux-preinstall
L_P_GLOBALS_PATH="$L_P_CONFIG_DIR/globals.rc"
if [ ! -f "$L_P_GLOBALS_PATH" ]; then
    echo "LINUX_PREINSTALL=\"$LINUX_PREINSTALL\"" > "$L_P_GLOBALS_PATH"
    echo "* wrote \"$L_P_GLOBALS_PATH\""
else
    source "$L_P_GLOBALS_PATH"
    if [ $? -ne 0 ]; then
        echo "ERROR: 'source \"$L_P_GLOBALS_PATH\"' failed."
        echo "The source command is required, such as using bash."
        exit 1
    fi
    if [ -z "$LINUX_PREINSTALL" ]; then
        echo "LINUX_PREINSTALL=\"$LINUX_PREINSTALL\"" >> "$L_P_GLOBALS_PATH"
        echo "* added LINUX_PREINSTALL to \"$L_P_GLOBALS_PATH\""
    elif [ ! -f "$LINUX_PREINSTALL/api.rc" ]; then
        echo "WARNING: LINUX_PREINSTALL in $L_P_GLOBALS_PATH was bad."
        echo "  It will be changed to \"$LINUX_PREINSTALL\"."
        echo "LINUX_PREINSTALL=\"$LINUX_PREINSTALL\"" >> "$L_P_GLOBALS_PATH"
    else
        echo "* LINUX_PREINSTALL=\"$LINUX_PREINSTALL\" is already"
        echo "  present in \"$L_P_GLOBALS_PATH\""
    fi
fi

INSTALL_ANY="$LINUX_PREINSTALL/utilities/install_any.py"
if [ -L "$HOME/.local/bin/install_any.py" ]; then
    INSTALL_ANY_DEST="`readlink $HOME/.local/bin/install_any.py`"
    if [ ! -f "$INSTALL_ANY_DEST" ]; then
        rm "$HOME/.local/bin/install_any.py"
        if [ $? -eq 0 ]; then
            echo "* removed bad symlink \"$HOME/.local/bin/install_any.py\""
            echo "  -> $INSTALL_ANY_DEST"
        else
            echo "* removing bad symlink \"$HOME/.local/bin/install_any.py\""
            echo "  -> $INSTALL_ANY_DEST"
            echo "  FAILED"
        fi
    fi
fi

if [ ! -L "$HOME/.local/bin/install_any.py" ]; then
    if [ -f "$INSTALL_ANY" ]; then
        if [ ! -d "$HOME/.local/bin" ]; then
            mkdir -p "$HOME/.local/bin"
        fi
        ln -s $INSTALL_ANY $HOME/.local/bin/install_any.py || echo "WARNING: 'ln -s $INSTALL_ANY $HOME/.local/bin/install_any.py' failed."
    else
        echo "Error: missing \"$INSTALL_ANY\""
        exit 1
    fi
else
    echo "* already installed \"$HOME/.local/bin/install_any.py\""
    INSTALL_ANY_DEST="`readlink $HOME/.local/bin/install_any.py`"
    echo "  -> $INSTALL_ANY_DEST"
fi

echo "* finished"
echo
