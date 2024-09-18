#!/bin/bash

PREFIX=$@
if [ -z $PREFIX ]; then
  PREFIX="/usr/local"
fi

# Ensure you have write permissions to PREFIX
sudo mkdir $PREFIX
sudo chown -R `whoami` $PREFIX

# Ensure that all required packages are installed.
sudo apt-get install git autoconf libtool automake build-essential gettext cmake python

PATH=$PREFIX/bin:$PATH
git clone https://github.com/mono/mono.git
cd mono
./autogen.sh --prefix=$PREFIX
make
make install
