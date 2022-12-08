#!/bin/bash
#!/bin/bash
>&2 cat <<END
Blacklist trashy builtin Broadcom WiFi adapters such as BCM4313 on Gateway laptaps which have a poor, slow connection compared to various Realtek USB devices.

Make sure you have another connection to the internet before running this!
END
# me=./`basename $0`
me="$0"
# BLACKLIST="/etc/modprobe.d/blacklist.conf"
BLACKLIST="/etc/modprobe.d/blacklist-broadcom.conf"
source /etc/os-release

REPO_TYPE=rpm

if [ "$NAME" = "Ubuntu" ]; then
    REPO_TYPE=apt
elif [ "$ID_LIKE" = "ubuntu debian" ]; then
    # such as Linux Mint 21
    REPO_TYPE=apt
elif [ ! -f "`command -v rpm`" ]; then
    REPO_TYPE=apt
fi

write_bcma_blacklist(){
    cat > $BLACKLIST  <<END
blacklist b43
blacklist bcma
blacklist bcma-pci-bridge
END
}

if [ "$REPO_TYPE" = "apt" ]; then
    # According to:
    #   pci (lspci -nnk | grep -iA2 net)
    #   (such as used after this exit)
    #   the card uses the bcma kernel module on Linux Mint 21 (not not wl like on Fedora).
    #   It also uses bcma-pci-bridge, so as per
    #   Pilot6's answer edited Jan 22, 2020 at 20:55
    #   answered Jan 22, 2020 at 20:30 on
    #   <https://askubuntu.com/a/1205001/766334>:
    >&2 echo "* writing $BLACKLIST"
    # 'tee $BLACKLIST 1>&2' or >/dev/null HANGS until enter pressed,
    #   or permanently if script is redirected!
    #   Therefore, to avoid tee to reserve stdout for linux-preinstall log,
    #   follow <https://unix.stackexchange.com/a/269080/343286>:    
    sudo bash -c "$(declare -f write_bcma_blacklist); write_bcma_blacklist"

    if [ $? -ne 0 ]; then
        exit 1
    else
        >&2 echo "OK"
    fi
    sudo update-initramfs -u 1>&2
    >&2 echo
    >&2 echo
    >&2 echo "A reboot is required."
    >&2 echo
    exit 0
fi
# Exit if Ubuntu since
# apparently kmod-wl is only used on Fedora not Linux Mint 21:


cat > /dev/null <<END
Blacklisting wl sounds like a bad idea, but slow BCM4313 uses it:

lspci -nnk | grep -iA2 net
# output:
. . .
03:00.0 Network controller [0280]: Broadcom Inc. and subsidiaries BCM4313 802.11bgn Wireless Network Adapter [14e4:4727] (rev 01)
        Subsystem: Foxconn International, Inc. Device [105b:e042]
        Kernel driver in use: wl
END
#if [ ! -z "$1" ]; then
#    DRIVER_NAME="$1"
#fi
if [ ! -z "$1" ]; then
    idVendor="$1"
fi
if [ ! -z "$2" ]; then
    idProduct="$2"
fi
if [ ! -z "$3" ]; then
    subsystem="$3"
fi

dest_rule_name="BC4313-disable.rules"
dest_rule="/etc/udev/rules.d/$dest_rule_name"

has_all=false

usage(){
    echo "Usage"
    echo "* Regular blacklisting is not useful since wl is used for so many cards."
    echo
    echo "* pci (lspci -nnk | grep -iA2 net):"
    lspci -nnk | grep -iA2 net
    echo
    echo "* usb (lsusb):"
    lsusb
    echo
    cat <<END

You must specify vendorID then productID (separated by a colon in the list above, but separate them by a space) one of the following active drivers, then pci or usb according to which list below is the one containing it, with no spaces:
  $me <vendorId> <productId> <pci|usb>

Example:
    sudo $me 14e4 4727 pci
    # ^ for Broadcom Inc. and subsidiaries BCM4313 802.11bgn Wireless Network Adapter [14e4:4727] (rev 01)

END

}
if [ ! -z "$idVendor" ]; then
    if [ ! -z "$idProduct" ]; then
        if [ ! -z "$subsystem" ]; then
            has_all="true"
        else
            usage
            echo "Error: You must specify subsystem."
            exit 1
        fi
    else
        usage
        echo "Error: You must specify idProduct."
        exit 1
    fi
else
    usage
    echo "Error: You must specify idVendor."
    exit 1
fi


# if [ ! -z "$DRIVER_NAME" ]; then
if [ "@$has_all" = "@true" ]; then
    if [ "@$2" = "@--undo" ]; then
        # echo "* Un-blacklisting $DRIVER_NAME..."
        # sed 's/blacklist $DRIVER_NAME//' -i $BLACKLIST
        echo "* Regular blacklisting is not useful since wl is used for so many cards."
        printf "* removing \"$dest_rule\"..."
        rm "$dest_rule"
        code=$?
        if [ $code -eq 0 ]; then
            echo "OK"
        else
            echo "FAILED"
        fi
    else
        # echo "* Blacklisting $DRIVER_NAME..."
        # See <https://askubuntu.com/a/604070>:
        # echo "blacklist $DRIVER_NAME" | tee -a $BLACKLIST
        echo "* Regular blacklisting is not useful since wl is used for so many cards."
        # See <https://www.pclinuxos.com/forum/index.php?topic=146211.0>:
        tmp_rule="/tmp/$dest_rule_name"
        longName="$idVendor:$idProduct"
        if [ "@$idVendor" = "@14e4" ]; then
            if [ "@$idProduct" = "@4727" ]; then
                longName="Broadcom Inc. and subsidiaries BCM4313 802.11bgn Wireless Network Adapter [14e4:4727] (rev 01)"
            else
                echo "* unknown idProduct (That's ok)"
            fi
        else
            echo "* unknown idVendor (That's ok)"
        fi
        printf "* generating $tmp_rule..."
        cat > $tmp_rule <<END
# Disable $longName
SUBSYSTEM=="$subsystem", ATTRS{idVendor}=="$idVendor", ATTRS{idProduct}=="$idProduct", ATTR{authorized}="0"
END
        code=$?
        if [ $code -eq 0 ]; then
            echo "OK:"
            cat "$tmp_rule"
            echo
        else
            echo "FAILED"
            exit $code
        fi

        if [ -f "$dest_rule" ]; then
            printf "* overwriting $dest_rule..."
        else
            printf "* installing $dest_rule..."
        fi
        mv -f "$tmp_rule" "$dest_rule"
        code=$?
        if [ $code -eq 0 ]; then
            echo "OK"
        else
            echo "'mv -f \"$tmp_rule\" \"$dest_rule\"' FAILED"
            exit $code
        fi
        printf "* reloading rules..."
        udevadm control --reload-rules && udevadm trigger
        code=$?
        if [ $code -eq 0 ]; then
            echo "OK"
        else
            echo "udevadm control --reload-rules && udevadm trigger FAILED"
            exit $code
        fi
    fi
else
    echo
    exit 1
fi
# the ./wireless-info script is also mentioned in "RT5370.sh".
cat <<END
* To see which device is using which driver, see GENERAL.CONNECTION (followed by -- if not connected, otherwise a network name a.k.a. SSID follows) in the "NetworkManager info" section of ~/wireless-info.txt after running:
cd ~ && wget -N -t 5 -T 10 https://github.com/UbuntuForums/wireless-info/raw/master/wireless-info && chmod +x wireless-info && ./wireless-info

* The rule still doesn't seem to work, so next, ONLY if your other device doesn't use wl do:
sudo modprobe -r wl
echo '# This blacklist is an example from $me' | sudo tee /etc/modprobe.d/wl-blacklist.conf
echo "blacklist wl" | sudo tee -a /etc/modprobe.d/wl-blacklist.conf
END

exit 1
echo "Now install something like 'Cana Kit' aka RT5370* script in this directory"
