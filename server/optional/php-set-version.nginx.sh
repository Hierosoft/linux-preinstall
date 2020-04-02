#!/bin/bash

# see also https://github.com/nextcloud/server/issues/11638#issuecomment-483868535

if [ -z "$1" ]; then
    echo
    echo "You must specify by a PHP version (such as 7.4)"
    echo
    echo
    exit 1
fi
reqested_ver=$1
# The next few lines are not for apache but are based on
# https://docs.nextcloud.com/server/14/admin_manual/installation/source_installation.html#ubuntu-installation-label
sudo apt install mariadb-server

for ver in 7.0 7.1 7.2 7.3 7.4 7.5 7.6 7.7 7.8 7.9
do
if [ "$reqested_ver" != "$ver" ]; then
    sudo apt remove -y php$ver-gd php$ver-json php$ver-mysql php$ver-curl php$ver-mbstring
    sudo apt remove php$ver-intl php-imagick php$ver-xml php$ver-zip
    sudo apt remove php$ver-fpm
fi
done

ver=$reqested_ver
sudo apt install php$ver-gd php$ver-json php$ver-mysql php$ver-curl php$ver-mbstring
sudo apt install php$ver-intl php-imagick php$ver-xml php$ver-zip
sudo apt install php$ver-fpm
# For WordPress plugins:
## As of 2020-04-01, sury is required for php7.4-mbstring (See https://github.com/wyveo/nginx-php-fpm/blob/master/Dockerfile)
echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/php.list
sudo apt install php$ver-mbstring


echo "enabling php$ver..."
sudo apt install php$ver-pgsql
# sudo apt install php$ver-sqlite3
sudo apt install php$ver-opcache
sudo apt install php$ver-readline
sudo apt install php$ver-memcached
sudo update-alternatives --set php /usr/bin/php$ver
# sudo systemctl reload nginx
