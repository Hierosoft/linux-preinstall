#!/bin/bash
# Dependencies for OpenDungeons-0.7.1-Linux64 on
# Linux Mint 22.1 Xia
# - based on Ubuntu 24.04 noble based on trixie/sid
# Fix "opendungeons.x86_64: error while loading shared libraries: libzzip-0.so.13: cannot open shared object file: No such file or directory":
echo "Warning: OpenDungeons is no longer maintained. Consider installing OpenDungeonsPlus instead."
sudo apt-get install libzzip-0-13
cd ~/Downloads/OpenDungeons-0.7.1-Linux64/
./opendungeons.x86_64




