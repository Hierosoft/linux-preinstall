#!/bin/sh
sudo apt install -y python3-kivy
sudo apt install -y geany
sudo apt install -y automake autoconf
sudo apt install -y git
sudo apt install -y mercurial
sudo apt install -y mono-complete

# Packages no longer available as of 18.04:
# - monodevelop: see mono-complete instead
# - kivy-examples
# - qcake

#some common development packages are in UNIVERSE including: mercurial maven2 qcake

#qcake: 3D game maker for PLIB(TM) (you can release games with QCake-Player)


#little to no effect:
#owner@login:/usr/bin$ geany -g kivy.py.tags /usr/lib/python3.4/asyncio/*.py /usr/lib/python3.4/collections/*.py /usr/lib/python3.4/dbm/*.py /usr/lib/python3.4/distutils/*.py /usr/lib/python3.4/encodings/*.py /usr/lib/python3.4/idlelib/*.py /usr/lib/python3.4/importlib/*.py /usr/lib/python3.4/tkinter/*.py /usr/lib/python3.4/*.py /usr/lib/python3/dist-packages/kivy/lib/osc/*.py /usr/lib/python3/dist-packages/kivy/uix/*.py /usr/lib/python3/dist-packages/kivy/*.py
