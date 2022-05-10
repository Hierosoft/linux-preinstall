#!/bin/bash
me="./qemu-nonroot.sh"
if [ ! -f "$me" ]; then
    me="$0"
fi
if [ -z "$QEMU_INITIALIZE" ]; then
    QEMU_INITIALIZE=false
fi
usage(){
cat <<END

qemu-nonroot
------------
(part of linux-preinstall)

Usage:

$me <VM_NAME> <VM_CDROM> [options]

# - .qcow will be appended to the machine name for the virtual machine.

Options:
(For any values in all caps above or below, you can also set the
corresponding environment variable instead.)
--help        Show this screen.
--prefix      Set the prefix. It must be followed by a value for PREFIX.
--cli         Set GUI to "false": Perform operations automatically
              instead of telling you how to use Virtual Machine Manager
              to set up the VM yourself.
--qemu        Specify what qemu command to use (such as qemu-kvm).


END
    if [ "@$PREFIX" != "@" ]; then
        echo "PREFIX=\"$PREFIX\""
    fi
    if [ "@$BOXES_DIR" != "@" ]; then
        echo "BOXES_DIR=\"$BOXES_DIR\"  # based on PREFIX"
    fi
    if [ "@$VM_CDROM" != "@" ]; then
        echo "VM_CDROM=\"$VM_CDROM\""
    fi
    if [ "@$VM_NAME" != "@" ]; then
        echo "VM_NAME=\"$VM_NAME\""
    fi
    if [ "@$VM_FILE_NAME" != "@" ]; then
        echo "VM_FILE_NAME=\"$VM_FILE_NAME\""
    fi
    if [ "@$VM_PATH" != "@" ]; then
        echo "VM_PATH=\"$VM_PATH\""
    fi
    if [ "@$GUI" != "@" ]; then
        echo "GUI=\"$GUI\""
    fi
    if [ "@$QEMU" != "@" ]; then
        echo "QEMU=\"$QEMU\""
    fi
    echo "QEMU_INITIALIZE=\"$QEMU_INITIALIZE\""
    echo
}

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
set_var=""
# VM_NAME=ubuntu14
VM_NAME=""
specified_cdrom=""
for var in "$@"
do
    if [ "@$var" = "@--cli" ]; then
        GUI=false
    elif [ "@$var" = "@--help" ]; then
        usage
        exit 0
    elif [ "@$var" = "@--prefix" ]; then
        set_var="PREFIX"
    elif [ "@$var" = "@--qemu" ]; then
        set_var="QEMU"
    elif [ "@$set_var" != "@" ]; then
        if [ "@$set_var" = "@PREFIX" ]; then
            PREFIX="$var"
        elif [ "@$set_var" = "@QEMU" ]; then
            QEMU="$var"
        else
            echo "Error: Setting $set_var is not implemented."
        fi
        set_var=""
    else
        # if VM_NAME
        if [ "@$VM_NAME" = "@" ]; then
            VM_NAME="$var"
        elif [ "@$specified_cdrom" = "@" ]; then
            specified_cdrom="$var"
            if [ ! -f "$specified_cdrom" ]; then
                echo "Error: The cdrom image \"$specified_cdrom\" doesn't exist."
                exit 1
            fi
        else
            echo "Error: unknown option '$var'"
            exit 1
        fi
    fi
done

if [ "@$set_var" != "@" ]; then
    usage
    echo "Error: $set_var must be followed by a value."
    exit 1
fi

if [ "@$specified_cdrom" = "@" ]; then
    VM_CDROM="$specified_cdrom"
fi

# if [ "@$VM_CDROM" = "@" ]; then
#     usage
#     echo "Error: You must set VM_CDROM."
#     exit 1
# fi
# VM_CDROM should only be required if the VM named
# $VM_NAME doesn't exist yet (See further down instead).

if [ "@$VM_NAME" = "@" ]; then
    usage
    echo "Error: You must set VM_NAME."
    exit 1
fi
# Some Ubuntu release dates from <https://wiki.ubuntu.com/Releases>:
# Ubuntu 16.04 LTS; Xenial Xerus; April 21, 2016
# Ubuntu 14.04.6 LTS; Trusty Tahr; March 7, 2019
# Ubuntu 14.04 LTS; Trusty Tahr; April 17, 2014

OLD_DEFAULT_BOXES_DIR="$HOME/qemu"
if [ -z "$PREFIX" ]; then
    PREFIX="$HOME/.var"
fi
echo "PREFIX=\"$PREFIX\""
LIB="$PREFIX/lib"
echo "LIB=\"$LIB\""
DEFAULT_BOXES_DIR="$LIB/libvirt"
# ^ default KVM dir is /var/lib/libvirt/images according to
#   <https://www.unixarena.com/2015/12/
#   linux-kvm-change-libvirt-vm-image-store-path.html/>

if [ -d "$OLD_DEFAULT_BOXES_DIR" ]; then
    if [ -d "$DEFAULT_BOXES_DIR" ]; then
        echo "WARNING: You have both the old and new directories,"
        echo "so virtual machines will be left there:"
        echo "* DEFAULT_BOXES_DIR: $DEFAULT_BOXES_DIR"
        echo "* OLD_DEFAULT_BOXES_DIR: $OLD_DEFAULT_BOXES_DIR"
    else
        mkdir -p "$LIB"
        # THIS_CMD="mv \"$OLD_DEFAULT_BOXES_DIR\" \"$LIB/\""
        THIS_CMD="mv \"$OLD_DEFAULT_BOXES_DIR\" \"$DEFAULT_BOXES_DIR\""
        mv "$OLD_DEFAULT_BOXES_DIR" "$DEFAULT_BOXES_DIR" || customExit "'$THIS_CMD' failed."
        echo "$THIS_CMD"
    fi
fi

if [ -z "$BOXES_DIR" ]; then
    BOXES_DIR="$DEFAULT_BOXES_DIR"
    echo "BOXES_DIR=$BOXES_DIR"
fi

# if [ -z "$VM_CDROM" ]; then
#     try_cd="$HOME/Downloads/ubuntu-14.04.6-desktop-amd64.iso"
#     if [ -f "$try_cd" ]; then
#         VM_CDROM="$try_cd"
#     fi
# fi
if [[ $VM_NAME = *" "* ]]; then
    usage
    echo "The VM_NAME must not contain spaces."
    exit 1
fi
if [ "@$VM_FILE_NAME" = "@" ]; then
    VM_FILE_NAME="$VM_NAME.qcow"
fi
if [ "@$VM_PATH" = "@" ]; then
    VM_PATH="$BOXES_DIR/$VM_FILE_NAME"
fi
echo "VM_PATH=\"$VM_PATH\""

if [ -z "$VM_CDROM" ]; then
    if [ ! -f "$VM_PATH" ]; then
    # if [ "@$QEMU_CREATE" = "@true" ]; then
        usage
        echo "Error: you must set --cdrom then a filename (or set it using the VM_CDROM environment variable), or already have $VM_PATH."
        exit 1
    fi
fi
echo "VM_CDROM=$VM_CDROM"


mkdir -p "$BOXES_DIR" || customExit "'mkdir -p \"$BOXES_DIR\"' failed."
cd "$BOXES_DIR" || customExit "'cd \"$BOXES_DIR\"' failed."
# See https://fedoraproject.org/wiki/How_to_use_qemu

printf "* checking for $VM_FILE_NAME..."
QEMU_CREATE=true

if [ ! -f "$VM_FILE_NAME" ]; then
    # qemu-img create $VM_FILE_NAME 100G || customExit "qemu-img create ubuntu12.qcow 100G failed."
    # ^ format=raw
    qemu-img create $VM_FILE_NAME 100G -f qcow2 || customExit "'qemu-img create $VM_FILE_NAME 100G --fmt qcow2' failed."
    QEMU_INITIALIZE=true
    echo "* automatically set QEMU_INITIALIZE since hda $VM_FILE_NAME is new."
else
    echo "FOUND ($VM_FILE_NAME)"
    QEMU_CREATE=false
fi

# Virtual Machine Manager
# FAILS to start VM if has '&'! Becomes '&amp;' such as in:
# /home/owner/Downloads/OS&amp;Boot/ubuntu-14.04.6-desktop-amd64.iso
# So save in /home/owner/Downloads/ubuntu-14.04.6-desktop-amd64.iso


# FAILS (no bootable device) unless CDROM is set correctly
cat <<END

Use \"Virtual Machine Manager\" as follows:
* Manual Install
  * x86_64
* Generic OS
* Memory: 1024 CPUs: 1 or more
* Enable storage
  * Select or create custom storage
    * Manage, browse local, show hidden, choose $VM_PATH
  * \"...may not have...permissions...correct this now?\": Yes
* Name: $VM_CDROM
* [x] Customize Before Install
  * Add Hardware
    * Storage
      * CDROM device
        * Select or create custom image
          * paste: $VM_CDROM
        * Bus type: IDE
    * Finish
  * Boot options
    * check \"IDE CDROM 1\"
  * Apply
  * Begin Install (top left button)
END
if [ "@$GUI" = "@TRUE" ]; then
    GUI="true"
elif [ "@$GUI" = "@True" ]; then
    GUI="true"
fi
if [ "@$GUI" = "@true" ]; then
    # Exit since the user wants to set up the machine using the
    # GUI instructions above.
    cat <<END
Specify --cli for command line interface, otherwise this script will
return an error code since no actions were performed (That is the case
now).
END
    exit 2
else
    cat <<END
GUI="$GUI" so VM creation process will be automated if options are
correct.
END
fi


# qemu is not a command unless you symlink it, so:
if [ "@$QEMU" = "@" ]; then
    # QEMU=qemu-system-x86_64
    # ^ full system emulation
    # ^
    # Spectre V2 : Spectre mitigation: LFENCE not serializing. Switching to generic pipeline
    # Initramfs unpacking failed: write error
    # /scripts/init-top/udev: line 16: /lib/systemd/systemd-udevd: not found
    #   [stuck on BusyBox (initramfs) prompt]
    # QEMU=qemu-x86_64
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
    if [ -f "$VM_CDROM" ]; then
        # $QEMU -cdrom $VM_CDROM -hda $VM_FILE_NAME -boot d -net nic -net user -m 196 -localtime
        #  ^ "qemu-system-x86_64: -localtime: invalid option"
        # $QEMU -cdrom $VM_CDROM -hda $VM_FILE_NAME -boot d -net nic -net user -m 196
        # ^ "WARNING: Image format was not specified for 'ubuntu14.qcow' and probing guessed raw.
        #         Automatically detecting the format is dangerous for raw images, write operations on block 0 will be restricted.
        #         Specify the 'raw' format explicitly to remove the restrictions."
        # $QEMU -hda $VM_FILE_NAME -cdrom $VM_CDROM -boot d -net nic -net user -m 196 -rtc base=localtime
        $QEMU -f $VM_FILE_NAME -c $VM_CDROM -boot d -net nic -net user -m 196 -rtc base=localtime
        # ^ DOESN'T WORK (see errors in comments near "QEMU=" lines further up)
    else
        echo "* $VM_CDROM does not exist, so the cdrom will not be installed to $VM_FILE_NAME."
    fi
else
    echo "* skipping install since QEMU_INITIALIZE is not true."
    echo "  Try 'cd `pwd`' then:"
    echo "  $QEMU -f $VM_FILE_NAME -c $VM_CDROM -net nic -net user -m 196 -rtc base=localtime"
    echo "  # or"
    if [ ! -f "`command -v qemu-system-x86_64`" ]; then
        echo "# install qemu-system-x86 then"
    fi
    echo "  qemu-system-x86_64 -drive file=$VM_FILE_NAME -net nic -net user -m 196 -rtc base=localtime"
fi
