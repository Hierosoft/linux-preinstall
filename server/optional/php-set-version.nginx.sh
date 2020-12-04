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

for ver in 5.0 5.1 5.2 5.3 5.3 5.4 5.5 5.6 5.7 5.8 5.9 6.0 6.1 6.2 6.3 6.4 6.5 6.6 6.7 6.8 6.9 7.0 7.1 7.2 7.3 7.4 7.5 7.6 7.7 7.8 7.9 8.0 8.1 8.2 8.3 8.4 8.5 8.6 8.7 8.8 8.9 9.0
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
# ^ This installs php-imagick php5.6-imagick php7.0-imagick php7.1-imagick php7.2-imagick php7.2-intl php7.2-xml php7.2-zip php7.3-imagick
#     php7.4-imagick php8.0-imagick ttf-dejavu-core
#   for some reason.
sudo apt install php$ver-fpm
# For WordPress plugins:
## As of 2020-04-01, sury is required for php7.4-mbstring (See https://github.com/wyveo/nginx-php-fpm/blob/master/Dockerfile)
echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" > sudo tee /etc/apt/sources.list.d/php.list
sudo apt update
sudo apt install php$ver-mbstring


echo "enabling php$ver..."
sudo apt install php$ver-pgsql
# sudo apt install php$ver-sqlite3
sudo apt install php$ver-opcache
sudo apt install php$ver-readline
sudo apt install php$ver-memcached
sudo update-alternatives --set php /usr/bin/php$ver
# sudo systemctl reload nginx
