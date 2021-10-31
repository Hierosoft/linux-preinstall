#!/bin/bash
DESTRC="$HOME/.jwmrc"
wget -O "$DESTRC.tmp" https://oldcoder.org/jwmrc.txt
if [ $? -ne 0 ]; then
    echo "Error: 'wget -O \"$DESTRC.tmp\" https://oldcoder.org/jwmrc.txt' failed."
    exit 1
fi
if [ -f "$DESTRC" ]; then
    if [ ! -f "$DESTRC.1st" ]; then
        mv "$DESTRC" "$DESTRC.1st"
    elif [ ! -f "$DESTRC.bak" ]; then
        mv "$DESTRC" "$DESTRC.bak"
    fi
fi
printf "* installing $DESTRC..."
mv "$DESTRC.tmp" "$DESTRC"
if [ $? -ne 0 ]; then
    echo "Error: 'mv \"$DESTRC.tmp\" \"$DESTRC\"' failed."
    exit 1
else
    echo "OK"
fi
