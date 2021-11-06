#!/bin/bash

xdg-mime default thunar.desktop inode/directory
# ^ Set the default directory handler application.
#   The full path doesn't work.
#   xdg-mime query default inode/directory  # get
#   xdg-open ~  # test
#   > I noticed that ~/.local/share/applications/mimeapps.list had a new line
#   > > [Default Applications]
#   > > inode/directory=nautilus.desktop;
#   -cedricmc 2013-02-02 11:38:22
#   > I had a similar issue. But here, the problem was that xdg-open detected the wrong DE here (I don't have any) and so it always opend pcmanfm as the filebrowser. I want xdg-open to lookup the default application for inode/directory, and one can force that by
#   >
#   > $ XDG_CURRENT_DESKTOP='X-Generic' xdg-open ~
#   -thorsten  2017-06-22 10:51:46


# References
# - "[SOLVED] How to set the default file browser." Arch Linux Forum. <https://bbs.archlinux.org/viewtopic.php?id=157033>:
