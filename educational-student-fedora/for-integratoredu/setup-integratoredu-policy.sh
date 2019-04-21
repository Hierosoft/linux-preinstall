#!/bin/sh
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}

integratoredu_url="$1"  # "http://login.axlemedia.net/sign"
if [ -z "$integratoredu_url" ]; then
    echo "You must modify $me so integratoredu_url is your integratoredu instance."
    exit 1
fi

cd /tmp
iedu_update_other_name="hourly"
cron_freq="hourly"
src_name="iedu-cs-$iedu_update_other_name"
dest_name="/etc/cron.$cron_freq/iedu-cs-$iedu_update_other_name"
if [ -f "$src_name" ]; then
  rm -f "$src_name"
fi
if [ -f "$dest_name" ]; then
  rm -f "$dest_name"
fi
local_name="$src_name"
wget --output-document="$src_name" $integratoredu_url/cppr?unit=0&kernel=linux&access_level=root&machine_group=StudentMachines&script_name=$iedu_update_other_name
good_flag="update_enable: $THIS_TRUE"

if grep -q "$good_flag" "$local_name"; then
    mv -f "$src_name" "$dest_name" || customDie "Cannot mv $src_name $dest_name"
    chmod +x "$dest_name"
    # and run it NOW:
    $dest_name
else
    echo "ERROR: not using $local_name since not downloaded properly (no $good_flag in):"
    cat "$local_name"
    rm -f "$local_name"
fi
