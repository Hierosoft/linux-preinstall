# MATE

MATE is a low-resource desktop environment (DE) and seems to handle low-memory situations well (when other applications are taking up resources). I used to get a hard freeze every so often in Xfce (in all recent versions in the past few years). GNU OOM killer daemon doesn't seem to be enough for Xfce--The situation is fatal before the daemon can step in. There are ways to configure the OOM killer daemon further, but I haven't gone that far. I recommend nohang either way, since I haven't proven for sure MATE fixes all of the issues as I also upgraded my RAM around then.

nohang: I know nohang basically solved the issue with Xfce though it isn't very comforting since maybe if I don't click "yes" to terminate processes maybe it would hang. Something similar is built into Windows (a low memory warning with an option or eventual requirement to terminate large processes). I consider nohang or something like it a necessity for using a computer for any sort of work, or in general, anything you don't want to lose (the same rule of thumb that applies to backup frequency). The nohang package is available on several distros and more information is at the nohang repo.


## Suggested Configuration
(requires manual steps until scripting of the linuxpreinstall/mate submodule is complete)
- If you have the default mate-panel configuration, which uses two panels: Delete the bottom menu (the one with just an application switcher) and move the top menu on the bottom, so it is like other desktops (right-click, Properties, then change orientation to "Bottom").
- Use Dock `*`: MATE Dock is a "true dock," in the sense that a pinned icon automatically change to application switcher if that application is open, similarly to KDE, Windows and macOS.
- Install and add "Indicator Applet Complete" `*`.
  - After manually adding it and moving it to the far right of the bottom menu, you see and control GUI-based applets such as Nextcloud which follow the app indicator paradigm (similarly to Windows tray icons).
- Move the "Desktop" button to the bottom all and the way to the right, like other desktops (such as KDE and Windows).
- Use [Brisk Menu](brisk-menu.md), a searchable menu where you can add favorites: Remove the Application menu ("Classic Menu") and add Brisk Menu there at the bottom left.
  - Install mozo `*`: This application makes the "Edit" feature of the Brisk Menu load the mozo GUI).

`*` See [everyone/MATE/mate-panel-additions.deb.sh](../../everyone/MATE/mate-panel-additions.deb.sh)


## linuxpreinstall/mate submodule
This submodule is for Python programmers (and this project) who want to script changes to the MATE menu.
The main problem with this module is that MATE configuration seems to be redundant in some way: entries in dconf refer to other things.
For example, Dock doesn't work on Devuan 4 (chimaera) (based on Debian 11 (bullseye)), so the current test script tries to remove broken (empty) instances of Dock which the user can't remove via the GUI. However, despite reloading mate-panel, the entry can't be removed. Not tried yet:
- [ ] Terminate mate-panel, remove the entries, then reload it.
