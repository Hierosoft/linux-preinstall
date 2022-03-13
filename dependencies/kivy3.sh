#!/bin/sh
echo "* tested on Devuan Chimera"
python3 -m pip install --upgrade --user virtualenv
mkdir -p ~/venv
python3 -m virtualenv ~/venv/kity
source ~/venv/kivy/bin/activate
pip install --upgrade pip wheel setuptools

# kivy3 deps:
# NOTE: stl results in "ImportError: cannot import name 'mesh' from 'stl' (/home/owner/venv/kivy/lib/python3.9/site-packages/stl/__init__.py)"
# so install numpy-stl instead.
pip uninstall stl
pip install --upgrade numpy numpy-stl


pip install --upgrade https://github.com/kivy/kivy3/archive/refs/heads/master.zip


# pip install --upgrade kivy[full]
# ^ full has multimedia etc--see <https://kivy.org/doc/stable/gettingstarted/installation.html#install-pip>
# (change cp39 to the correct Python version matching `python --version` after running activate above)
pip install https://github.com/kivy/kivy/releases/download/2.1.0/Kivy-2.1.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# I still get: "File "/usr/lib/python3.9/imghdr.py", line 19, in what
#     location = file.tell()
#     AttributeError: 'NoneType' object has no attribute 'tell'"
cat <<END
INFO: The demo files are not added by the install until the issue is resolved: See issue ['NoneType' has no attribute 'tell' #30](https://github.com/kivy/kivy3/issues/30) on kivy's fork.
END
