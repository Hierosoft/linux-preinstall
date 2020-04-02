#!/bin/sh

# see also https://github.com/nextcloud/server/issues/11638#issuecomment-483868535

if [ -z "$1" ]; then
    echo
    echo "You must specify by a PHP version (such as 7.4)"
    echo "php is using (so you should probably use what is shown from"
    echo "the output of 'sudo apache2ctl -M | grep php' below):"
    sudo apache2ctl -M | grep php
    echo
    echo
    exit 1
fi
ver=$1
# next 9 lines are from https://docs.nextcloud.com/server/14/admin_manual/installation/source_installation.html#ubuntu-installation-label
sudo apt install apache2 mariadb-server libapache2-mod-php$ver
sudo apt install php$ver-gd php$ver-json php$ver-mysql php$ver-curl php$ver-mbstring
sudo apt install php$ver-intl php-imagick php$ver-xml php$ver-zip
sudo a2enmod rewrite
sudo a2enmod headers
sudo a2enmod env
sudo a2enmod dir
sudo a2enmod mime
sudo a2enmod ssl

sudo a2dismod php7.0
sudo a2dismod php7.1
sudo a2dismod php7.2
sudo a2dismod php7.3
echo "enabling php$ver..."
sudo a2enmod php$ver
sudo apt install php$ver-pgsql
# sudo apt install php$ver-sqlite3
sudo apt install php$ver-opcache
sudo apt install php$ver-readline
sudo apt install php$ver-memcached
sudo update-alternatives --set php /usr/bin/php$ver
sudo systemctl restart apache2
