# Battery Protection - ThinkPad
## Installation Instruction for TLP for Lenovo ThinkPads

Install & Start TLP & Check System Status
```bash
sudo apt install tlp tlp-rdw
sudo tlp start
sudo tlp-stat -s
```

Check status of battery features with
```bash
sudo tlp-stat -b
```

Example output:

```bash
--- TLP 1.3.1 --------------------------------------------

+++ Battery Features: Charge Thresholds and Recalibrate
natacpi    = active (data, thresholds)
tpacpi-bat = active (recalibrate)
tp-smapi   = inactive (ThinkPad not supported)
```

## Install Battery Features

```bash
sudo apt install acpi-call-dkms
```

Install the required battery module for tpacpi-bat

```bash
sudo apt install acpi-call-dkms
```

## Set Permanent Charging Threshold

Uncomment the following lins in **/etc/tlp.conf** and add the desired charge start and stop percentage. (Start percentage musst be 3% higher then the stop)

```
START_CHARGE_THRESH_BAT0=50
STOP_CHARGE_THRESH_BAT0=80
```

## Full documentation
Full documentation unter: [https://linrunner.de/tlp/installation/index.html](https://linrunner.de/tlp/installation/index.html)
