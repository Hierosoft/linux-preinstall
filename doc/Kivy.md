# Kivy

For updated instructions on installing Kivy, see
- [kivy.org/doc/stable/gettingstarted/installation.html](https://kivy.org/doc/stable/gettingstarted/installation.html#install-pip)

For potentially easier steps, see:
- [Installing Kivy](https://expertmultimedia.com/usingpython/py3/installing-kivy.html) on [expertmultimedia.com/usingpython](https://expertmultimedia.com/usingpython/)


## Fedora
The following steps are known to work on Fedora (tested on Fedora 26):
```
#see https://stackoverflow.com/questions/41925585/gcc-error-usr-lib-rpm-redhat-redhat-hardened-cc1-no-such-file-or-directory -- tried:
#On Fedora 26:
sudo dnf install redhat-rpm-config
#sudo python -m pip install kivy --no-cache-dir
#results in error still--see "Fedora 26 pip install kivy cython error.txt"
#kivy.org says to install khrplatform-devel which isn't in Fedora 26 or rpmfusion Fedora 26, so
#tried installing a khronos package that may be comparable (only package found via dnf search khr):
sudo dnf install android-opengl-api
#but that has no effect, so tried:
#sudo dnf search svg
#so installed:
sudo dnf install python-pygal python3-pygal python2-scour python3-scour
#so tried:
sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install cython
sudo python3 -m pip install --upgrade pip wheel setuptools
sudo python3 -m pip install docutils pygments
#sudo python3 -m pip install kivy --no-cache-dir
#results in error--see "Fedora 26 python3 pip install kivy cython error.txt"
#NOTE: "fatal error: Python.h: No such file or directory"
#so as per https://stackoverflow.com/questions/21530577/fatal-error-python-h-no-such-file-or-directory tried:
sudo dnf install python2-devel
sudo dnf install python3-devel
#sudo python -m pip install kivy --no-cache-dir
#(still results in same error as before)
#sudo python3 -m pip install kivy --no-cache-dir
#(now has same error as python 2)
#see https://github.com/kivy/kivy/issues/5228
#realized Cython was not installed, so:
#(version avail via dnf search Cython was 0.25.2-4)
sudo dnf install python2-Cython
sudo dnf install python3-Cython
sudo python -m pip install kivy --no-cache-dir
sudo python3 -m pip install kivy --no-cache-dir
```

### Stuff that didn't work
```
sudo dnf install -y python-devel ffmpeg-libs SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel portmidi-devel libavdevice libavc1394-devel zlibrary-devel ccache mesa-libGL mesa-libGL-devel
sudo python -m pip install --upgrade pip
sudo python -m pip install cython
sudo python -m pip install --upgrade pip wheel setuptools
sudo python -m pip install docutils pygments
sudo python -m pip install kivy --no-cache-dir
```
- `xterm` is used by geany such as running python in xterm to execute py file


NOTE: The instructions above are included with [IntroCompatiblizer](https://github.com/poikilos/IntroCompatiblizer) but IntroCompatiblizer works much more quickly with [kivy-tkinter](https://github.com/poikilos/kivy-tkinter).

For some reason the instructions may produce
`Command "/bin/python -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-vm3yeq/kivy/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-W9U76r-record/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-build-vm3yeq/kivy/`

