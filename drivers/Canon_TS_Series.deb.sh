#!/bin/sh
FILE=cnijfilter2-5.70-1-deb.tar.gz
URL=https://gdlp01.c-wss.com/gds/8/0100009928/01/$FILE
wget -O $FILE $URL
code=$?
if [ $code -ne 0 ]; then
    echo "Error: 'wget -O $FILE $URL' failed with error code $code in \"`pwd`\""
    exit $code
fi
mkdir -p ~/Downloads
cd ~/Downloads
if [ -d "cnijfilter2-tmp" ]; then
    rm -Rf "cnijfilter2-tmp"
fi
mkdir "cnijfilter2-tmp"
cd cnijfilter2-tmp
tar -xvf ../$FILE
cd cnijfilter2-*
#dpkg -i packages/cnijfilter2_5.70-1_amd64.deb
./install.sh

# After following the install steps, the following is the result:
# printer name: TS6200USB (default)
# sudo /usr/sbin/lpadmin -p TS6200USB -P /usr/share/cups/model/canonts6200.ppd -v cnijbe2://Canon/?port=usb&serial=305507 -E
