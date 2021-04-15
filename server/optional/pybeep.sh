#!/bin/sh
apt install -y python3-pip
# python3 -m pip install --user https://github.com/jas14/pybeep/archive/refs/heads/master.zip
# python3 -m pip uninstall -y pybeep
# python3 -m pip install --user ~/git/pybeep
python3 -m pip install --user https://github.com/poikilos/pybeep/archive/refs/heads/master.zip
# ImportError: /home/owner/.local/lib/python3.7/site-packages/pybeep.cpython-37m-x86_64-linux-gnu.so: undefined symbol: Py_InitModule
