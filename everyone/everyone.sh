#!/bin/sh
source /etc/os-release

dnf -y install evince
#evince: (aka "Document Viewer") pdf viewer better than okular

vid_conf_type="radeon"
vid_conf=
if [ -f /etc/X11/xorg.conf.d/10-radeon.conf ]; then
    vid_conf=/etc/X11/xorg.conf.d/10-radeon.conf
elif [ -f /etc/X11/xorg.conf.d/20-radeon.conf ]; then
    vid_conf=/etc/X11/xorg.conf.d/20-radeon.conf
elif [ -f /usr/share/X11/xorg.conf.d/20-intel.conf ]; then
    vid_conf=/usr/share/X11/xorg.conf.d/20-intel.conf
    vid_conf_type="intel"
elif [ -f /usr/share/X11/xorg.conf.d/10-intel.conf ]; then
    vid_conf=/usr/share/X11/xorg.conf.d/10-intel.conf
    vid_conf_type="intel"
else
    vid_conf_type="unknown"
    vid_conf="/usr/share/X11/xorg.conf.d/??-<your video card brand>.conf"
fi

cat <<END
1. In Terminal:

    sudo nano $vid_conf


2. Then add the TearFree setting so your conf looks similar to below:

END

if [ "@$vid_conf_type" = "@intel" ]; then
    cat <<END
Section "Device"
    Identifier "Intel Graphics"
    Driver "intel"
    Option "AccelMethod" "sna"
    Option "TearFree" "true"
    Option "DRI" "3"
EndSection

# sna may increase CPU load--uxa can fix additional screen tearing in
  Skype, but is a downgrade. See
  https://askubuntu.com/questions/752743/ubuntu-16-04-skylake-6th-generation-screen-flickering
END
elif [ "@$vid_conf_type" = "@radeon" ]; then
    cat <<END
Section "Device"
    Identifier "Radeon"
    Driver "radeon"
    Option "TearFree" "on"
EndSection
END
else
    cat <<END
    Option "TearFree" "on"
END
fi



echo
