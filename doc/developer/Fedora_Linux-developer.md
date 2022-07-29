# Fedora Linux Developer

This document is for installing applications developers using Fedora
Linux usually want to install.

Manual steps:
- [drivers/TEMPer_USB.md](drivers/TEMPer_USB.md)
- Nextcloud
- extras and nonfree from rpmfusion: click and install the repo packages free and nonfree from https://rpmfusion.org/Configuration/

### Management:
```
sudo dnf install gparted filezilla gnome-tweak-tool pysdm keepassx
```
- "Tweak Tool" icon allows configuring various aspects of gnome configuration
- "PySDM" is a gui for editing fstab mountpoints
- If KeePass 1 works in your version of Wine, you can manually install Windows version of KeePass 1 (NOTE: only Windows version of keepass 2 has import for KeePass 1, since dll is Windows-only). However, keepassx version 2.xx can import KeePass 1 files, unlike the linux version of KeePass 2.xx
- Install 32-BIT version of Wine to avoid issues (64-bit is not well supported and doesn't run 32-bit windows programs)
```
sudo dnf remove wine-core
sudo dnf install wine.i686
sudo dnf install winetricks
#(winetricks is a noarch package)
export WINEARCH=win32
export WINEPREFIX=~/win32
winetricks
```

## Tasks
This section describes changes that need to be made to this article, as
well as WIP information that may help.

- [ ] Set those wine variables for the user at login (workaround: make shell script called winetricks32 containing the two lines:
```
#!/bin/sh
WINEARCH=win32 WINEPREFIX=~/win32 winetricks
```
* Then run `chmod +x winetricks32`, wait for the config window to appear, then continue.
* Choose default wine prefix, OK
* Choose "Install a Windows DLL or Component", OK
  * MS GDI+ (required for many applications, such as KeePass 1.xx, though KeePass 1 doesn't work on Wine 2.4)
  * MS Setup API
  * MS Visual Basic 6 runtime sp6

For some reason, result is: `vb6run install completed, but installed file /home/owner/win32/dosdevices/c:/windows/system32/MSVBVM60.DLL not found`

After the above commands, wine will be 32-bit, and wine64 will be 64-bit. ~/win32 should be used for the wine prefix for the 32-bit version, and `WINEARCH=win32` should be used.
The line below is from <https://wiki.winehq.org/Fedora>:
```
dnf config-manager --add-repo https://dl.winehq.org/wine-builds/fedora/25/winehq.repo
```

### Developer Tools
```
# various tools:
sudo dnf install gimp blender geany xterm monodevelop qt-creator kate gitg
```

#### Kivy
See [Kivy.md](Kivy.md).
