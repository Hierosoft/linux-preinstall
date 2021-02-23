#See https://www.digitalocean.com/community/tutorials/how-to-set-up-vsftpd-for-anonymous-downloads-on-ubuntu-16-04
#(except change /var/ftp/pub to the $PUBDIR as set below)
if [ -z $PUBDIR ]; then
    PUBDIR=/var/ftp/pub
    if [ -d /tank/services ]; then
        PUBDIR=/tank/services/ftp/pub
    fi
fi
mkdir -p $PUBDIR
chown nobody:nogroup $PUBDIR
echo "vsftpd test file" | tee $PUBDIR/test.txt

echo "In /etc/vsftpd.conf, set:"
cat << END
anonymous_enable=YES
# local_enable=NO  # digitalocean says to do this
anon_root=$PUBDIR
#
# Stop prompting for a password on the command line.
no_anon_password=YES
#
# Show the user and group as ftp:ftp, regardless of the owner.
# hide_ids=YES
#^ The setting above is from the digitalocean readonly ftp tutorial
#
# Limit the range of ports that can be used for passive FTP
# pasv_min_port=40000
# pasv_max_port=50000
#^ The ports above are from the digitalocean readonly ftp tutorial
#The below ports are from a standard vsftpd setup tutorial:
pasv_min_port=10090
pasv_max_port=10100
END
