# Fedora 25 Tips
by expertmm

## Reduce swappiness to 0
(especially for SSD)
* Open sysctl configuration:
```
sudo nano /etc/sysctl.d/99-sysctl.conf
```
* then add:
```
vm.swappiness = 0
```
see also https://ask.fedoraproject.org/en/question/79229/swappiness-setting/
* manually activate using
```
sudo -i
echo 0 > /proc/sys/vm/swappiness
```
see also https://www.dizwell.com/wordpress/technical-articles/linux/fedora-25-performance-tweaks/
* check result via:
```
sysctl -a | grep vm.swappi
```

## Enable Trim for SSD
#from https://www.reddit.com/r/Fedora/comments/43jadh/periodic_ssd_trim_do_i_need_to_do_anything/
#but may not be necessary except under high workloads:
```
systemctl enable fstrim.timer 
```

## GParted won't start
https://www.reddit.com/r/Fedora/comments/5ok5kz/gparted_wont_start/
F22Rapture says:
```
xhost +local:
sudo gparted
```
(running sudo gparted before that may say cannot connect to display)

## Install improved fonts
(since Infinality is stalled--see https://devhen.org/category/fedora/ )
follow the directions at https://github.com/silenc3r/fedora-better-fonts


## Other tips:
* Tether digital camera: https://fedoramagazine.org/tether-digital-camera-fedora/
* PDF Modification (including command line split & join tools): https://fedoramagazine.org/pdf-modification-tools-fedora/


## Expert Multimedia (Developer) setup
#extras and nonfree from rpmfusion:
#click and install the repo packages free and nonfree from https://rpmfusion.org/Configuration/ 

### Management:
sudo dnf install gparted filezilla gnome-tweak-tool pysdm keepassx
#"Tweak Tool" icon allows configuring various aspects of gnome configuration
#"PySDM" is a gui for editing fstab mountpoints
#If KeePass 1 works in your version of Wine, you can manually install Windows version of KeePass 1 (NOTE: only Windows version of keepass 2 has import for KeePass 1, since dll is Windows-only). However, keepassx version 2.xx can import KeePass 1 files, unlike the linux version of KeePass 2.xx
#Install 32-BIT version of Wine to avoid issues (64-bit is not well supported and doesn't run 32-bit windows programs)
sudo dnf remove wine-core
sudo dnf install wine.i686
sudo dnf install winetricks
#(winetricks is a noarch package)
export WINEARCH=win32
export WINEPREFIX=~/win32
winetricks

#### TODO
* set those wine variables for the user at login (workaround: make shell script called winetricks32 containing the two lines:
```
#!/bin/sh
WINEARCH=win32 WINEPREFIX=~/win32 winetricks
```
* then chmod +x winetricks32

#wait for the config window to appear, then:
* Choose default wine prefix, OK
* Choose "Install a Windows DLL or Component", OK
    * MS GDI+ (required for many applications, such as KeePass 1.xx, though KeePass 1 doesn't work on Wine 2.4)
    * MS Setup API
    * MS Visual Basic 6 runtime sp6
    * 
#for some reason, result is: "vb6run install completed, but installed file /home/owner/win32/dosdevices/c:/windows/system32/MSVBVM60.DLL not found"
#after the above commands, wine will be 32-bit, and wine64 will be 64-bit. ~/win32 should be used for the wine prefix for the 32-bit version, and WINEARCH=win32 should be used.
#line below is from https://wiki.winehq.org/Fedora
dnf config-manager --add-repo https://dl.winehq.org/wine-builds/fedora/25/winehq.repo

#owncloud client (below) as per https://software.opensuse.org/download/package?project=isv:ownCloud:desktop&package=owncloud-client (package in fedora/rpmfusion didn't work--client didn't open after successful config--one below worked and picked up that saved login instantly)
sudo dnf config-manager --add-repo http://download.opensuse.org/repositories/isv:ownCloud:desktop/Fedora_25/isv:ownCloud:desktop.repo
sudo dnf install owncloud-client
### Development
sudo dnf install gimp blender geany xterm monodevelop qt-creator kate gitg
#xterm is used by geany such as running python in xterm to execute py file

sudo dnf install -y python-devel ffmpeg-libs SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel portmidi-devel libavdevice libavc1394-devel zlibrary-devel ccache mesa-libGL mesa-libGL-devel
sudo python -m pip install --upgrade pip
sudo python -m pip install cython
sudo python -m pip install --upgrade pip wheel setuptools
sudo python -m pip install docutils pygments
sudo python -m pip install kivy --no-cache-dir
#NOTE: The instructions above are included with IntroCompatiblizer
#for some reason results in:
#Command "/bin/python -u -c "import setuptools, tokenize;__file__='/tmp/pip-build-vm3yeq/kivy/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record /tmp/pip-W9U76r-record/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-build-vm3yeq/kivy/

#### Fedora 26
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
#Now it works!

#### temperature sensor tools for TEMPerV1 devices
```
sudo pip install temperusb
```
##### Now give permission to user
see http://ask.xmodulo.com/change-usb-device-permission-linux.html
```
sudo lsusb -vvv
```
results in lots of info. Find the TEMPer device there in that huge list to get the block of info for your specific device--something like the contents of the file included with this guide: "TEMPerV1 (white, all-in-one) USB device from AMAZON lsusb -vvv.txt"
* yields the necessary info such as:
```
idVendor           0x0c45 Microdia
idProduct          0x7401 TEMPer Temperature Sensor
```
* then create a rules file:
```
sudo nano /etc/udev/rules.d/50-myusb.rules
```
* adding the line (where 0c45 7401 and are your values found above after 0x [hexadecimal] values using sudo lsusb -vvv):
```
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0c45", ATTRS{idProduct}=="7401", GROUP="users", MODE="0666"
```
* then run:
```
#DOESN"T WORK: sudo udevadm control --reload
sudo udevadm control --reload-rules && sudo udevadm trigger
#some GNU/Linux systems use udevtrigger instead of udevadm trigger
```
* now temper should work:
```
temper-poll
```
* should output something like:
```
Found 1 devices
Device #0: 23.8°C 74.8°F
```

### Multimedia:
sudo dnf install vlc smplayer
#h264 as per https://fedoraproject.org/wiki/OpenH264
sudo dnf config-manager --set-enabled fedora-cisco-openh264
sudo dnf install gstreamer1-plugin-openh264 mozilla-openh264
#### DVD:
curl https://www.folkswithhats.org/installer | sudo bash
#FORMERLY bash -c 'su -c "curl https://folkswithhats.org/fedy-installer -o fedy-installer && chmod +x fedy-installer && ./fedy-installer"'
Then you can use Fedy (gui application) to install:
* Utilities:
    * Archive formats
    * Encrypted DVD playback
    * Microsoft TrueType core fonts
    * Multimedia codecs

### Internet
#now follow the instructions for Firefox about:config using the OpenH264 instructions link above
#Install flash:
sudo rpm -ivh http://linuxdownload.adobe.com/adobe-release/adobe-release-x86_64-1.0-1.noarch.rpm
sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-adobe-linux
sudo dnf install flash-plugin alsa-plugins-pulseaudio libcurl
sudo dnf install chromium

### Stuff that didn't work
#### DVD (Use fedy instead--see above)
sudo dnf install libdvdcss
sudo dnf install gstreamer1-libav gstreamer1-plugins-bad-free-extras gstreamer1-plugins-bad-freeworld gstreamer1-plugins-base-tools updates gstreamer1-plugins-good-extras gstreamer1-plugins-ugly gstreamer1-plugins-bad-free gstreamer1-plugins-good gstreamer1-plugins-base gstreamer1 ffmpeg memcoder ffmpeg2theora mplayer libdvdread libdvdnav lsdvd libdvdcss gstreamer-plugins-bad gstreamer-plugins-ugly gstreamer-plugins-base
sudo dnf install gstreamer­ffmpeg gstreamer1­plugins­bad­free­extras gstreamer1­plugins­bad­freeworld gstreamer1­plugsins­base­tools gstreamer1­plugins­good­extras gstreamer1­plugins­ugly gstreamer1­plugins­bad­free gstreamer1­plugins­good gstreamer1­plugins­base
#sudo yum-config-manager --enable rpmfusion-free
#sudo yum-config-manager --enable rpmfusion-free-updates
#sudo yum-config-manager --enable rpmfusion-nonfree
#sudo yum-config-manager --enable rpmfusion-nonfree-updates
sudo yum ­y install libdvdread libdvdnav lsdvd 
sudo dnf install libdvdread libdvdnav lsdvd 
sudo dnf install gstreamer1­plugins­ugly
sudo dnf install gstreamer-plugins-bad gstreamer-plugins-bad-free-extras gstreamer-plugins-bad-nonfree gstreamer-plugins-ugly gstreamer-ffmpeg
sudo dnf install gstreamer-plugins-bad gstreamer-plugins-bad-free-extras gstreamer-plugins-bad-nonfree gstreamer-plugins-ugly gstreamer-ffmpeg
sudo dnf install libdvdread libdvdnav lsdvd 
 
