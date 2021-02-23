#!/bin/sh

# See also https://dev.mysql.com/doc/refman/8.0/en/installing.html

# linux_preinstall_interactive is a flag variable specific to the
# linux-preinstall project and is reserved for future use.
linux_preinstall_interactive=true

#See https://dev.mysql.com/doc/mysql-repo-excerpt/5.7/en/linux-installation-yum-repo.html
#(this method seems to require manual steps)
#echo "You must first download mysql80-community-release-fc29-2.noarch.rpm from https://dev.mysql.com/downloads/repo/yum/"
#sudo dnf install mysql80-community-release-fc29-2.noarch.rpm
#yum repolist all | grep mysql
#exit 0

#dnf install -y gpg
#gpg --keyserver pgpkeys.mit.edu --recv-key 8c718d3b5072e1f5
##results:
##gpg: requesting key 5072E1F5 from hkp server pgpkeys.mit.edu
##gpg: key 5072E1F5: public key "MySQL Release Engineering <mysql-build@oss.oracle.com>" imported
##gpg: no ultimately trusted keys found
##gpg: Total number processed: 1
##gpg:               imported: 1


# Not Tried: https://dev.mysql.com/doc/mysql-repo-excerpt/5.6/en/linux-installation-yum-repo.html


# Below is from https://dev.mysql.com/doc/refman/5.6/en/checking-gpg-signature.html
gpg --recv-keys 5072E1F5
#results:
#gpg: requesting key 5072E1F5 from hkp server keys.gnupg.net
#gpg: key 5072E1F5: "MySQL Release Engineering <mysql-build@oss.oracle.com>" not changed
#gpg: Total number processed: 1
#gpg:              unchanged: 1

#gpg -k lists public keys (guessed--since -K shows private). Results:
yes | cp -f $HOME/.gnupg/pubring.gpg /etc/pki/rpm-gpg/RPM-GPG-KEY-mysql

if [ ! -f "/etc/pki/rpm-gpg/RPM-GPG-KEY-mysql" ]; then
    echo "Failed to create /etc/pki/rpm-gpg/RPM-GPG-KEY-mysql from $HOME/.gnupg/pubring.gpg"
fi

# Steps below are from <https://tecadmin.net/install-mysql-8-on-fedora/>
# CAREFUL pasting this--youll need to add backslash before dollar signs or get:
#MySQL 8.0 Community Server                                                                                                   32  B/s |  16  B     00:00
#Failed to synchronize cache for repo 'mysql80-community'
#Ignoring repositories: mysql80-community
#Last metadata expiration check: 0:11:35 ago on Sun 16 Jun 2019 12:32:14 AM EDT.
#No match for argument: mysql-community-server
#Error: Unable to find a match

cat > /etc/yum.repos.d/mysql-community.repo << END
[mysql80-community]
name=MySQL 8.0 Community Server
baseurl=http://repo.mysql.com/yum/mysql-8.0-community/fc/$releasever/$basearch/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql
END

#dnf config-manager --set-enabled mysql80-community


dnf install -y mysql-community-server || exit 1
dnf install -y mysql-connector-java

service_name=mysql
systemctl enable $service_name.service || service_name=mysqld
if [ "$service_name" = "mysql" ]; then
    echo "trying old service name $service_name..."
    systemctl enable $service_name.service
    systemctl start $service_name.service
else
    systemctl start $service_name.service
fi
echo "According to <https://dev.mysql.com/doc/refman/8.0/en/default-privileges.html>,"
echo "Done."
cat <<END
"Installation using RPM packages generates an initial random password,
which is written to the server error log. . . For data directory
initialization performed manually using mysqld --initialize, mysqld
generates an initial random password, marks it expired, and writes it to
the server error log."
END
echo "Therefore the password should appear below via tail /var/log/mysqld.log:"
tail /var/log/mysqld.log
mysql -u root -p
echo
echo
echo "Please review <https://dev.mysql.com/doc/refman/8.0/en/postinstallation.html>"
echo
echo
