#!/bin/bash
cd
if [ ! -d Downloads ]; then
  mkdir Downloads
fi
#2018-07-17 version for Python 3.6:
#wget http://buildbot.panda3d.org/downloads/71e18eb9606fe9da975858c9a877bc62c46a80d0/panda3d-1.10.0.dev1690-cp36-cp36m-manylinux1_x86_64.whl
#2018-07-17 version for Python 3.7:
#wget http://buildbot.panda3d.org/downloads/71e18eb9606fe9da975858c9a877bc62c46a80d0/panda3d-1.10.0.dev1690-cp37-cp37m-manylinux1_x86_64.whl
#Automatically choose correct version:
sudo python3 -m pip install --pre --extra-index-url https://archive.panda3d.org/ panda3d
echo
echo "Usually installs to:"
echo "  /usr/local/lib64/python3.6/site-packages/panda3d"
echo
