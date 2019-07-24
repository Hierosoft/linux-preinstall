#!/bin/bash
#see https://www.thegeekstuff.com/2011/07/rsync-over-ssh-without-password/
pubFile="$HOME/.ssh/id_rsa.pub"
usage() {
    echo
    echo "Usage:"
    echo
    echo "$0 <remoteHost> <something.pub>"
    echo "or"
    echo "$0 <remoteHost>"
    echo
    echo "* If a second parameter is not specified, $0"
    echo "  creates or uses the default file: '$pubFile'"
    echo "  (If that is not the default file on your version"
    echo "  of ssh-keygen, you'll have to specify your file)"
    echo
    echo
}
if [ ! -z "$1" ]; then
    remoteHost="$1"
fi
if [ -z "$remoteHost" ]; then
    echo "You must specify a remote host to which you want to connect without a password."
    exit 1
fi
noPubMsg=
if [ ! -z "$2" ]; then
    pubFile="$2"
    noPubMsg="* You specified '$pubFile' as the public key file, but it is not present. If it is not the default path, you must specify the same path below when asked."
fi
if [ ! -f "$pubFile" ]; then
    echo
    if [ ! -z "$noPubMsg" ]; then
        echo "$noPubMsg"
    fi
    echo "Reply with a BLANK passphrase below to allow future ssh connections to $remoteHost without entering a passphrase:"
    echo
    sleep 1
    ssh-keygen
else
    echo "Using existing $pubFile"
fi
echo "You must know the actual password for the server and enter it when asked:"
if [ ! -f "$pubFile" ]; then
    usage
    customDie ".pub key file '$pubFile' does not exist. Use the default path when running ssh-keygen, or specify your custom .pub file."
fi
ssh-copy-id -i $pubFile $1
