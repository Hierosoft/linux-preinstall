me=`basename "$0"`
echo "NOTE: Only tested for netbeans 8.2 on fedora 27."
sudo dnf install -y wget java-1.8.0-openjdk java-1.8.0-openjdk-devel
cd $HOME/Downloads
SRC_INSTALLER_NAME="netbeans-8.2-javase-linux.sh"
SRC_INSTALLER_PATH="$SRC_INSTALLER_NAME"
if [ -f "$SRC_INSTALLER_NAME" ]; then
  rm -f "$SRC_INSTALLER_NAME"
fi
wget -O $SRC_INSTALLER_NAME http://download.netbeans.org/netbeans/8.2/final/bundles/$SRC_INSTALLER_NAME
chmod +x $SRC_INSTALLER_NAME
echo "installing netbeans (this may take a while)..."
./$SRC_INSTALLER_PATH --silent
