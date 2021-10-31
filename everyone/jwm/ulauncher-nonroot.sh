#!/bin/bash

REPO_USER=Ulauncher
REPO_NAME=Ulauncher
DEST_DIR_NAME=ulauncher
REPO_URL=https://github.com/$REPO_USER/$REPO_NAME
VENV_PATH="$HOME/venv/$DEST_DIR_NAME"

mkdir -p ~/Downloads/git/$REPO_USER
cd ~/Downloads/git/$REPO_USER
if [ $? -ne 0 ]; then
    echo "Error: 'cd ~/Downloads/git/$REPO_USER' failed."
    exit 1
fi

if [ ! -d "$REPO_NAME" ]; then
    git clone $REPO_URL $REPO_NAME
    if [ $? -ne 0 ]; then
        echo "Error: 'git clone $REPO_URL $REPO_NAME' failed in \"`pwd`\"."
        exit 1
    fi
    cd "$REPO_NAME"
    if [ $? -ne 0 ]; then
        echo "Error: 'cd \"$REPO_NAME\"' failed in \"`pwd`\"."
        exit 1
    fi
else
    cd "$REPO_NAME"
    if [ $? -ne 0 ]; then
        echo "Error: 'cd \"$REPO_NAME\"' failed in \"`pwd`\"."
        exit 1
    fi
    git pull --ff-only
    if [ $? -ne 0 ]; then
        echo "Warning: 'git pull' failed in \"`pwd`\"."
    fi
fi

#git fetch
#git checkout dev

mkdir -p ~/.local/bin
mkdir -p ~/.local/lib
if [ ! -d ~/.local/lib/Ulauncher ]; then
    cp -R ../Ulauncher ~/.local/lib/
else
    printf "* updating ~/.local/lib/Ulauncher from ../Ulauncher/..."
    rsync -rt --delete ../Ulauncher/ ~/.local/lib/Ulauncher
    if [ $? -ne 0 ]; then
        echo "Warning: 'rsync -rt --delete ../Ulauncher/ ~/.local/lib/Ulauncher' failed in \"`pwd`\"."
    else
        echo "OK"
    fi
fi

mkdir -p $HOME/venv

if [ ! -d "$VENV_PATH" ]; then
    python3 -m venv "$VENV_PATH"
    if [ $? -ne 0 ]; then
        echo "Error: 'cd \"$REPO_NAME\"' failed in \"`pwd`\"."
        exit 1
    fi

    source $VENV_PATH/bin/activate
    python -m pip install --upgrade pip wheel setuptools
    python -m pip install --upgrade levenshtein
    #python -m pip install --upgrade websocket

    #python -m pip install -r requirements.txt
    # ^ fails on mypy==0.701
    python -m pip install mock==2.0.0
    python -m pip install pytest==5.2.0
    python -m pip install pytest-mock==3.3.1
    python -m pip install pylint==2.3.1
    python -m pip install mypy
    python -m pip install mypy_extensions
    python -m pip install flake8==3.7.7

    python -m pip install gobject PyGObject
    python -m pip install dbus-python
    python -m pip install pyxdg
    python -m pip install pyinotify
    python -m pip install ~/.local/lib/Ulauncher
    # ^ (See pip warning in the failure state below)
    # ^ fails with:
    cat > /dev/null <<END
  DEPRECATION: A future pip version will change local packages to be built in-place without first copying to a temporary directory. We recommend you use --use-feature=in-tree-build to test your packages with this new behavior before it becomes the default.
   pip 21.3 will remove support for this functionality. You can find discussion regarding this at https://github.com/pypa/pip/issues/7555.
    ERROR: Command errored out with exit status 1:
     command: /home/owner/venv/ulauncher/bin/python3 -c 'import io, os, sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-req-build-jjrja6_a/setup.py'"'"'; __file__='"'"'/tmp/pip-req-build-jjrja6_a/setup.py'"'"';f = getattr(tokenize, '"'"'open'"'"', open)(__file__) if os.path.exists(__file__) else io.StringIO('"'"'from setuptools import setup; setup()'"'"');code = f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' egg_info --egg-base /tmp/pip-pip-egg-info-s301s4zp
         cwd: /tmp/pip-req-build-jjrja6_a/
    Complete output (1 lines):
    To build ulauncher you need "python3-distutils-extra"
    ----------------------------------------
WARNING: Discarding file:///home/owner/Downloads/git/Ulauncher/Ulauncher. Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output.
ERROR: Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output.
END
    # See [Problems installing from AUR with pyenv in use #820](https://github.com/Ulauncher/Ulauncher/issues/820)
    deactivate
fi

mkdir -p ~/.var/log/
echo '#/bin/sh' > $HOME/.local/bin/ulauncher
echo "$HOME/venv/ulauncher/bin/python $HOME/.local/lib/Ulauncher/bin/ulauncher > ~/.var/log/ulauncher.log 2>&1" >> $HOME/.local/bin/ulauncher
chmod +x $HOME/.local/bin/ulauncher

source ~/venv/ulauncher/bin/activate

cat <<END

1. You must add the following to startup:
    $HOME/.local/bin/ulauncher

    # Note that the following doesn't work and is available only as a work-in-progress (WIP) idea:
    # sudo cp -f etc/init.d/net.launchpad.ulauncher /etc/init.d/net.launchpad.ulauncher
    # then restart or run: sudo service ulauncher start

2. You must add the following to a shortcut:
    $HOME/.local/lib/Ulauncher/bin/ulauncher-toggle

You can expect ulauncher-toggle to work but show the following error if you have an OS that doesn't use systemd:

* (always ignore this error) "Error org.freedesktop.DBus.Error.ServiceUnknown: The name net.launchpad.ulauncher was not provided by any .service files"

END
