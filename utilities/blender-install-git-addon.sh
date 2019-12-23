#!/bin/sh

customDie(){
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}

cd
if [ ! -d Downloads/git ]; then
  mkdir -p Downloads/git
fi
cd Downloads/git


for var in "$@"
do
    if [[ $var == --* ]]; then
        if [ "$var" = "--uninstall" ]; then
            enable_uninstall=true
        else
            echo "'$var' is not a recognized option."
            exit 1
        fi
    else
        url="$var"
    fi
done

if [ -z "$url" ]; then
    customDie "No URL was specified (http* URL ending in .git or other valid git URL should be specified as param to this script)."
fi

project_dot_git=${url##*/}
name=`echo "$project_dot_git" | cut -d'.' -f1`
echo "$name"
src=""
if [ ! -d "$name" ]; then
    if [ ! -f "`command -v git`" ]; then
        customDie "For downloading, $0 requires git, but it is not present."
    fi
    git clone "$url" || customDie "git clone \"$url\" failed in '`pwd`'."
    if [ -d "$name" ]; then
        cd "$name"
        src="$(pwd)"
    fi
else
    cd "$name"
    src="$(pwd)"
    if [ -f "`command -v git`" ]; then
        git pull || customDie "git pull failed in '`pwd`'."
    else
        echo "WARNING: git is not present, so '$src' will not be updated."
    fi
fi
if [ ! -d "$src" ]; then
    customDie "Cloning the URL $url did not result in a '$src' directory."
fi
#addons="/usr/local/share/blender/scripts/addons"
versions_path="$HOME/.blender"
if [ -d "$HOME/.config/blender" ]; then
    versions_path="$HOME/.config/blender"
fi
version_path=""
version=""
if [ ! -d "$versions_path" ]; then
    cat <<END
ERROR: $versions_path is missing determining the Blender addons path is not possible.
A path such as $HOME/.config/blender (or $HOME/.blender/2.79) must exist for this script to be able to detect the latest version and continue the add-on installation.
END
    exit 1
fi
for sv in 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99
do
    version_path="$versions_path/2.$sv"
    #echo "looking for $version_path..."
    if [ -d "$version_path" ]; then
        echo "found."
        cd "$version_path"
        version="2.$sv"
    fi
done
version_path="$versions_path/$version"
if [ ! -d "$version_path" ]; then
    echo
    echo "ERROR: Nothing done since $versions_path is missing version-specific directory so cannot determine Blender addons path"
    echo "--path such as $version_path must exist for this script to work."
    echo
    echo
    exit 2
fi
addons="$version_path/scripts/addons"
if [ ! -d "$addons" ]; then
    mkdir -p "$addons"
fi
echo
addon="$addons/$name"
if [ "@$enable_uninstall" = "@true" ]; then
    echo "Uninstalling $src/* files from $addons..."
    prev_dir="`pwd`"
    # See https://stackoverflow.com/questions/16773457/linux-bash-remove-all-files-which-are-in-one-directory-from-another-directory
    cd "$src"
    find . -exec rm -rf $addons/{} \;
    cd "$prev_dir"
else
    if [ -f "$src/__init__.py" ]; then
        echo "* installing the $name add-on to $addons as a new directory..."
        echo
        #rsync -rtv "$src/" "$addons"
        if [ -d "$addon" ]; then
            echo "Removing previously installed $addon..."
            rm -Rf "$addon"
        fi
        cp -R $src "$addons/"
    else
        echo "* installing the $name add-on py files directly to $addons..."
        echo
        #rsync -rtv "$src/" "$addons"
        if [ -d "$addon" ]; then
            echo "Removing incorrectly installed $addon..."
            rm -Rf "$addon"
        fi
        cp -R $src/* "$addons/"
    fi
    echo
    echo "You still need to enable the addon in Blender $version:"
    echo "  * File, User Preferences"
    echo "  * Addons"
    echo "  * Check the box for $name"
fi
echo
echo
