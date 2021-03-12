#!/bin/bash

declare -A vendors
vendors[dockbarx]=M7S
vendors[xfce4-dockbarx-plugin]=TiZ-EX1

#for program in M7S xfce4-dockbarx-plugin
#do
#    vendor=${vendors[program]}
# ^ doesn't work
for program in "${!vendors[@]}"
do
    echo "* Updating $program"
    vendor="${vendors[$program]}"
    mkdir -p ~/Downloads/git/$vendor
    cd "$HOME/Downloads/git/$vendor"
    printf "* cd \"$HOME/Downloads/git/$vendor\"..."
    if [ $? -ne 0 ]; then
        echo "FAILED"
        exit 1
    else
        echo "OK"
    fi
    if [ ! -d $program ]; then
        printf "* 'git clone https://github.com/$vendor/$program.git' in \"`pwd`\"..."
        git clone https://github.com/$vendor/$program.git
        if [ $? -ne 0 ]; then
            echo "FAILED"
            exit 1
        else
            echo "OK"
        fi
        cd "$program"
        if [ $? -ne 0 ]; then
            echo "Error: 'cd \"$program\"' failed."
            exit 1
        fi
    else
        cd "$program"
        if [ $? -ne 0 ]; then
            echo "Error: 'cd \"$program\"' failed."
            exit 1
        fi

        if [ $? -ne 0 ]; then
            echo "Error: 'git pull' failed in \"`pwd`\"."
            exit 1
        fi
    fi
done

cd "$HOME/Downloads/git/M7S/dockbarx"
if [ $? -ne 0 ]; then
    echo "Error: 'cd \"$HOME/Downloads/git/M7S/dockbarx\"' failed."
fi
git fetch
git checkout -b pygi-python3 origin/pygi-python3
which dockx
# ^ returns 0 only if present
#sudo ./setup.py install
code=$?
printf "* dockx install..."
if [ $code -ne 0 ]; then
    echo "FAILED ('sudo ./setup.py install' in `pwd`)"
    exit 1
else
    echo "OK"
fi
# vendor="xuzhen"
vendor="poikilos"
repos="$HOME/Downloads/git/$vendor"
if [ "$vendor" = "poikilos" ]; then
    repos="$HOME/git"
else
    mkdir -p $HOME/Downloads/git/$vendor
fi
echo "* Installing $vendor's python3 fork of abandoned xfce4-dockbarx-plugin..."
cd "$repos"
if [ $? -ne 0 ]; then
    echo "Error: 'cd \"$repos\"' failed."
fi
if [ ! -d xfce4-dockbarx-plugin ]; then
    git clone https://github.com/$vendor/xfce4-dockbarx-plugin.git
    if [ $? -ne 0 ]; then
        echo "Error: 'git clone https://github.com/vendor/xfce4-dockbarx-plugin.git' failed in `pwd`."
        exit 1
    fi
    cd xfce4-dockbarx-plugin
    if [ $? -ne 0 ]; then
        echo "Error: 'cd xfce4-dockbarx-plugin' failed in `pwd`."
        exit 1
    fi
else
    cd xfce4-dockbarx-plugin
    if [ $? -ne 0 ]; then
        echo "Error: 'cd xfce4-dockbarx-plugin' failed in `pwd`."
        exit 1
    fi
    git pull
    if [ $? -ne 0 ]; then
        echo "WARNING: 'git pull' failed in `pwd`."
        echo "* continuing anyway..."
    fi
fi
./waf configure --prefix=/usr
# ^ The panel will probably not detect the plugin unless you install it in the /usr prefix, so instead do the configure step with ./waf configure --prefix=/usr If you are using a distribution that supports checkinstall, you can replace the install step with sudo ./waf checkinstall to install it in your package manager.
code=$?
if [ $code -ne 0 ]; then
    echo "Error: ./waf configure --prefix=/usr' failed in `pwd`."
    exit $code
fi
./waf build
sudo ./waf install
