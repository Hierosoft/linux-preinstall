apt install tlp tlp-rdw || exit $?
tlp start || exit $?
tlp-stat -s
tlp-stat -b

# Install battery features:
apt install acpi-call-dkms || exit $?
if [ ! -f /etc/tlp.conf ]; then
    >&2 echo "Error: Missing /etc/tlp.conf"
    exit 1
fi
echo 'START_CHARGE_THRESH_BAT0=50' >> /etc/tlp.conf
echo 'STOP_CHARGE_THRESH_BAT0=80' >> /etc/tlp.conf


echo "Installing TLP GUI..."
flatpak install -y com.github.d4nj1.tlpui || exit $?
