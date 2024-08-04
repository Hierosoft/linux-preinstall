#!/bin/bash
cd /lib/x86_64-linux-gnu || exit 1
TOTAL=`ls | wc -l`
COUNT=0
BAD=0
for filename in *; do
    >&2 printf "\rChecking $COUNT/$TOTAL  "
    # ^ Extra space is necessary since stderr output from dpkg (if the file is not from a package [is bad])
    # COUNT=$((COUNT+1))
    let "COUNT=COUNT+1"
    if [ ! -L "$filename" ]; then
        _output=`dpkg -S $filename`
        if [ -z "$_output" ]; then
            echo $filename
            let "BAD=BAD+1"
        # else there is a result and the file is from a package. Example:
        # libkeyutils1:amd64: /lib/x86_64-linux-gnu/libkeyutils.so.1.8
        fi
    fi
done
>&2 echo "Found $BAD bad file(s)!"
if [ $BAD -ne 0 ]; then
    echo "If one of the files is a libkeytools file, you can try to clean the infection by running clean-libkeyutils-rootkit.sh!"
fi
