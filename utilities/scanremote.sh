#!/bin/bash

if [ -z "$CONFIG_PATH" ]; then
    CONFIG_PATH="$HOME/.config/scanremote"
fi
SETTINGS_PATH="$CONFIG_PATH/settings.rc"

usage() {
    cat <<END
USAGE:
$0 <filename> [<remote_host>] [--<option>]
(You don't have to specify [] options, but remote_host is only
optional if you specified it before--in which case
remote_host from $SETTINGS_PATH is used.)

--<option>      changes ANY option in $SETTINGS_PATH
                Therefore, remote_host is the same as having filename
                followed by another unnamed parameter.
--scanner_name  specifies the remote scanner name
                (otherwise, the first scanner available from
                \"ssh <remote_host> 'scanimage -L'\" will be used.
--rotate        specifies rotation: 90, 180, or 270
                (only works if remote CLIENT has jpegtran
                such as from the libjpeg-turbo-utils package)

Each option must be followed by a space then a value.

END

}

customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
if [ -f "$SETTINGS_PATH" ]; then
    echo "* Using the following settings from $SETTINGS_PATH:"
    # cat "$SETTINGS_PATH"
    while read line; do
	if [ ! -z "$line" ]; then
	    echo "  $line"
	fi
    done <"$SETTINGS_PATH"
    source "$SETTINGS_PATH"
fi
prev_remote_user="$remote_user"
prev_remote_host="$remote_host"
prev_scanner_name="$scanner_name"
if [ -z "$remote_user" ]; then
    remote_user="$USER"
    echo "* using '$remote_user' (your local username) as remote_user."
    echo "  To change it, use"
    echo "  --remote_user <remote_user>"
    echo "  or set remote_user in $SETTINGS_PATH."
fi

new_scan_name=
new_remote_host=

set_var=
for var in "$@"
do
    if [ ! -z "$set_var" ]; then
	let $set_var=$var
	echo "* You specified '$var' for $set_var."
	set_var=
    elif [[ $var == --* ]]; then
	# echo "* about to set ${var:2}..."
	set_var="${var:2}"
    else
	if [ -z "$new_scan_name" ]; then
	    new_scan_name="$var"
	    scan_name="$var"
	elif [ -z "$new_remote_host" ]; then
	    new_remote_host="$var"
	    remote_host="$var"
	else
	    usage
	    customDie "You cannot specify a third unnamed parameter ('$var' was encountered unexpectedly)."
	fi
    fi
done

if [ -z "$remote_host" ]; then
    usage
    customDie "You must specify a remote host."
fi

ext=jpg
fmt=jpeg

if [ -z "$scan_name" ]; then
    usage
    customDie "You must specify a new file name (without extension)."
fi

if [ -f "$scan_name.$ext" ]; then
    customDie "There is already a file named '$scan_name.$ext'"
fi

save_config() {
    echo "remote_user=\"$remote_user\"" > $SETTINGS_PATH
    echo "remote_host=\"$remote_host\"" >> $SETTINGS_PATH
    echo "scanner_name=\"$scanner_name\"" >> $SETTINGS_PATH
    echo "* saved settings to '$SETTINGS_PATH'."
}

enable_save=false

if [ "@$prev_remote_user" != "@$remote_user" ]; then enable_save=true; fi
if [ "@$prev_remote_host" != "@$remote_host" ]; then enable_save=true; fi
if [ "@$prev_scanner_name" != "@$scanner_name" ]; then enable_save=true; fi

if [ "@enable_save" = "@true" ]; then
    save_config
fi

if [ -z "$remote_host" ]; then
    usage
    customDie "You must specify remote_host as second unnamed param or in $SETTINGS_PATH"
fi
this_scanner=
if [ -z "$scanner_name" ]; then
    echo "* listing scanners..."
    ssh $remote_user@$remote_host 'scanimage -L' > "$CONFIG_PATH/scanners.list"
    echo >> "$CONFIG_PATH/scanners.list"
    # ^ must end with newline or `while read p; do` will miss last line.
    # cat "$CONFIG_PATH/scanners.list"
    PREV_IFS=$IFS
    # See https://stackoverflow.com/questions/1521462/looping-through-the-content-of-a-file-in-bash
    # for line in ("$CONFIG_PATH/scanners.list"); do
    # while IFS="" read -r line || [ -n "$line" ]; do
    # below trims leading whitespace, interprets backslash sequences,
    # and skips trailing line; longer `while ...` above does not.
    line_i=1
    count=0
    while read line; do
	if [ "${line:0:8}" = 'device `' ]; then
	    PREV_IFS=$IFS
	    this_scanner="${line:8}"
	    IFS="'" read -ra parts <<< "$this_scanner"
	    #for i in "${ADDR[@]}"; do
	    #done
	    this_scanner="${parts[0]}"
	    if [ ! -z "$this_scanner" ]; then
		echo "$line_i. found a scanner: \"${this_scanner}\"."
		echo "   ${line}"
		if [ -z "$scanner_name" ]; then
		    scanner_name="$this_scanner"
		    echo "   - using first scanner in list: \"$scanner_name\""
		fi
		let count++
	    else
		echo "$line_i. '${line}' seems to be missing scanner name enclosed in '\`"
	    fi
	    IFS=PREV_IFS
	else
	    if [ ! -z "$line" ]; then
	        echo "$line_i. '${line}' was not a recognized scanner format"
	    fi
	fi
	let line_i++
    done <"$CONFIG_PATH/scanners.list"
    if [ "$count" = "0" ]; then
	echo "* There were 0 scanners found by running 'scanimage -L' on remote server, which yielded:"
	cat "$CONFIG_PATH/scanners.list"
    fi
fi
if [ -z "$scanner_name" ]; then
    usage
    customDie "You must specify --scanner_name or set scanner_name in $SETTINGS_PATH or allow it to auto-detect"
else
    if [ -z "$this_scanner" ]; then
	echo "* using scanner from '$SETTINGS_PATH': \"$scanner_name\""
    else
	save_config
    fi
fi



echo "* scanning '$scan_name'..."
ssh $remote_user@$remote_host "scanimage -d \"$scanner_name\" --format=$fmt > $scan_name.$ext"
echo "* transferring '$scan_name.$ext' to you ($HOSTNAME)..."
ssh $remote_user@$remote_host "rsync $scan_name.$ext $HOSTNAME:`pwd`"
if [ -f "$scan_name.$ext" ]; then
    echo "* done aquiring '$scan_name.$ext'"
else
    customDie "* Running scanimage and rsync on $remote_host as $remote_user did not result in any '$scan_name.$ext'"
fi
exit 0
