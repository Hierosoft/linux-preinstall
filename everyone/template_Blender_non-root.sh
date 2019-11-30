#!/bin/bash

customDie(){
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}

echo
# see https://stackoverflow.com/questions/918886/how-do-i-split-a-string-on-a-delimiter-in-bash
program_name=Blender
template_name="$program_name project"
template_file_name="$template_name.blend"
IN="`kde4-config --path templates`"
# paths=$(echo $IN | tr ":" "\n")
src="templates/$template_file_name"
if [ ! -f "$src" ]; then
    try_path="$HOME/git/linux-preinstall/everyone/templates/$template_file_name"
    if [ -f "$try_path" ]; then
	src="$try_path"
    fi
fi
if [ ! -f "$src" ]; then
    customDie "$src is missing."
fi
# for path in $paths; do
# echo "path=$path"
# done
kde_templates1=$(echo $IN| cut -d':' -f 1)
echo "Adding '$src' to KDE templates: '$kde_templates1'..."
if [ ! -d "$kde_templates1" ]; then
    mkdir -p "$kde_templates1" || customDie "mkdir -p '$kde_templates1' failed."
fi

gnome_templates1="$HOME/Templates"
echo "Adding '$src' to GNOME templates: '$gnome_templates1'..."
if [ ! -d "$gnome_templates1" ]; then
    mkdir -p "$gnome_templates1" || customDie "mkdir -p '$gnome_templates1' failed."
fi
cp "$src" "$gnome_templates1/" || customDie "cp '$src' '$gnome_templates1/' failed."

echo "Done."
echo

kde_plasma_templates="$HOME/.local/share/templates"
kde_plasma_templates_source="$kde_plasma_templates/.source"
echo "Adding '$src' to GNOME templates: '$kde_plasma_templates_source'..."
if [ ! -d "$kde_plasma_templates_source" ]; then
    mkdir -p "$kde_plasma_templates_source" || customDie "mkdir -p '$kde_plasma_templates_source' failed."
fi
cp "$src" "$kde_plasma_templates_source/" || customDie "cp '$src' '$kde_plasma_templates_source/' failed."

# See https://askubuntu.com/questions/1086015/kde-plasma-does-not-give-the-extension-in-create-new-menu
# answered Oct 22 '18 at 18:08
# by user26687
# https://askubuntu.com/a/1086194
kde_plasma_template="$kde_plasma_templates/$template_name.desktop"
echo "Writing '$kde_plasma_template'..."
cat > "$kde_plasma_template" << END
[Desktop Entry]
Name=$template_name
Comment=Enter $template_name file name:
Type=Link
URL=.source/$template_file_name
Icon=blender
END
echo "Done."
echo
