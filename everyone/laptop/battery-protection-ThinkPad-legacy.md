# Battery Protection - ThinkPad - Legacy
Legacy ThinkPads only: External Kernel Module for Battery Care
(<https://linrunner.de/tlp/installation/ubuntu.html#legacy-thinkpads-only-external-kernel-module-for-battery-care>)

First complete steps in:
[battery-protection-Thinkpad](battery-protection-Thinkpad.md)

```bash
sudo apt install tp-smapi-dkms
```

> Warning
> In Ubuntu 23.10 and 24.04 the tp-smapi-dkms package from the official repositories is currently broken and does neither build nor install the kernel module.
> Workaround: download the working package from Debian Sid and install manually
```bash
wget -P /tmp http://ftp.de.debian.org/debian/pool/main/t/tp-smapi/tp-smapi-dkms_0.44-1_all.deb
sudo apt install /tmp/tp-smapi-dkms_0.44-1_all.deb
```
