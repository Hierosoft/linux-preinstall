# Linux Drivers
(from <https://github.com/Hierosoft/linux-preinstall/tree/master/drivers>)

In many cases, drivers are included with the linux kernel, or can be installed from a software repository.

In any case where the driver isn't installed automatically, this folder will attempt to include a script or at least documentation for installing the hardware.

## Wi-Fi
Usually the drivers and compatibility claims from manufacturers are unreliable. For example, Panda Wireless devices are touted as very good for linux, but the *one* model I bought didn't work. See details for "RT5572 (such as PAU09)" under "Ralink chipsets" below.

In general, the driver from the linux kernel or linux repos is best. In several cases, you need to download firmware which is non-free (It may be free of charge but not having public licensed source code), which is why it isn't included in most distros by default. 

To determine which driver you need, you must identify the chipset. The brand doesn't always determine the chipset or even the manufacturer.

For example, if you have a "CanaKit", lsusb may result in "RT5370" (see below for details).

Ralink chipsets
* [RT5370.sh](RT5370.sh) such as "CanaKit Raspberry Pi WiFi Wireless Adapter / Dongle (802.11 n/g/b 150 Mbps)" USB 2 from Amazon ([here](https://www.amazon.com/gp/product/B00GFAN498/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1))
* RT5572 (such as PAU09): no compatibility or at least no support (See details below)
  * It is NOT SUPPORTED by Panda Wireless anymore: In some contexts Panda Wireless' website says all of their cards are supported on Linux, but if you click all the way down through the support downloads to this particular model, there is no Linux option.
    * For shame!
  * See [panda_wireless_PAU09_or_Ralink_RT5572.sh](panda_wireless_PAU09_or_Ralink_RT5572.sh)
    * Compiling it doesn't work on Fedora 35, apparently because the kernel headers on the Fedora 35 aren't configured correctly. Using documentation to construct the sh file didn't help on Fedora 35.

## Printers
Many printers are plug and play on Linux, but some may require installation steps either to make the printer work or provide you with printer controls. The "Printers" or "Printer Settings" application of your desktop environment will contain a list of installed printers, and may have all of the settings you need depending on your printer.

### Brother
The driver from the brother website is usually fine. See examples in this folder of how install could be automated.

### HP
Usually installing the `hplip` package is enough to get an HP printer working and configure it.

### Canon
The driver from the Canon website is recommended. See [Canon_TS_Series.deb.sh](Canon_TS_Series.deb.sh) for an example of how this could be automated (for the TS series).
