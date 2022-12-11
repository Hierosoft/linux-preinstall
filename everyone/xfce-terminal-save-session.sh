#!/bin/bash
MY_DIR=`dirname $0`
MY_DIR=`realpath $MY_DIR`
if [ "@$1" != "@--force" ]; then
cat <<END
This script is for installing a version of Xfce Terminal that has the
save session feature, more accurately called the save Tabset feature.

However, the repu1sion fork is really old. The recommended course of
action is to install the oldcoder fork which integrates the repu1sion
feature into a later version of Xfce Terminal:

    <https://laclin.com/xfce4-tabset.html>
    such as via:
    $MY_DIR/xfce4-terminal-tabset-laclin.sh

To install the old repu1sion fork anyway, run
  $0 --force
END
exit 0
fi

REPO_USER=repu1sion
REPO_NAME=xfce4-terminal
REPOS_PATH=~/Downloads/git/$REPO_USER
REPO_PATH=~/Downloads/git/$REPO_USER/$REPO_NAME
REPO_URL=https://github.com/$REPO_USER/$REPO_NAME.git

cat <<END
from <https://github.com/repu1sion/xfce4-terminal/tree/pulseterm/doc>:
  * Make sure you have the xfce-dev-tools, gnome-doc-utils (for xml2po)
    and libxslt (for xsltproc) packages installed.
  * Create a GIT clone; "git clone git://git.xfce.org/apps/terminal".
  * Run "./autogen.sh --enable-gen-doc" and make sure the build
    configuration shows "Generate documentation: yes".
  * Run "make" and "make DESTDIR=/some/prefix install".
END


cat <<END
re xml2po <https://command-not-found.com/xml2po>:
"In new projects, please use the yelp-tools package instead."
END
sudo apt-get install -y xfce4-dev-tools yelp-tools libvte-dev
echo "* INFO: yelp-tools didn't provide an xml2po command."
echo >/dev/null <<END
checking for libxfce4ui-1 >= 4.10.0... not found
*** The required package libxfce4ui-1 was not found on your system.
*** Please install libxfce4ui-1 (atleast version 4.10.0) or adjust
*** the PKG_CONFIG_PATH environment variable if you
*** installed the package in a nonstandard prefix so that
*** pkg-config is able to find it.

but:

sudo apt-get install libxfce4ui-1.0
says:
Note, selecting 'libxfce4ui-1-0' for regex 'libxfce4ui-1.0'
libxfce4ui-1-0 is already the newest version (4.12.1-3).

There is no dev package found via:

(only libxfce4ui-2-dev which says it is for gtk3)
END

if [ $? -ne 0 ]; then exit 1; fi

mkdir -p $REPOS_PATH \
    && cd $REPOS_PATH
if [ $? -ne 0 ]; then exit 1; fi
if [ ! -d "$REPO_PATH" ]; then
    git clone $REPO_URL $REPO_PATH
    if [ $? -ne 0 ]; then exit 1; fi
    cd $REPO_PATH
    if [ $? -ne 0 ]; then exit 1; fi
else
    cd $REPO_PATH
    if [ $? -ne 0 ]; then exit 1; fi
    git pull --no-rebase --verbose
    if [ $? -ne 0 ]; then exit 1; fi
fi
./autogen.sh
if [ $? -ne 0 ]; then exit 1; fi
./configure
if [ $? -ne 0 ]; then exit 1; fi
make
if [ $? -ne 0 ]; then exit 1; fi
suso make install


if [ $? -ne 0 ]; then
    echo
    echo "Error: make install failed. Ensure you're running as root."
    echo
else
    echo
    echo "Done"
    echo
fi
