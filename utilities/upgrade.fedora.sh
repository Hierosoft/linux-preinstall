if [ -z "$1" ]; then
    echo "You must specify the next Fedora version."
    exit 1
fi
sudo dnf upgrade -y --refresh
sudo dnf install -y dnf-plugin-system-upgrade
sudo dnf system-upgrade download -y --releasever=$1
#&& sudo dnf system-upgrade reboot
