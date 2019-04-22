cd
if [ ! -d "Downloads" ]; then
  mkdir Downloads
fi
cd Downloads
unz_name=linux-brprinter-installer-2.2.0-1
dl_name="$unz_name.gz"
wget -O "$dl_name" http://download.brother.com/welcome/dlf006893/linux-brprinter-installer-2.2.0-1.gz
gunzip $dl_name
bash $unz_name HL-3170CDW
#above is INTERACTIVE installer
exit 0


# For some reason, below doesn't work (says ready, but doesn't print even after printer is added manually).
# The printer only works if the interactive installer script from the brother website is used.

package_name=hl3170cdwlpr-1.1.2-1.i386.rpm
echo "downloading lpr driver (required by cupswrapper)"
wget -O $package_name http://support.brother.com/g/b/files/dlf/dlf007055/hl3170cdwlpr-1.1.2-1.i386.rpm
rpm  -ihv --nodeps $package_name

echo "downloading cupswrapper driver (provides cups configuration features for the lpr driver)"
package_name=hl3170cdwcupswrapper-1.1.4-0.i386.rpm
wget -O $package_name http://download.brother.com/welcome/dlf007057/hl3170cdwcupswrapper-1.1.4-0.i386.rpm
rpm  -ihv --nodeps $package_name


echo "NOTE: if you do not have glibc installed, this will not work"

echo "The installer should have installed a ppd file such as:"
echo "  /usr/share/cups/model/Brother/brother_hl3170cdw_printer_en.ppd"
if [ -f "/usr/share/cups/model/Brother/brother_hl3170cdw_printer_en.ppd" ]; then
  echo "  (found)"
else
  echo "  (not found)"
fi
echo "Now you must add a printer or configure using http://localhost:631/printers"
echo "If you have a firewall, allow:"
echo "Inbound direction : UDP Port 54925"
echo "Outbound direction : TCP Port 54921"
lpadmin -p HL3170CDW -v socket://192.212.100.253
#lpadmin -p HL3170CDW -v socket://192.212.100.253 -E

#see also https://docs.oracle.com/cd/E23824_01/html/821-1451/gllgm.html#gllfr
#stats:
#lpstat -p HL3170CDW -l
#set default:
lpoptions -d HL3170CDW
#show default:
#lpstat -d
