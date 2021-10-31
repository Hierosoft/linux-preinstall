#!/bin/bash

sudo apt-get install -y python3-distutils-extra
if [ $? -ne 0 ]; then
    exit 1
fi

# for the gobject and PyGObject pip packages (imported as "gi"--See
# <https://askubuntu.com/questions/80448/what-would-cause-the-gi-module-to-be-missing-from-python>)
cat > /dev/null <<END
File "/home/owner/Downloads/git/Ulauncher/Ulauncher/bin/ulauncher", line 27, in <module>
    from ulauncher.main import main
  File "/home/owner/Downloads/git/Ulauncher/Ulauncher/ulauncher/main.py", line 11, in <module>
    import gi
ModuleNotFoundError: No module named 'gi'
END
sudo apt-get install -y pkg-config libcairo2-dev gcc python3-dev libgirepository1.0-dev
if [ $? -ne 0 ]; then
    exit 1
fi

sudo apt-get install -y wmctrl
# ^ Used by $HOME/Downloads/git/Ulauncher/Ulauncher/bin/ulauncher-toggle
if [ $? -ne 0 ]; then
    exit 1
fi


echo
echo $0 completed successfully.

echo "INFO: You can use xfce4-appfinder (a backend used by whiskermenu!) instead of ulauncher."
echo
