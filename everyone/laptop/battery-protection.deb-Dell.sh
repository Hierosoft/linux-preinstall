

#echo "Dell-centric Dell Command Configure wrapper..."
#REPOS=~/Downloads/git/glynhudson
#DST="$REPOS/dell-charge-limit"
#if [ -d "$DST" ]; then
#    cd "$DST" || exit $?
#    git pull
#    echo
#    echo "Updated $DST:"
#else
#    mkdir -p "$REPOS"
#    git clone https://github.com/glynhudson/dell-charge-limit.git "$DST" || exit $?
#    echo
#    echo "Installed $DST:"
#fi
#ls "$DST"



CCTK_PATH=/opt/dell/dcc/cctk
if [ ! -f "`command -v cctk`" ]; then
    if [ ! -f  /opt/dell/dcc/cctk ]; then
	echo "Error: cctk not found in path nor \"$CCTK_PATH\". See <https://www.dell.com/support/kbdoc/en-us/000178000/dell-command-configure>"
        exit 1
    fi
else
    CCTK_PATH="`command -v cctk`"
fi
cd ~/Downloads
mkdir -p ~/Downloads

# As per <https://askubuntu.com/a/1491682/766334>
#   re <https://askubuntu.com/questions/1403778/upgrading-to-ubuntu-22-04-causes-libcrypto-errors-apt-dpkg-broken>:
# - I reposted the answer here: <https://www.dell.com/community/en/conversations/linux-general/dell-command-configure-breaks-openssl-and-other-things/647f9fa2f4ccf8a8de480dd8>
LIBSSL_PKG="libssl1.1_1.1.1w-0+deb11u1_amd64.deb"
if [ ! -f ~/Downloads/$LIBSSL_PKG ]; then
    wget -O ~/Downloads/$LIBSSL_PKG https://debian.mirror.ac.za/debian/pool/main/o/openssl/libssl1.1_1.1.1w-0%2Bdeb11u1_amd64.deb
fi
sudo dpkg -i "$LIBSSL_PKG"

sudo $CCTK_PATH -H primarybatterycfg
# ^ ". . .
#   The start value range should be 50-95 percentage,
#   the stop value range should be 55-100 percentage,
#   and the difference between the start and stop values should be greater than or equal to 5."
$CCTK_PATH --primarybatterycfg=custom:50-80

echo
