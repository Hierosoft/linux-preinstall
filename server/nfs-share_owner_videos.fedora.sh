#!/bin/sh
# See [NFS : Configure NFS Server](https://www.server-world.info/en/note?os=Fedora_31&p=nfs&f=1)
# and [5.4.3. DO NOT USE THE NO_ROOT_SQUASH OPTION](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/4/html/security_guide/s2-server-nfs-noroot)

source $HOME/.config/linux-preinstall/globals.rc
if [ $? -ne 0 ]; then
    echo "ERROR: 'source $HOME/.config/linux-preinstall/globals.rc' failed."
    echo "You must run linux-preinstall/setup.sh first."
    exit 1
fi
source $LINUX_PREINSTALL/api.rc
if [ $? -ne 0 ]; then
    echo "ERROR: 'source $LINUX_PREINSTALL/api.rc' failed."
    echo "You must run linux-preinstall/setup.sh first."
    exit 1
fi

distro_install \
    nfs-utils
firewall-cmd --add-service=nfs --permanent
firewall-cmd --add-service={nfs3,mountd,rpc-bind} --permanent
firewall-cmd --reload
DOMAIN_LINE="Domain = home.local"
echo "$DOMAIN_LINE"
SHARE_LINE="/home/owner/Videos 192.168.1.0/24(rw,anonuid=1000,anongid=1000)"
echo "If the line above isn't right, press Ctrl+C to exit now and write a better line to /etc/exports manually (then add a line like '$SHARE_LINE' to /etc/exports and run 'systemctl enable --now rpcbind nfs-server')."
echo "3..."
sleep 1
echo "2..."
sleep 1
echo "1..."
sleep 1
echo "$DOMAIN_LINE" >> /etc/idmapd.conf
echo "$SHARE_LINE"
echo "If the line above isn't right, press Ctrl+C to exit now and write a better line to /etc/exports manually (then run 'systemctl enable --now rpcbind nfs-server')."
echo "3..."
sleep 1
echo "2..."
sleep 1
echo "1..."
sleep 1
echo "$SHARE_LINE" >> /etc/exports
systemctl enable --now rpcbind nfs-server
