#!/bin/sh
customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
# VirtualBox-Extensions-Pack enables USB 2&3
#I had this issue:
#License accepted. For batch installaltion add
#--accept-license=56be48f923303c8cababb0bb4c478284b688ed23f16d775d729b89a2e8e5f9eb
#to the VBoxManage command line.

#0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
#Successfully installed "Oracle VM VirtualBox Extension Pack".
#[owner@pgs student]$ VBoxManage list extpacks
#WARNING: The vboxdrv kernel module is not loaded. Either there is no module
         #available for the current kernel (5.0.16-200.fc29.x86_64) or it failed to
         #load. Please try load the kernel module by executing as root

           #dnf install akmod-VirtualBox kernel-devel-5.0.16-200.fc29.x86_64
           #akmods --kernels 5.0.16-200.fc29.x86_64 && systemctl restart systemd-modules-load.service

         #You will not be able to start VMs until this problem is fixed.
#Extension Packs: 1
#Pack no. 0:   Oracle VM VirtualBox Extension Pack
#Version:      5.2.30
#Revision:     130521
#Edition:
#Description:  USB 2.0 and USB 3.0 Host Controller, Host Webcam, VirtualBox RDP, PXE ROM, Disk Encryption, NVMe.
#VRDE Module:  VBoxVRDP
#Usable:       true
#Why unusable:
#[owner@pgs student]$ sudo akmods --kernels 5.0.16-200.fc29.x86_64 && sudo systemctl restart systemd-modules-load.service
#Could not find files needed to compile modules for 5.0.16-200.fc29.x86_64
#Are the development files for kernel 5.0.16-200.fc29.x86_64 or the appropriate kernel-devel package installed?


# VM startup error gives directions to correct it:

#Turning USB to 1 still showed:
#
#Kernel driver not installed (rc=-1908)
#The VirtualBox Linux kernel driver (vboxdrv) is probably not loaded.
#You may not have kernel driver installed for kernel that is runnig,
#if so you may do as root:
#dnf install akmod-VirtualBox kernel-devel-$(uname -r)
#If you installed VirtualBox packages and don't want reboot the system, you may need load the kernel driver, doing as root: akmods; systemctl restart systemd-modules-load.service
#where: suplibOsInit what: 3 VERR_VM_DRIVER_NOT_INSTALLED (-1908) - The support driver is not installed. On linux, open returned ENOENT.

#Clicking "Copy" on error then pasting shows:
#
#Failed to open a session for the virtual machine NetApps_VM.
#The virtual machine 'NetApps_VM' has terminated unexpectedly during startup with exit code 1 (0x1).
#Result Code: NS_ERROR_FAILURE (0x80004005)
#Component: MachineWrap
#Interface: IMachine {85cd948e-a71f-4289-281e-0ca7ad48cd89}


su
# Get Extensions Pack
# as per https://unix.stackexchange.com/questions/289685/how-to-install-virtualbox-extension-pack-to-virtualbox-latest-version-on-linux
if [ ! -d "$HOME/Downloads" ]; then
  mkdir -p "$HOME/Downloads"
fi
cd "$HOME/Downloads" || customDie "Cannot cd $HOME/Downloads"
LatestVirtualBoxVersion=$(wget -qO - http://download.virtualbox.org/virtualbox/LATEST-STABLE.TXT) && wget "http://download.virtualbox.org/virtualbox/${LatestVirtualBoxVersion}/Oracle_VM_VirtualBox_Extension_Pack-${LatestVirtualBoxVersion}.vbox-extpack"
# TODO: verify checksums: https://www.virtualbox.org/download/hashes/${LatestVirtualBoxVersion}/SHA256SUMS
sudo VBoxManage extpack install --replace Oracle_VM_VirtualBox_Extension_Pack-${LatestVirtualBoxVersion}.vbox-extpack --accept-license=56be48f923303c8cababb0bb4c478284b688ed23f16d775d729b89a2e8e5f9eb
# extpack install says:
#Progress state: NS_ERROR_FAILURE
#VBoxManage: error: Failed to install "/home/owner/Oracle_VM_VirtualBox_Extension_Pack-5.2.30.vbox-extpack"
#VBoxManage: error: VBoxExtPackRegister returned VERR_VERSION_MISMATCH, pReg=0000000000000000 ErrInfo='Helper version mismatch - expected 0x10002 got 0x3'
#VBoxManage: error: Details: code NS_ERROR_FAILURE (0x80004005), component ExtPackManagerWrap, interface IExtPackManager
#VBoxManage: error: Context: "RTEXITCODE handleExtPack(HandlerArg*)" at line 1361 of file VBoxManageMisc.cpp

VBoxManage list extpacks
cat <<END
You can uninstall VirtualBox Extensions Pack like:"
  sudo VBoxManage extpack uninstall "Oracle VM VirtualBox Extension Pack"

Update it as per guntbert, answered Jun 17 '16 at 18:44
  vboxversion=$(wget -qO - https://download.virtualbox.org/virtualbox/LATEST.TXT)
  wget "https://download.virtualbox.org/virtualbox/${vboxversion}/Oracle_VM_VirtualBox_Extension_Pack-${vboxversion}.vbox-extpack"
  sudo vboxmanage extpack install --replace Oracle_VM_VirtualBox_Extension_Pack-${vboxversion}.vbox-extpack

END
dnf install akmod-VirtualBox kernel-devel-$(uname -r)
# says: No match for argument: kernel-devel-5.0.16-200.fc29.x86_64
akmods; systemctl restart systemd-modules-load.service
