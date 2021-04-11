#!/bin/bash
PREFIX="$HOME/.local"
src_dt="dist/share/applications/install_any.desktop"
dst_dt="$PREFIX/share/applications/install_any.desktop"
printf "* copying \"$dst_dt\"..."
cp "$src_dt" "$dst_dt"
if [ $code -eq 0 ]; then
    echo "OK"
else
    echo "FAILED"
    exit $code
fi
printf "* installing \"$dst_dt\"..."
xdg-desktop-icon install --novendor $dst_dt
code=$?
if [ $code -eq 0 ]; then
    echo "OK"
else
    echo "FAILED"
    exit $code
fi
