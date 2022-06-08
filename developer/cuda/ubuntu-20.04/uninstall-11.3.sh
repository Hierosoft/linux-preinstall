#!/bin/bash
cat <<END

11.3 requires-unavailable-deprecated-xorg-video-abi
Try uninstalling all components
and rebooting.
END
# As per <https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_local>:
sudo rm /etc/apt/preferences.d/cuda-repository-pin-600
PKG="cuda-repo-ubuntu2004-11-3-local_11.3.1-465.19.01-1_amd64.deb"
echo "* you can now manually remove \"$PKG\""
# rm $PKG
sudo apt-get -y remove cuda
sudo apt-get -y remove cuda-toolkit-11.3
sudo rm /usr/share/keyrings/cuda-*-keyring.gpg

sudo apt remove -y cuda-repo-ubuntu2004-11-3-local
sudo rm /etc/apt/sources.list.d/cuda-ubuntu2004-11-3-local.list
sudo apt-get autoremove -y --purge

# Fix "W: https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/InRelease: Key is stored in legacy trusted.gpg keyring (/etc/apt/trusted.gpg), see the DEPRECATION section in apt-key(8) for details."


sudo apt-get update


cat <<END
If you can't install nvidia-driver-470 or the driver of your choice
after this, try:

sudo apt clean
sudo apt update -m
sudo dpkg --configure -a
sudo apt install -f
sudo apt full-upgrade
sudo apt autoremove --purge
sudo apt install nvidia-driver-470

# Note that even if you get version 465 installed, nvidia-extras-465
from Jammy will conflict with nvidia-extras from the cuda repo so there
is no use in trying 11.3 on Jammy. You have to downgrade to
Ubuntu 20.04 Focal or wait for PyTorch for cuda 11.7 to be released.

END


echo "You will have to manually ensure all of the packages below this line are uninstalled if any."
dpkg -l | awk '/^.i/ {print $2}' | xargs apt-cache policy | awk '/^[a-z0-9.\-]+:/ {pkg=$1}; /\*\*\*/ {OFS="\t"; ver=$2; getline; print pkg,ver,$2,$3}'|grep -v /var/lib/dpkg/status| sed -e 's/://'|awk '{printf "%-40s %-36s %-36s %-16s \n",$1,$2,$3, $4}' | grep -i cuda/repos/ubuntu2004

# ^ based on https://unix.stackexchange.com/a/401625
# ^ returns lines such as:
#   libnvidia-compute-515                    515.48.07-0ubuntu1                   https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64 Packages 

