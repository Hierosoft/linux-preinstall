# TEMPer USB
TEMPer USB is a standard for temperature sensor tools for TEMPerV1 devices.
Because of this standard, many devices can work using the same driver (or user-space driver code which requires [udev](../developer/udev.md) rules described below).
```
sudo pip install temperusb
```
##### Now give permission to user
See <http://ask.xmodulo.com/change-usb-device-permission-linux.html>:
```
sudo lsusb -vvv
```
* This results in lots of info. Find the TEMPer device there in that huge list to get the block of info for your specific device--something like the contents of the file included with this guide: "TEMPerV1 (white, all-in-one) USB device from AMAZON lsusb -vvv.txt"
* It yields the necessary info used in steps further down:
```
idVendor           0x0c45 Microdia
idProduct          0x7401 TEMPer Temperature Sensor
```
* then create a rules file:
```
sudo nano /etc/udev/rules.d/50-myusb.rules
```
* adding the line (where 0c45 7401 and are your values found above after 0x [hexadecimal] values using sudo lsusb -vvv):
```
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0c45", ATTRS{idProduct}=="7401", GROUP="users", MODE="0666"
```
* then run:
```
#DOESN"T WORK: sudo udevadm control --reload
sudo udevadm control --reload-rules && sudo udevadm trigger
#some GNU/Linux systems use udevtrigger instead of udevadm trigger
```
* now temper should work:
```
temper-poll
```
* should output something like:
```
Found 1 devices
Device #0: 23.8°C 74.8°F
```

For an example program, see [TemperatureSanitizer](https://github.com/poikilos/TemperatureSanitizer).
