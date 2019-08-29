# HDMI Audio

## Tested On...
- Pavilion G6
  - Fedora 30: NOT working yet

## works in speaker-test (but not other programs)
<https://bbs.archlinux.org/viewtopic.php?id=207085>
```
speaker-test -D hdmi:CARD=PCH,DEV=0 -c 2
```

## List devices:
```
aplay -l
```

Shows:
```
**** List of PLAYBACK Hardware Devices ****
card 0: PCH [HDA Intel PCH], device 0: 92HD87B2/4 Analog [92HD87B2/4 Analog]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: PCH [HDA Intel PCH], device 3: HDMI 0 [HDMI 0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```


## Reload settings

<https://askubuntu.com/questions/15223/how-can-i-restart-pulseaudio-without-having-to-logout>

- Reloads settings even though forum reply says it kills it:
```
pulseaudio -k
```

- You may also need:
```
sudo killall pulseaudio
sudo pulseaudio -D
```

- Then you must select the device with `pavucontrol` unless your
  settings set the default to the HMDI device or a combined sink that
  includes the HMDI.


## Didn't Work

### Settings for /etc/pulse/default.pa

- Does not create another sink at all:
  - 1,3

- <https://forums.fedoraforum.org/showthread.php?265449-Problem-with-HDMI-audio-output-on-HP-Pavilion-dv6>
  (does nothing):
```
load-module module-alsa-sink device=hw:1,3
```
- Other combinations that don't work: hw:[0-3],[0-3]
 
