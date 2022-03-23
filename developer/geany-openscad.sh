#!/bin/bash

cat <<END

This script installs [Geany Configuration for OpenSCAD Editing](https://www.thingiverse.com/thing:263620)
[Creative Commons Attribution-ShareAlike 3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/)
(CC BY-SA 3.0)
by [cobra18t](https://www.thingiverse.com/cobra18t) March 05, 2014

Installing...
END

geanyConfDir=~/.config/geany
dstFiletypesDir="$geanyConfDir/filedefs"
mkdir -p $geanyConfDir

srcFiletypeConf="uploads_42_3c_3d_83_43_filetypes.OpenSCAD.conf"
# dstFiletypeConf="$geanyConfDir/filetypes.OpenSCAD.conf"
# ^ The documentation of OpenSCAD for Geany says this, but it is wrong!
dstFiletypeConf="$dstFiletypesDir/filetypes.OpenSCAD.conf"
# ^ You can't leave off the .conf even though many in /usr/share/geany/filedefs do
#   (add .conf according to file:///usr/share/doc/geany/html/index.html#id194)!

if [ ! -f "$srcFiletypeConf" ]; then
    echo "ERROR: You must run this script from the directory containing \"$srcFiletypeConf\"."
    exit 1
fi
printf "* copying \"$srcFiletypeConf\" to \"$dstFiletypeConf\"..."
cp "$srcFiletypeConf" "$dstFiletypeConf"
if [ $? -ne 0 ]; then
    echo "FAILED"
else
    echo "OK"
fi

#srcExtConf="uploads_af_c1_65_df_ff_filetype_extensions.conf"
#if [ ! -f "$srcExtConf" ]; then
#    echo "ERROR: You must run this script from the directory containing \"$srcExtConf\"."
#    exit 1
#fi
dstExtConf="$geanyConfDir/filetype_extensions.conf"

if grep -q "Script=OpenSCAD" "$dstExtConf"; then
    # ^ This is done again further down as a confirmation if adding it.
    echo "* INFO: \"$dstExtConf\" already contains \"Script=OpenSCAD\"."
    echo "Installation is complete."
    echo
    exit 0
fi

printf "* generating $dstExtConf..."

#if [ ! -f "$dstExtConf" ]; then
echo "[Extensions]" >> "$dstExtConf"
#fi
echo "OpenSCAD=*.scad;" >>  "$dstExtConf"
cat >> "$dstExtConf" <<END

# Note: restarting is required after editing groups
[Groups]
Script=OpenSCAD

END
if grep -q "Script=OpenSCAD" "$dstExtConf"; then
    echo "OK"
else
    echo "FAILED"
    echo "ERROR: Appending lines to \"$dstExtConf\" failed."
    exit 1
fi

echo "Installation is complete."
echo "* You must close & reopen Geany (AND any scad file(s) open)!"
echo
