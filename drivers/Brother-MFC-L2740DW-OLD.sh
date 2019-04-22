#!/bin/sh
cd
if [ ! -d "Downloads" ]; then
  mkdir Downloads
fi
wget http://download.brother.com/welcome/dlf006893/linux-brprinter-installer-2.2.0-1.gz
#or get latest from <http://support.brother.com/g/b/downloadhowto.aspx?c=us&lang=en&prod=mfcl2740dw_us_eu_as&os=127&dlid=dlf006893_000&flang=4&type3=625>
gunzip linux-brprinter-installer-2.2.0-1.gz
sudo bash linux-brprinter-installer-2.2.0-1 MFC-L2740DW
