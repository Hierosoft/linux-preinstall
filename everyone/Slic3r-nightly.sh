#!/bin/sh
customDie(){
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
installer_path=../utilities/install_any.py

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
linux_preinstall_repo_path="$( dirname $DIR )"
#if [ ! -f "$installer_path" ]; then
# always get absolute path
    # See https://stackoverflow.com/questions/59895/get-the-source-directory-of-a-bash-script-from-within-the-script-itself
    try_path="$linux_preinstall_repo_path/utilities/install_any.py"
    if [ -f "$try_path" ]; then
        installer_path="$try_path"
    fi
#fi
if [ ! -f "$installer_path" ]; then
    customDie "You must run this from the utilities directory so \"$installer_path\" can be found."
fi
if [ ! -d ~/Downloads ]; then
    mkdir ~/Downloads || customDie "'mkdir ~/Downloads' failed."
fi
cd ~/Downloads || customDie "'cd ~/Downloads' failed."
latest_name=Slic3r-master-latest.AppImage
url=https://dl.slic3r.org/dev/linux/$latest_name
wget -O $latest_name $url || customDie "'wget $url' failed."
latest_path="`pwd`/$latest_name"
python3 "$installer_path" "$latest_path" || customDie "'python \"$installer_path\" \"$latest_name\"' failed."
