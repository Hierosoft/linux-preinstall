#!/bin/sh

# Dependencies according to <https://aur.archlinux.org/packages/signal-desktop-beta-bin/>
# (or <https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=signal-desktop-beta-bin>):
cat > /dev/null <<END
gtk2 (gtk2-patched-gdkwin-nullcheck, gtk2-ubuntu, gtk2-git, gtk2-minimal-git, gtk2-patched-filechooser-icon-view)
libnotify (libnotify-gtk2, libnotify-id-git, libnotify-id)
libxss
libxtst
nss (nss-hg)
xdg-utils (mimi-git, sx-open, busking-git, xdg-utils-git, linopen, xdg-utils-terminal-true-git, xdg-utils-mimeo, xdg-utils-handlr, xdg-utils-slock, mimi-bachoseven-git, mimejs-git)
END
dnf install -y gtk2 libnotify libxss libxtst nss xdg-utils


exit 0

# ONLY if from source:

if [ ! -f "`command -v node`" ]; then
    dnf install -y nodejs
    # ^ does install npm
fi
if [ ! -f "`command -v git`" ]; then
    dnf install -y git
fi

mkdir -p "$HOME/Downloads/yarn"
cd "$HOME/Downloads/yarn"
if [ $? -ne 0 ]; then
    echo "cd \"$HOME/Downloads/yarn\" failed."
    exit 1
fi
wget -O install.sh https://yarnpkg.com/install.sh
chmod +x install.sh
./install.sh
