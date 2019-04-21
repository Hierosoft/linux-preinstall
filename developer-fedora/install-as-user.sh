#!/bin/sh
if [ ! -f "`command -v git-cola`" ]; then
  python3 -m pip install https://github.com/git-cola/git-cola/zipball/master --user
  # with --user option, this installs launch script to /home/owner/.local/bin/git-cola
fi
# flatpak install gimp

# see <https://askubuntu.com/questions/237942/how-does-copy-paste-work-with-xterm>
# (also mentions that apparently Shift+Ins or Shift+Middle Click works in some cases without the setting below)
touch ~/.Xresources
echo "XTerm*selectToClipboard: true" >> ~/.Xresources
xrdb -merge ~/.Xresources
cat <<END
Manual steps needed:
* Firefox plugin
* Blender Fiber Mesh: see also <https://blenderartists.org/t/fiber-mesh-resurrected-for-2-80/1141872>
  Install via User Preferences, Addons, Install in Blender
END
cd
if [ ! -d ~/Downloads/git/amadvance ]; then mkdir ~/Downloads/git/amadvance; fi
cd ~/Downloads/git/amadvance
# includes scalerx command (resize png while preserving edge shape):
git clone https://github.com/amadvance/scale2x.git
cd scale2x
./autogen.sh
./configure
make
