#!/bin/bash

# Based on <https://wiki.debian.org/ZRam>

# See also: [Linux Performance: Almost Always Add Swap. Part 2: ZRAM](https://haydenjames.io/linux-performance-almost-always-add-swap-part2-zram/)
# October 18, 2021 by Hayden James, in Blog Linux

if [ ! -f "`command -v insserv`" ]; then
cat <<END
Error: Ensure you are root and have access to the insserv command. You may also have to install insserv such as via:
    apt-get install insserv
END
exit 1
fi

if [ ! -f "etc/init.d/zram" ]; then
    echo "Error: The file etc/init.d/zram is missing in `pwd`."
    exit 1
fi

cp etc/init.d/zram /etc/init.d/
chmod +x /etc/init.d/zram
insserv zram

if [ ! -f "/etc/default/zramswap" ]; then
    echo "Error: The ZRAM configuration is not implemented by $0 since /etc/default/zramswap is missing."
    exit 1
fi

done_flag="`cat /etc/default/zramswap | grep linuxpreinstall`"
if [ ! -z "$done_flag" ]; then
    echo "INFO: /etc/default/zramswap won't be modified since it already contains the done_flag \"$done_flag\"."
    exit 0
fi

cat >> /etc/default/zramswap <<END

#region linuxpreinstall
ALGO=lz4
SIZE=1024
PRIORITY=100
#endregion linuxpreinstall
END

