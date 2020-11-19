
```
$ xinput  # get the IDs for all relevant pieces of my tablet.
⎡ Virtual core pointer                       id=2   [master pointer  (3)]
⎜   ↳ Virtual core XTEST pointer                 id=4   [slave  pointer  (2)]
[...]
⎜   ↳ Wacom Bamboo 16FG 4x5 Pen stylus           id=17   [slave  pointer  (2)]
⎜   ↳ Wacom Bamboo 16FG 4x5 Pen eraser           id=20   [slave  pointer  (2)]
⎜   ↳ Wacom Bamboo 16FG 4x5 Pad pad              id=21   [slave  pointer  (2)]
⎜   ↳ Wacom Bamboo 16FG 4x5 Finger               id=22   [slave  pointer  (2)]
⎣ Virtual core keyboard                      id=3   [master keyboard (2)]
    ↳ Virtual core XTEST keyboard                id=5   [slave  keyboard (3)]
    ↳ Power Button                               id=6   [slave  keyboard (3)]
    ↳ Power Button                               id=7   [slave  keyboard (3)]
    ↳ Microsoft Microsoft® Nano Transceiver v2.1   id=13   [slave  keyboard (3)]
[...]
$ xrandr  # get the names of my displays
Screen 0: minimum 8 x 8, current 3840 x 1200, maximum 16384 x 16384
DVI-I-0 disconnected (normal left inverted right x axis y axis)
[...]
DVI-I-3 connected 1920x1200+1920+0 (normal left inverted right x axis y axis) 546mm x 352mm
   1920x1200     59.95*+
   1920x1080     60.00
   1680x1050     59.95
[...]
DP-1 connected 1920x1200+0+0 (normal left inverted right x axis y axis) 546mm x 352mm
   1920x1200     59.95*+
   1920x1080     60.00    59.99    59.94    50.00    60.05    60.00    50.04
   1680x1050     59.95
[...]
$ xinput map-to-output 17 DVI-I-3
$ xinput map-to-output 20 DVI-I-3
$ xinput map-to-output 21 DVI-I-3
$ xinput map-to-output 22 DVI-I-3
```
(Timotimo, 2016)


## References
Timotimo. (2016, January 19). Re: Graphics tablet assign to one monitor of dual display se. KDE Community Forums. https://forum.kde.org/viewtopic.php?f=139&t=125532#p349760
