#!/bin/sh

cd /tmp
dl_name=get-deps-from-apt.sh
URL="https://github.com/poikilos/xfce4-dockbarx-plugin/raw/pygi-python3/$dl_name"
wget -O $dl_name $URL
code=$?
if [ $code -ne 0 ]; then
    echo "Error: 'wget -O $dl_name $URL' failed."
    exit $code
fi
bash ./$dl_name
