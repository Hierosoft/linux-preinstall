#!/bin/bash

thisAlert(){
    # notify-send 'javajar' "$1" &
    xmessage -center "$1"
    exit 1
}

if [ ! -f "$1" ]; then
    thisAlert "ERROR: The file \"$1\" does not exist."
    exit 1
fi
if [ ! -f "`command -v java`" ]; then
    thisAlert "ERROR: The java command is not available."
    exit 1
fi
java -jar "$1" || sleep 5
