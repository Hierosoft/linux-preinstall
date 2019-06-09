#!/bin/sh
if [ ! -f "`command -v mogrify`" ]; then
    echo "ERROR (nothing done): this script requires mogrify command, such as from a recent ImageMagick package, as opposed to a version with the magick mogrify syntax."
fi
mogrify -format jpg *.png
