#!/bin/bash
cat <<END

Now you must manually:
- Install the proprietary nvidia driver version mentioned in the URL:
  $RUPO_DEB_URL
- Then run whichever step2 file is most appropriate:
END
ls step2-*.sh

cat <<END
if it is not working:

Prune old kernels as per:
https://www.tecmint.com/remove-old-kernel-in-debian-and-ubuntu/

If monitor isn't detected,
https://www.tecmint.com/remove-old-kernel-in-debian-and-ubuntu/
find the required mininum driver version
for the version of CUDA at:
<https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html>
then install NVIDIA proprietary driver
as per <https://linuxconfig.org/how-to-install-the-nvidia-drivers-on-ubuntu-22-04>
or DraugerOS-specific instructions at:
<https://www.reddit.com/r/DraugerOS/comments/pac56e/how_to_install_nvidia_drivers_for_the_first_time/>
(replace the driver version with whatever
version is recommended by 'ubuntu-drivers devices'
that is high enough for the CUDA toolkit version according
to the chart on the other web page).
- However, installing the recommended one doesn't allow installing the cuda
  package. Install the version recommended by the cuda package instead
  (the one in the name such as 465 in "cuda-repo-ubuntu2004-11-3-local_11.3.1-465.19.01-1_amd64.deb" above.

gcc 10 has been installed. If the cuda toolkit version is 11.3, first do:
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 10

reboot

END
