# Devuan

## Devuan Caveats
(tested on updated Devuan Chimera 2021-11-22)
- Devuan MATE will not start unless installed via tasksel rather than the mate-desktop package. If you install the mate-desktop package only, MATE will not appear as checked in tasksel, and choosing it then logging in will result in a blank background with a movable cursor.

## Mounting and Unmounting
Drives will not unmount as an unpriveleged user by default. You must add a polkit file.
- Install the file using `cd linux-preinstall && ./everyone/devuan/allow-unpriveleged-automount.sh`
