#!/bin/bash

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

url=""
src=""
IN_PLACE=false

for var in "$@"
do
    if [[ $var == --* ]]; then
        if [ "$var" = "--uninstall" ]; then
            enable_uninstall=true
        elif [ "$var" = "--in-place" ]; then
            IN_PLACE=true
        else
            echo "'$var' is not a recognized option."
            exit 1
        fi
    else
        if [ -d "$var" ]; then
            if [ "x$src" != "x" ]; then
                echo "The source directory was already set."
                exit 1
            fi
            src="$var"
        else
            url="$var"
        fi
    fi
done

if [ -z "$url" ]; then
    if [ -z "$src" ]; then
        customDie "No directory nor URL was specified (http* URL ending in .git or other valid git URL should be specified as param to this script)."
    fi
fi

project_dot_git=${url##*/}
name=`echo "$project_dot_git" | cut -d'.' -f1`
echo "$name"

if [ "x$src" != "x" ]; then
    name="`basename $src`"
    echo "* installing local \"$src\" as $name"
elif [ ! -d "$name" ]; then
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

for mv in 3 2
do
    for sv in 3 2 1 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
    do
        # Check for 3.3 first since that is stable (3.3.x use /3.3/ not /3.3.*/) 
        version_path="$versions_path/$mv.$sv"
        #echo "looking for $version_path..."
        if [ -d "$version_path" ]; then
            echo "* detected \"$version_path\""
            cd "$version_path"
            version="$mv.$sv"
            break
        fi
    done
    if [ "x$version" != "x" ]; then
        break
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
if [ -z "$name" ]; then
    echo "Error: The addon name wasn't set."
    exit 1
fi
addon="$addons/$name"
if [ "@$enable_uninstall" = "@true" ]; then
    echo "Uninstalling $src/* files from $addons..."
    prev_dir="`pwd`"
    # See https://stackoverflow.com/questions/16773457/linux-bash-remove-all-files-which-are-in-one-directory-from-another-directory
    cd "$src"
    find . -exec rm -rf $addons/{} \;
    cd "$prev_dir"
else
    src_param=""
    if [ -f "$src/__init__.py" ]; then
        echo "* installing the $name add-on to $addons as a new directory..."
        echo
        #rsync -rtv "$src/" "$addons"
        if [ -L "$addon" ]; then
            echo "Removing previously installed $addon symlink..."
            rm -f "$addon"
        elif [ -d "$addon" ]; then
            echo "Removing previously installed $addon directory..."
            rm -Rvf "$addon"
        fi
        src_param="$src"
        if [ "x$IN_PLACE" = "xtrue" ]; then
            ln -s $src "$addons/"
            echo "* created symlink in $addons/"
            ls -la addons/`basename $src`
        else
            cp -Rv $src "$addons/"
        fi
    else
        echo "* installing the $name add-on py files directly to $addons..."
        echo
        #rsync -rtv "$src/" "$addons"
        if [ -L "$addon" ]; then
            echo "Removing incorrectly installed $addon symlink..."
            rm -f "$addon"
        elif [ -d "$addon" ]; then
            echo "Removing incorrectly installed $addon..."
            rm -Rf "$addon"
        fi

        src_param="$src/*"
        if [ "x$IN_PLACE" = "xtrue" ]; then
            ln -s $src/* "$addons/"
            echo "* created symlinks in $addons/:"
            ls $src
        else
            cp -R $src/* "$addons/"
        fi
    fi
    echo
    echo
    echo "You still need to enable the addon in Blender $version:"
    echo "* Only the following versions of Blender will use the user $version/scripts directory:"
    echo "  - The system's Blender: \"`command -v blender`\" (`blender --version | head -n1`)"
    echo "  - Blender AppImages"
    echo "  - Blender versions compiled from source but not run-in-place."
    echo "* If you don't have $version in one of those formats, install in your version such as:"
    try_addons="$HOME/Downloads/blender-3.3.1-linux-x64/3.3/scripts"
    if [ "x$IN_PLACE" = "xtrue" ]; then
        echo "ln -s $src_param \"$try_addons/\""
    else
        echo "cp -R $src_param \"$addons/\""
    fi
    echo "* Open the correct Blender above then File, User Preferences"
    echo "* Addons"
    echo "* Check the box for $name (or earch for \"DirectX Importer\" first)"
fi
echo
echo
