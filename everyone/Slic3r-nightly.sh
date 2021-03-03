#!/bin/sh
me=$0
myPath="`realpath "$0"`"
myDir="`dirname "$myPath"`"
myName="Slic3r Nightly Installer"
customDie(){
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
linux_preinstall_repo_path=".."
#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
trylinux_preinstall_repo_path=`dirname "$myDir"`
if [ -f "$trylinux_preinstall_repo_path/utilities/install_any.py" ]; then
    linux_preinstall_repo_path="$trylinux_preinstall_repo_path"
fi
installer_path="$linux_preinstall_repo_path/utilities/install_any.py"

#linux_preinstall_repo_path="$( dirname $DIR )"
#if [ ! -f "$installer_path" ]; then
# always get absolute path
    # See https://stackoverflow.com/questions/59895/get-the-source-directory-of-a-bash-script-from-within-the-script-itself
    #try_path="$linux_preinstall_repo_path/utilities/install_any.py"
    #if [ -f "$try_path" ]; then
    #    installer_path="$try_path"
    #fi
#fi
if [ ! -f "$installer_path" ]; then
    customDie "You must run this from the utilities directory so \"$installer_path\" can be found."
fi
if [ ! -d ~/Downloads ]; then
    mkdir ~/Downloads || customDie "'mkdir ~/Downloads' failed."
fi
cd ~/Downloads || customDie "'cd ~/Downloads' failed."
latest_name=Slic3r-master-latest.AppImage
DL_PAGE_URL=https://dl.slic3r.org/dev/linux/
if [ -z "$SLICER_APPIMAGE_URL" ]; then
    SLICER_APPIMAGE_URL=https://dl.slic3r.org/dev/linux/$latest_name
fi
if [ ! -z "$1" ]; then
    SLICER_APPIMAGE_URL=$1
fi
if [ ! -f "`command -v wget`" ]; then
    echo "Error: $myName $me requires wget."
    exit 1
fi
wget -O $latest_name.tmp $SLICER_APPIMAGE_URL
if [ $? -ne 0 ]; then
    echo
    echo
    echo "Error: Downloading $SLICER_APPIMAGE_URL failed. Try specifying a URL can be found by right-clicking and copying a link from $DL_PAGE_URL using a param or by setting SLICER_APPIMAGE_URL in the environment."
    echo "Example:"
    echo "$me https://dl.slic3r.org/dev/linux/branches/Slic3r-1.3.1-dev-24fc045-PR5010-x86_64.AppImage"
    echo
    exit 1
elif [ ! -s $latest_name.tmp ]; then
    echo
    echo
    echo "Error: The file downloaded from $SLICER_APPIMAGE_URL is empty."
    echo
    exit 1
fi
mv -f $latest_name.tmp $latest_name
latest_path="`pwd`/$latest_name"
python3 "$installer_path" "$latest_path" || customDie "'python \"$installer_path\" \"$latest_name\"' failed."
