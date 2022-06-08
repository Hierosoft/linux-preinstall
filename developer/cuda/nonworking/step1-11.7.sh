#!/bin/bash
# As per <https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_local>:
# This version is not on pypi:
me="$0"

cat >/dev/null <<END
If install cuda fails, there may be a merge list error
during apt-get- update so as per <https://askubuntu.com/a/30199> run:
END
sudo rm -vf /var/lib/apt/lists/*
sudo apt-get update
# That didn't help, so:
sudo apt-get remove cuda-repo-ubuntu2204-11-7-local
mkdir ~/Desktop/nvidia-broken
sudo mv /etc/apt/sources.list.d/archive_uri-https_developer_download_nvidia_com_compute_cuda_repos_ubuntu2204_x86_64_-strigoi.list ~/Desktop/nvidia-broken/
sudo chown -R owner:owner ~/Desktop/nvidia-broken/
# ^ still doesn't help, but does remove an extra file there (probably from cuda 11.3)

# I added --no-clobber.
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: '' failed."; exit $code; fi
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: '' failed."; exit $code; fi
RUPO_DEB_URL="https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda-repo-ubuntu2204-11-7-local_11.7.0-515.43.04-1_amd64.deb"
wget --no-clobber $RUPO_DEB_URL
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: '' failed."; exit $code; fi
sudo dpkg -i cuda-repo-ubuntu2204-11-7-local_11.7.0-515.43.04-1_amd64.deb
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: '' failed."; exit $code; fi
sudo cp /var/cuda-repo-ubuntu2204-11-7-local/cuda-*-keyring.gpg /usr/share/keyrings/
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: '' failed."; exit $code; fi
sudo apt-get update
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: '' failed."; exit $code; fi
sudo apt-get -y install cuda
code=$?
if [ $code -ne 0 ]; then
	echo "[$me] Error: '' failed."
	exit $code
fi



# The 'pip install --global-option="--no-networks" git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch' command shows:
#    OSError: PyTorch CUDA is unavailable. tinycudann requires PyTorch to be installed with the CUDA backend.
#    No CUDA runtime is found, using CUDA_HOME='/usr/local/cuda'
#    Building PyTorch extension for tiny-cuda-nn version 1.6
# So:
sudo update-alternatives --config cuda
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


