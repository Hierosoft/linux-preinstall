#!/bin/bash
# As per <https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_local>:
# This version is not on pypi:
me="$0"

WEBINSTALL=false
if [ "@$1" == "@--web" ]; then
	WEBINSTALL=true
	echo "* using web installer."
else
	echo "* downloading full installer."
fi

# The old versions/releases are listed at <https://developer.nvidia.com/cuda-toolkit-archive>.
# 11.3 is the example in the ndviffrec readme (therefore must be known to work)
# so as per <https://developer.nvidia.com/cuda-11-3-1-download-archive?target_os=Linux>
# (only has an ubuntu 20.04 package (*not* 22.04 jammy).
# - To be sure, only use the driver version in the filename of RUPO_DEB_URL
#   below (using 470 didn't work; the cuda package said I held broken packages and that it required 465)
#   - *However*, after that installing 465 had the same error:
cat >/dev/null <<END
The following packages have unmet dependencies:
 xserver-xorg-video-nvidia-465 : Depends: xorg-video-abi-24 but it is not installable or
                                          xorg-video-abi-23 but it is not installable or
                                          xorg-video-abi-20 but it is not installable or
                                          xorg-video-abi-19 but it is not installable or
                                          xorg-video-abi-18 but it is not installable or
                                          xorg-video-abi-15 but it is not installable or
                                          xorg-video-abi-14 but it is not installable or
                                          xorg-video-abi-13 but it is not installable or
                                          xorg-video-abi-12 but it is not installable or
                                          xorg-video-abi-11 but it is not installable or
                                          xorg-video-abi-10 but it is not installable or
                                          xorg-video-abi-8 but it is not installable or
                                          xorg-video-abi-6.0 but it is not installable
END
# run:
# echo $XDG_SESSION_TYPE
# to see whether wayland or x11 is running.
# According to <https://ubuntuforums.org/showthread.php?t=2474289>, xorg must be running not wayland.
# As per [Pop os won't upgrade #370](https://github.com/pop-os/beta/issues/370)
# which mentions the same error, tried:
cat >/dev/null <<END
sudo apt clean
sudo apt update -m
sudo dpkg --configure -a
sudo apt install -f
sudo apt full-upgrade
sudo apt autoremove --purge
sudo apt install nvidia-driver-465
END
# However, the problem is not resolved.
# Only nvidia-driver-470 will install.

# After reboot, it installs.

# The Ubuntu 20 version won't work due to the long xorg dep error above:
#
#
#
#
#
#sudo apt-get update
#sudo apt-get -y install cuda

sudo apt-get remove libnvidia-extra-515 libnvidia-extra-470  nvidia-kernel-common-515 nvidia-kernel-common-470

if [ "@$WEBINSTALL" != "@true" ]; then
# I added --no-clobber.
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: '' failed."; exit $code; fi
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: '' failed."; exit $code; fi
RUPO_DEB_URL="https://developer.download.nvidia.com/compute/cuda/11.3.1/local_installers/cuda-repo-ubuntu2004-11-3-local_11.3.1-465.19.01-1_amd64.deb"
wget --no-clobber $RUPO_DEB_URL
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: '' failed."; exit $code; fi
sudo dpkg -i cuda-repo-ubuntu2004-11-3-local_11.3.1-465.19.01-1_amd64.deb
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: '' failed."; exit $code; fi
sudo apt-key add /var/cuda-repo-ubuntu2004-11-3-local/7fa2af80.pub
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: '' failed."; exit $code; fi
sudo apt-get update
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: '' failed."; exit $code; fi
# sudo apt-get install cuda
# ^ keeps installing 11.7, so:
sudo apt-get -y install cuda-toolkit-11.3
code=$?
if [ $code -ne 0 ]; then
	echo "[$me] Error: '' failed."
	echo "Try running $me with the --web option."
	exit $code
fi
fi
# ^ The offline install doesn't work on Ubuntu 22.04 Jammy, so try the
#   network install:


cat >/dev/null <<END


The network-based install still has:
The following packages have unmet dependencies:
 libnvidia-extra-470 : Conflicts: libnvidia-extra
 libnvidia-extra-515 : Conflicts: libnvidia-extra
 nvidia-kernel-common-470 : Conflicts: nvidia-kernel-common
 nvidia-kernel-common-515 : Conflicts: nvidia-kernel-common
E: Error, pkgProblemResolver::Resolve generated breaks, this may be caused by held packages.

so:

END

if [ "@$WEBINSTALL" == "@true" ]; then
# I added --no-clobber.
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: 'wget' failed."; exit $code; fi
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: 'mv' failed."; exit $code; fi
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: 'apt-key' failed."; exit $code; fi
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
# ^ the --remove option uninstalls it.
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: 'add-apt-repository' failed."; exit $code; fi
sudo apt-get update
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: 'sudo apt-get update' failed."; exit $code; fi
# sudo apt-get install cuda
# ^ keeps installing 11.7, so:
sudo apt-get -y install cuda-toolkit-11.3
code=$?
if [ $code -ne 0 ]; then
	echo "[$me] Error: 'sudo apt-get -y install cuda' failed."
	exit $code
fi
fi

# The 'pip install --global-option="--no-networks" git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch' command shows:
#    OSError: PyTorch CUDA is unavailable. tinycudann requires PyTorch to be installed with the CUDA backend.
#    No CUDA runtime is found, using CUDA_HOME='/usr/local/cuda'
#    Building PyTorch extension for tiny-cuda-nn version 1.6
# So:
sudo update-alternatives --config cuda
if [ $? -ne 0 ]; then
	exit 1
fi
/usr/local/cuda/bin/nvcc --version
# nvidia-smi may still show a different version, but
# that is ok according to Michael Kelzel on <https://stackoverflow.com/questions/53422407/different-cuda-versions-shown-by-nvcc-and-nvidia-smi#comment93719643_53422407>
# who says "nvidia-smi shows you the CUDA version that your driver supports"
# The pip command still yields:
#In file included from /usr/local/cuda/include/cuda_runtime.h:83,
#                     from <command-line>:
#    /usr/local/cuda/include/crt/host_config.h:139:2: error: #error -- unsupported GNU version! gcc versions later than 10 are not supported! The nvcc flag '-allow-unsupported-compiler' can be used to override this version check; however, using an unsupported host compiler may cause compilation failure or incorrect run time execution. Use at your own risk.
#      139 | #error -- unsupported GNU version! gcc versions later than 10 are not supported! The nvcc flag '-allow-unsupported-compiler' can be used to override this version check; however, using an unsupported host compiler may cause compilation failure or incorrect run time execution. Use at your own risk.

# so as per <https://linuxconfig.org/how-to-switch-between-multiple-gcc-and-g-compiler-versions-on-ubuntu-22-04-lts-jammy-jellyfish>:
sudo apt update
sudo apt install -y build-essential
# sudo apt -y install gcc-8 g++-8 gcc-9 g++-9 gcc-10 g++-10
sudo apt -y install gcc-10 g++-10
# sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 10
# ^ not done yet--only for cuda 11.3 and that won't install due to long xorg dependency error further up
echo "gcc --version"
gcc --version
echo "g++ --version"
g++ --version
cat <<END
If either gcc or g++ version are >10 they are not suitable for cuda 11.3 pytorch so as necessary, run:
  sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 10
  sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 10
  # After that, the following should show 10.x:
  g++ --version
  gcc --version
  cc --version
  c++ --version
END
# NOTE: There are no alternatives for gcc.

