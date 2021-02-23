#!/bin/sh

# see also https://github.com/nextcloud/server/issues/11638#issuecomment-483868535

if [ -z "$1" ]; then
    echo
    echo "You must specify by a PHP version (such as 7.4)"
    echo "php is using (so you should probably use what is shown from"
    echo "the output of 'apache2ctl -M | grep php' below):"
    apache2ctl -M | grep php
    echo
    echo
    exit 1
fi
ver=$1
# next 9 lines are from https://docs.nextcloud.com/server/14/admin_manual/installation/source_installation.html#ubuntu-installation-label
apt install -y apache2 mariadb-server libapache2-mod-php$ver
apt install -y php$ver-gd php$ver-json php$ver-mysql php$ver-curl php$ver-mbstring
apt install -y php$ver-intl php-imagick php$ver-xml php$ver-zip
a2enmod rewrite
a2enmod headers
a2enmod env
a2enmod dir
a2enmod mime
a2enmod ssl

echo "* disabling old modules..."
# for OTHER_VER in 7.0 7.1 7.2 7.3 7.4 7.5 7.6 7.7 7.8 7.9
# do
#     a2dismod php$OTHER_VER 1>/dev/null 2>&1
# done
# List modules: apachectl -M | awk '{print $1}' | grep php
# List modules without _modules suffix:
# apachectl -M | awk '{print $1}' | awk -F_ '{print $1}' | grep php
module_count=0
for MODULE_NAME in `apachectl -M | awk '{print $1}' | awk -F_ '{print $1}' | grep php`
do
    a2dismod $MODULE_NAME 1>/dev/null 2>&1
    module_count=$((module_count+1))
    if [ $? -eq 0 ]; then
        echo "- a2dismod $MODULE_NAME...OK"
    else
        echo "- a2dismod $MODULE_NAME...FAILED"
    fi
done
echo "  - done ($module_count PHP modules)"

echo "enabling php$ver..."
a2enmod php$ver
apt install -y php$ver-pgsql
# apt install -y php$ver-sqlite3
apt install -y php$ver-opcache
apt install -y php$ver-readline
apt install -y php$ver-memcached
update-alternatives --set php /usr/bin/php$ver
systemctl restart apache2
