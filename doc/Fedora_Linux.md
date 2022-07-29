# Fedora Linux
by Jake Gustafson

These Fedora tips were written for Fedora 25, and have notes on
Fedora 26.

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
See [developer/Fedora_Linux-developer.md](developer/Fedora_Linux-developer.md)

## Kivy
See [Kivy.md](Kivy.md)

### Multimedia:
```
sudo dnf install vlc smplayer
#h264 as per https://fedoraproject.org/wiki/OpenH264
sudo dnf config-manager --set-enabled fedora-cisco-openh264
sudo dnf install gstreamer1-plugin-openh264 mozilla-openh264
#### DVD:
curl https://www.folkswithhats.org/installer | sudo bash
#FORMERLY bash -c 'su -c "curl https://folkswithhats.org/fedy-installer -o fedy-installer && chmod +x fedy-installer && ./fedy-installer"'
```

Then you can use Fedy (GUI application) to install utilities:
* Archive formats
* Encrypted DVD playback
* Microsoft TrueType core fonts
* Multimedia codecs

### Internet
Now follow the instructions for Firefox about:config using the OpenH264 instructions link above

Install flash (deprecated):
```
sudo rpm -ivh http://linuxdownload.adobe.com/adobe-release/adobe-release-x86_64-1.0-1.noarch.rpm
sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-adobe-linux
sudo dnf install flash-plugin alsa-plugins-pulseaudio libcurl
sudo dnf install chromium
```

### Stuff that didn't work
#### DVD
(Use Fedy instead--see above)
``
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
```
