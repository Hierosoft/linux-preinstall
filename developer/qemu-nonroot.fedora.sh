#!/bin/sh


customExit(){
    code=1
    if [ ! -z "$2" ]; then
        code="$2"
    fi
    cat <<END
Error:
$1
END
    exit $code
}

GUI=true

for var in "$@"
do
    if [ "@$var" = "@--cli" ]; then
        GUI=false
    else
        echo "Error: unknown option '$var'"
        exit 1
    fi
done

# Some Ubuntu release dates from <https://wiki.ubuntu.com/Releases>:
# Ubuntu 16.04 LTS; Xenial Xerus; April 21, 2016
# Ubuntu 14.04.6 LTS; Trusty Tahr; March 7, 2019
# Ubuntu 14.04 LTS; Trusty Tahr; April 17, 2014

if [ -z "$BOXES_DIR" ]; then
    BOXES_DIR="$HOME/qemu"
    echo "BOXES_DIR=$BOXES_DIR"
fi
mkdir -p "$BOXES_DIR" || customExit "'mkdir -p \"$BOXES_DIR\"' failed."
cd "$BOXES_DIR" || customExit "'cd \"$BOXES_DIR\"' failed."
# See https://fedoraproject.org/wiki/How_to_use_qemu
if [ -z "$QEMU_HDA" ]; then
    QEMU_HDA="ubuntu14.qcow"
fi
printf "* checking for $QEMU_HDA..."
QEMU_CREATE=true
if [ -z "$QEMU_INITIALIZE" ]; then
    QEMU_INITIALIZE=false
fi
if [ ! -f "$QEMU_HDA" ]; then
    # qemu-img create $QEMU_HDA 100G || customExit "qemu-img create ubuntu12.qcow 100G failed."
    # ^ format=raw
    qemu-img create $QEMU_HDA 100G -f qcow2 || customExit "'qemu-img create ubuntu12.qcow 100G --fmt qcow2' failed."
    QEMU_INITIALIZE=true
    echo "* automatically set QEMU_INITIALIZE since hda $QEMU_HDA is new."
else
    echo "* using existing $QEMU_HDA"
    QEMU_CREATE=false
fi


if [ -z "$QEMU_CDROM" ]; then
    QEMU_CDROM="$HOME/Downloads/ubuntu-14.04.6-desktop-amd64.iso"
    echo "QEMU_CDROM=$QEMU_CDROM"
fi
# Virtual Machine Manager
# FAILS to start VM if has '&'! Becomes '&amp;' such as in:
# /home/owner/Downloads/OS&amp;Boot/ubuntu-14.04.6-desktop-amd64.iso
# So save in /home/owner/Downloads/ubuntu-14.04.6-desktop-amd64.iso

echo "Use \"Virtual Machine Manager\" as follows:"
#exit 0


# FAILS (no bootable device) unless CDROM is set correctly
echo "* Manual Install"
echo "  * x86_64"
echo "* Generic OS"
echo "* Memory: 1024 CPUs: 1 or more"
echo "* Enable storage"
echo "  * Select or create custom storage"
echo "    * Manage, browse local, choose $QEMU_HDA"
echo "  * \"...may not have...permissions...correct this now?\": Yes"
echo "* Name: $QEMU_CDROM"
echo "* [x] Customize Before Install"
echo "  * Add Hardware"
echo "    * Storage"
echo "      * CDROM device"
echo "        * Select or create custom image"
echo "          * paste: $QEMU_CDROM"
echo "        * Bus type: IDE"
echo "    * Finish"
echo "  * Boot options"
echo "    * check \"IDE CDROM 1\""
echo "  * Apply"
echo "  * Begin Install (top left button)"
echo
echo "Specify --cli for command line interface instructions."
echo
if [ "$GUI" = "@true" ]; then
    exit 0
fi


# qemu is not a command unless you symlink it, so:
if [ -z "$QEMU" ]; then
    QEMU=qemu-system-x86_64
    # ^ full system emulation
    # ^
    # Spectre V2 : Spectre mitigation: LFENCE not serializing. Switching to generic pipeline
    # Initramfs unpacking failed: write error
    # /scripts/init-top/udev: line 16: /lib/systemd/systemd-udevd: not found
    #   [stuck on BusyBox (initramfs) prompt]
    QEMU=qemu-x86_64
    # ^
    #   (See <https://linux-tips.com/t/booting-from-an-iso-image-using-qemu/136>)
    # ^ "qemu: unknown option 'cdrom'"
    # ^ because it is only for running executables:
    #   <https://qemu.readthedocs.io/en/latest/user/main.html>
    QEMU=qemu-kvm
    # ^ (See <https://documentation.suse.com/sles/11-SP4/html/SLES-all/cha-qemu-running.html>)
    # ^ Initramfs unpacking failed: write error
    #   /scripts/init-top/udev: line 16: /lib/systemd/systemd-udevd: not found
    #   [stuck on BusyBox (initramfs) prompt]
    echo "QEMU=$QEMU"
fi

echo "QEMU_INITIALIZE=$QEMU_INITIALIZE"
if [ "@$QEMU_INITIALIZE" = "@true" ]; then
    if [ -f "$QEMU_CDROM" ]; then
        # $QEMU -cdrom $QEMU_CDROM -hda $QEMU_HDA -boot d -net nic -net user -m 196 -localtime
        #  ^ "qemu-system-x86_64: -localtime: invalid option"
        # $QEMU -cdrom $QEMU_CDROM -hda $QEMU_HDA -boot d -net nic -net user -m 196
        # ^ WARNING: Image format was not specified for 'ubuntu14.qcow' and probing guessed raw.
        #         Automatically detecting the format is dangerous for raw images, write operations on block 0 will be restricted.
        #         Specify the 'raw' format explicitly to remove the restrictions.
        # $QEMU -hda $QEMU_HDA -cdrom $QEMU_CDROM -boot d -net nic -net user -m 196 -rtc base=localtime
        $QEMU -f $QEMU_HDA -c $QEMU_CDROM -boot d -net nic -net user -m 196 -rtc base=localtime
        # ^ DOESN'T WORK (see errors in comments near "QEMU=" lines further up)
    else
        echo "* $QEMU_CDROM does not exist, so the cdrom will not be installed to $QEMU_HDA."
    fi
else
    echo "* skipping install since QEMU_INITIALIZE is not true."
    echo "  Try 'cd `pwd`' then:"
    echo "  $QEMU -f $QEMU_HDA -c $QEMU_CDROM -net nic -net user -m 196 -rtc base=localtime"
    echo "  # or"
    if [ ! -f "`command -v qemu-system-x86_64`" ]; then
        echo "# install qemu-system-x86 then"
    fi
    echo "  qemu-system-x86_64 -drive file=$QEMU_HDA -net nic -net user -m 196 -rtc base=localtime"
fi
