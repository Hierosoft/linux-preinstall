#!/bin/sh

# From https://gist.github.com/aweijnitz/c9ac7a18880225f12bf0 "aweijnitz/install_CUPS_all_defaults.sh"
apt-get update
apt-get -y install cups
# The following NEW packages will be installed:
# acl avahi-daemon bc colord colord-data cups cups-browsed cups-client cups-common cups-core-drivers cups-daemon cups-filters cups-filters-core-drivers cups-ipp-utils cups-ppdc cups-server-common dbus-user-session dconf-gsettings-backend dconf-service libavahi-core7 libavahi-glib1 libcolord2 libcolorhug2 libdconf1 libexif12 libfontembed1 libgd3 libgphoto2-6 libgphoto2-l10n libgphoto2-port12 libgudev-1.0-0 libgusb2 libgutenprint-common libgutenprint9 libieee1284-3 liblouis-data liblouis17 liblouisutdml-bin liblouisutdml-data liblouisutdml8 libmariadb3 libnspr4 libnss-mdns libnss3 libpolkit-agent-1-0 libpolkit-backend-1-0 libpolkit-gobject-1-0 libpoppler82 libqpdf21 libsane libsane-common libsnmp-base libsnmp30 libxpm4 mariadb-common mysql-common policykit-1 poppler-utils printer-driver-gutenprint sane-utils ssl-cert update-inetd

# From <https://askubuntu.com/questions/23936/how-do-you-administer-cups-remotely-using-the-web-interface>:
cupsctl --remote-admin --remote-any --share-printers
if [ $? -eq 0 ]; then
    echo "You should now be able to access the web interface http://$HOSTNAME:631/ from other computers."
    MY_IP="`hostname -I | cut -d' ' -f1`"
    echo "The admin interface such as for adding printers is https://$MY_IP:631/admin/"
else
    echo "Error: Enabling remote admin failed."
    exit 1
fi
cat <<END

The settings for Posiflex AURA PP7000-II are defined in the manual.

Some of the settings vary based on dip switches.
1 stands for on and 0 stands for off in digits before colons below.
The first 2 switches form a 4-bit enumeration of 4 speeds.
11: 38400 bps / (Parallel)
01: 4800 bps
10: 9600 bps
00: 19200 bps

Other switches:
3. Parity  1:Even 0:None
4. Handshaking  1:XON 0:Hardware
5. Busy on...  1:"buffer full" 2:"off line"
6. ...cut  1:"Immediate"  2:"Protective"
7. CR code...  1:"effective" 0:"ineffective"
8. 1:"Factory internal setting" 0:"Application standard mode"

Poikilos' suggested settings (switches 1-8):
1. 0
2. 0
[1-2 default:00 for serial, 11 for parallel]
3. 0 (no parity) [default:0]
4. 0 (hardware handshaking) [default:0]
5. 0 (busy on offline) [default:0]
6. 0 (protective cut) [default:0]
7. 0 "CR code ineffective" [default:0]
8. 0 "Application standard mode" [default:0]

CUPS settings:
- Baud rate for serial mode (with switches 1-2 set to 00 as per serial mode with auto cutter default): 19200
- Parity: None
- Flow control: The manual says that in hardware handshaking mode (for serial mode) "the printer signifies the busy status over hardware signals that can be detected by the host as 'DSR' or 'CTS'".
- Data bits: 8

Suggested CUPS driver settings:
- Name: PP7000-II
- Description: Posiflex Aura PP7000-II
- Make: Click "Generic", "Next", "Generic Text-Only Printer (en)", "Add Printer" as per <https://www.digi.com/support/knowledge-base/how-to-add-cups-serial-printers-in-linux>.

Suggested general CUPS settings:
- Media Size: "Custom Page Size 1" (actually 3+1/8 inches or 79.5 mm)
- Long line handling: Wrap at right edge
- Tab Stop Width: 8 [default:8]
- Paginate Output: Off (continuous)
- Left Margin: 5 columns [default:5]
- Right Margin: 2 columns [default:2]
- Top Margin: 2 lines [default:2]
- bottom Margin: 2 lines [default:2]

The above results in the following connection string: serial:/dev/ttyS0?baud=19200+bits=8+parity=none+flow=hard

Test:
lp -d PP7000-II /dev/inittab
# ^ only for SystemV-style init, not systemd
lp -d PP7000-II /etc/os-release

lp  -t"test"  -o -f  -o -a /etc/motd -d PP7000-II

# NOTE that the author of the tool I based my work on says he was just following the ESC/P standard (which up until then I thought was EPSON-specific), so a more fully-fledged application using ESC/P will probably be better than continuing work on this. However, the notes from the manual, if complete, could help implement unique features of this model if there are any.
END

pip install -U pyserial

