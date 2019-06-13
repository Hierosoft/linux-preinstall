#!/bin/sh
# Description: Restart audio (fixes frozen xfce4-pulseaudio-plugin)
cat <<END
See also:
* https://forum.xfce.org/viewtopic.php?id=8627
END
pulseaudio -k
pulseaudio --start
