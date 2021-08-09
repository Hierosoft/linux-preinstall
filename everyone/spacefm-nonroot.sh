#!/bin/sh
printf "* setting column_width for name to 300..."
spacefm -s set column_width name 300
if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "FAILED"
fi
echo "  * The setting may not stay until the following SpaceFM issues are resolved:"
echo "     * [In tiling WMs, column width is rarely optimal #587](https://github.com/IgnorantGuru/spacefm/issues/587)"
echo "     * [Maximized window column widths not saved in 0.9.1 #382](https://github.com/IgnorantGuru/spacefm/issues/382)"
