#!/bin/bash

# To find your ubuntu codename under Linux Mint, type:
#  cat /etc/os-release
#  # Then consult https://askubuntu.com/questions/445487/what-debian-version-are-the-different-ubuntu-versions-based-on
#  #   for version number (and Debian codename if necessary, such as for repos that only have debian not ubuntu codenames)

# Microsoft recommends switching to https://github.com/dotnet/core, or https://github.com/dotnet/runtime/tree/main/src/mono for old apps
# - 3.0 or above has Windows.Forms
# - but Windows Forms names have changed, so compiling old Windows Forms applications will not work out of the box.
#   - Port using documentation at <https://learn.microsoft.com/en-us/dotnet/core/compatibility/winforms#removed-controls>
#     as discussed here: <https://stackoverflow.com/a/59954655>

# First, install old version, since it is required in order to build the new version:

# Based on <https://www.liberiangeek.net/2024/04/install-mono-on-ubuntu-24-04/>
sudo apt install -y apt-transport-https dirmngr
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
# ^ says to use:
#   deb https://download.mono-project.com/repo/ubuntu vs-bionic main
#   - 18.04
# but <https://www.mono-project.com/download/stable/#download-lin> says to use
#   deb [signed-by=/usr/share/keyrings/mono-official-archive-keyring.gpg] https://download.mono-project.com/repo/ubuntu stable-focal main
#   - 20.04
#   - No later versions are listed at <https://download.mono-project.com/repo/ubuntu/dists/index.html>.
if [ -f /etc/apt/sources.list.d/mono-official-vs.list ]; then
	sudo mkdir -p /etc/apt/sources.list.disabled
    sudo mv /etc/apt/sources.list.d/mono-official-vs.list /etc/apt/sources.list.disabled/
fi
echo "deb https://download.mono-project.com/repo/ubuntu stable-focal main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list
sudo apt update
sudo apt install mono-devel

# OR:

# > If you don't have a working Mono installation, you can try a slightly more risky approach: getting the latest version of the 'monolite' distribution, which contains just enough to run the 'mcs' compiler. You do this with:
# > Run the following line after ./autogen.sh
# > make get-monolite-latest
#
# -<https://gitlab.winehq.org/mono/mono>

# ./autogen.sh says we need ... "to compile Mono.":
# autoconf libtoolize automake
# also says cmake is not found and ends early if not present
# NOTE: apt-cache rdepends cmake
# says cmake can be installed via: any of packaging-dev qtcreator multimedia-devel kdevelop [or others]
sudo apt install -y autotools-dev autoconf libtool cmake

# To find build-deps, Open "Software Sources" turn on "Source code repositories"
#  as per <https://askubuntu.com/questions/496549/error-you-must-put-some-source-uris-in-your-sources-list>
#  (NOTE: `sudo cp --no-clobber /etc/apt/sources.list /etc/apt/sources.list~ && sudo sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list` doesn't work anymore. The new location is 'sources.list.d/official-source-repositories.list')
#  then
#  as discussed at <https://askubuntu.com/questions/21379/how-do-i-find-the-build-dependencies-of-a-package>:
# sudo apt install -y apt-rdepends
# # apt-rdepends --build-depends mono  # *VERY* long output. Maybe pipe to `| uniq -u`?
# # apt-rdepends --build-depends --print-state mono | grep NotInstalled  # also *VERY* long output. Maybe pipe to `| uniq -u`?
# apt-rdepends --build-depends --follow=none mono
# NOTE: ^ none in --follow=none is a workaround (none is not a valid symbol, so all recursion is avoided)
# Result:
sudo apt install -y autoconf automake bison cmake dc debhelper dpkg-dev libkrb5-dev libtool libx11-dev libxml-dom-perl libxslt1-dev libxt-dev lsb-release procps python3 tzdata zlib1g-dev
# <https://www.mono-project.com/docs/compiling-mono/linux/> says:
# (See /opt/git/linux-preinstall/utilities-developer/build-mono.sh for a copy of their Debian mono build script)
sudo apt install -y git autoconf libtool automake build-essential gettext cmake python3 curl
# or try:
# sudo apt-get --simulate build-dep mono
# or:
# apt showsrc mono | grep '^Build-Depends'

# Then compile as per <https://gitlab.winehq.org/mono/mono>:

sudo mkdir -p /opt/git
THIS_GROUP=`id -nG | awk '{print $1}'`
sudo chown $USER:$THIS_GROUP /opt/git
if [ ~ -d /opt/git/mono ]; then
	git clone https://gitlab.winehq.org/mono/mono /opt/git/mono
	cd /opt/git/mono || exit 1
else
	cd /opt/git/mono || exit 1
	git pull
fi
# ./autogen.sh

#   but change PREFIX as per <https://www.mono-project.com/docs/compiling-mono/linux/>!
PREFIX="/usr/local"
sudo mkdir -p $PREFIX
sudo chown -R `whoami` $PREFIX
PATH=$PREFIX/bin:$PATH
echo
echo
echo "Running \"./autogen.sh\"..."
./autogen.sh --prefix=$PREFIX
code=$?
if [ $code -ne 0 ]; then
	echo "\"./autogen.sh\" failed in `pwd` with code $code"
	exit $code
fi
echo
echo
echo "Running \"make\"..."
make
code=$?
if [ $code -ne 0 ]; then
	echo "\"make\" failed in `pwd` with code $code"
	exit $code
fi
echo
echo
echo "Running \"make check\"..."
make check
code=$?
if [ $code -ne 0 ]; then
	echo "\"make check\" failed in `pwd` with code $code"
	exit $code
fi

echo
echo "Running \"sudo make install\"..."
GIT_HASH=$(git rev-parse --short HEAD)
sudo make install | tee ~/mono-$GIT_HASH.manifest.txt
code=$?
if [ $code -ne 0 ]; then
	echo "\"make install\" failed in `pwd` with code $code"
	exit $code
fi
