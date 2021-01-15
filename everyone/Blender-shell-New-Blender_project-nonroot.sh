#!/bin/sh
# Pass a full path to a blender executable or set BLENDER env variable
# to use a blender other than "blender".

BASEDIR=$(dirname "$0")

mkdir -p "$HOME/.local/share/templates/.source/"

if [ ! -z "$1" ]; then
    BLENDER="$1"
fi

is_custom_fname=false

if [ -z "$BLENDER" ]; then
    BLENDER=blender
else
    is_custom_fname=true
fi


PY="$BASEDIR/blender/save_blank_blender_project_to_templates.py"
$BLENDER --background --python $PY
TMP_BLEND="/tmp/blender_project.blend"
SOURCES="$HOME/.local/share/templates/.source"
BLEND_NAME="blender_project.blend"


B_AND_V=`$BLENDER --version | head -n1`

DT_CURRENT_NAME=Blender_project
if [ "@$is_custom_fname" == "@true" ]; then
    DT_CURRENT_NAME="$B_AND_V"
    BLEND_NAME="$B_AND_V project.blend"
fi
BLEND="$SOURCES/$BLEND_NAME"

# BLEND_BAK="$HOME/.local/share/templates/.source/blender_project.blend1"
BLEND_BAK="/tmp/blender_project.blend1"
if [ -f "$BLEND_BAK" ]; then
    rm "$BLEND_BAK"
fi
BLEND_DEPRECATED="$HOME/.local/share/templates/.source/Blender project.blend"
if [ -f "$BLEND_DEPRECATED" ]; then
    rm "$BLEND_DEPRECATED"
fi

if [ ! -f "$TMP_BLEND" ]; then
    echo "ERROR:"
    echo "'blender --background --python $PY' failed to produce $TMP_BLEND."
    exit 1
fi

mv "$TMP_BLEND" "$BLEND"
if [ $? -ne 0 ]; then
    echo "ERROR:"
    echo "'mv \"$TMP_BLEND\" \"$BLEND\" failed."
    exit 1
fi

DT_DEPRECATED="$HOME/.local/share/templates/Blender project.desktop"
if [ -f "$DT_DEPRECATED" ]; then
    rm "$DT_DEPRECATED"
fi

cat > $HOME/.local/share/templates/$DT_CURRENT_NAME.desktop << END
[Desktop Entry]
Name=$B_AND_V project
Comment=Enter Blender project file name:
Type=Link
URL=.source/$BLEND_NAME
Icon=blender
END
