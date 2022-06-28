#!/bin/bash
In the file, write the following line:

destConf="/etc/modprobe.d/nvidia-drm-nomodeset.conf"
printf "* "
if [ -f "$destConf" ]; then
    printf "over"
fi
echo "writing \"$destConf\""
echo 'options nvidia-drm modeset=1' | sudo tee $destConf
echo "* update-initramfs -u..."
sudo update-initramfs -u
echo
echo "xrandr output:"
xrandr
cat <<END
Now reboot and run (requires proprietary NVIDIA driver and you still may need to turn on vsync and buffered both in the NVIDIA settings GUI):
  sudo nvidia-settings --assign CurrentMetaMode="DVI-I-1:1920x1080_60 +0+0 { ForceFullCompositionPipeline = On }"
  # but replace DVI-I-1 with the "connected" device in the xrandr output above.
END
