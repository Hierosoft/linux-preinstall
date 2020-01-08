#!/bin/bash


installTesting(){
    # See https://devtalk.nvidia.com/default/topic/1066408/linux/can-t-build-390-xx-drivers-on-fedora-30/
    dnf update -y --enablerepo=rpmfusion-nonfree-updates-testing xorg-x11-drv-nvidia\*
    akmods --force
}


# See https://linuxconfig.org/how-to-install-the-nvidia-drivers-on-fedora-31
# echo "This is only for 200 Series or similar cards"
# sleep 4
dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
dnf install -y https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

DESCRIPTION=`lspci -vnn | grep VGA`

cat <<END

Your card is:
$DESCRIPTION

1.
For recent GeForce/Quadro/Tesla execute:
  dnf install -y --refresh akmod-nvidia
For Legacy GeForce 400/500 execute:
  dnf install -y --refresh xorg-x11-drv-nvidia-390xx akmod-nvidia-390xx
For Legacy GeForce 8/9/200/300 execute:
  dnf install -y --refresh xorg-x11-drv-nvidia-340xx akmod-nvidia-340xx

2.
  akmods --force

3. If #3 shows an error building, run:
  dnf update -y --enablerepo=rpmfusion-nonfree-updates-testing xorg-x11-drv-nvidia\*
  # (See See https://linuxconfig.org/how-to-install-the-nvidia-drivers-on-fedora-31)

END

# dnf install -y --refresh xorg-x11-drv-nvidia-340xx akmod-nvidia-340xx
#akmods --force || installTesting
