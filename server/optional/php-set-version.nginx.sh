#!/bin/bash

# see also https://github.com/nextcloud/server/issues/11638#issuecomment-483868535

if [ -z "$1" ]; then
    echo
    echo "You must specify by a PHP version (such as 7.4)"
    echo
    echo
    exit 1
fi
CHANGE=true
if [ "@$2" = "@CHECKUP" ]; then
    CHANGE=false
fi
reqested_ver=$1
# The next few lines are not for apache but are based on
# https://docs.nextcloud.com/server/14/admin_manual/installation/source_installation.html#ubuntu-installation-label
if [ "@$CHANGE" = "@true" ]; then
    sudo apt install -y mariadb-server
fi

WARNING_SITES=""

NL=$'\n'
for ver in 5.0 5.1 5.2 5.3 5.3 5.4 5.5 5.6 5.7 5.8 5.9 6.0 6.1 6.2 6.3 6.4 6.5 6.6 6.7 6.8 6.9 7.0 7.1 7.2 7.3 7.4 7.5 7.6 7.7 7.8 7.9 8.0 8.1 8.2 8.3 8.4 8.5 8.6 8.7 8.8 8.9 9.0
do
if [ "$reqested_ver" != "$ver" ]; then
    if [ "@$CHANGE" = "@true" ]; then
        sudo apt remove -y php$ver-gd php$ver-json php$ver-mysql php$ver-curl php$ver-mbstring
        sudo apt remove -y php$ver-intl php-imagick php$ver-xml php$ver-zip
        sudo apt remove -y php$ver-fpm
    fi
    for SITE in `ls -t /etc/nginx/sites-available`
    do
        #echo "* checking $SITE"
        ANY_OLD="`grep $ver-fpm /etc/nginx/sites-available/$SITE`"
        if [ ! -z "$ANY_OLD" ]; then
            ANY_OLD=`echo $ANY_OLD | sed -r 's/( )+//g'`
            # ^ remove whitespace as per bruziuz' comment on
            # https://stackoverflow.com/questions/369758/how-to-trim-whitespace-from-a-bash-variable
            ANY_OLD_firstchar=${ANY_OLD:0:1}
            # ^ as per https://stackoverflow.com/a/27791269
            if [ "@$ANY_OLD_firstchar" = "@#" ]; then
                ANY_OLD=""
                # ^ ignore comments
            fi
        fi
        if [ ! -z "$ANY_OLD" ]; then
            # echo "  * found $ANY_OLD"
            WARNING_SITES="${WARNING_SITES}* /etc/nginx/sites-available/${SITE} uses: '${ANY_OLD}'${NL}"
            # STR="${H}"$'\n'"${W}"
            # ^ as per JDS's comment on https://stackoverflow.com/a/3182519
        #else
        #    echo "  * no $ver-fpm: '$ANY_OLD'"
        fi

    done
fi
done
echo
if [ "@$CHANGE" = "@true" ]; then
    echo "Removing other versions of php-related packages is complete."
fi
echo
echo "The following list should be empty (dpkg --get-selections | grep -i php): START"
sudo dpkg --get-selections | grep -i php
echo "END"
echo

ver=$reqested_ver
if [ "@$CHANGE" = "@true" ]; then
    sudo apt install -y php$ver-gd php$ver-json php$ver-mysql php$ver-curl php$ver-mbstring
    sudo apt install -y php$ver-intl php-imagick php$ver-xml php$ver-zip
    # ^ This installs php-imagick php5.6-imagick php7.0-imagick php7.1-imagick php7.2-imagick php7.2-intl php7.2-xml php7.2-zip php7.3-imagick
    #     php7.4-imagick php8.0-imagick ttf-dejavu-core
    #   for some reason.


    sudo apt install -y php$ver-fpm
    sudo systemctl enable php$ver-fpm
    sudo systemctl start php$ver-fpm
    sudo systemctl status php$ver-fpm

    # NOTE: at this point, the other services should already be masked,
    # so don't bother doing anything to them.

    # For WordPress plugins:
    ## As of 2020-04-01, sury is required for php7.4-mbstring (See https://github.com/wyveo/nginx-php-fpm/blob/master/Dockerfile)
    echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" > sudo tee /etc/apt/sources.list.d/php.list
    sudo apt update
    sudo apt install -y php$ver-mbstring


    echo "enabling php$ver..."
    sudo apt install php$ver-pgsql
    # sudo apt install php$ver-sqlite3
    sudo apt install php$ver-opcache
    sudo apt install php$ver-readline
    sudo apt install php$ver-memcached
    sudo update-alternatives --set php /usr/bin/php$ver
    # sudo systemctl reload nginx
    sudo systemctl restart nginx
fi
if [ ! -z "$WARNING_SITES" ]; then
    echo "WARNING: The following sites in /etc/nginx/sites-available still try to call old versions of php:"
    echo "$WARNING_SITES"
    echo
    echo "The correct location where the sock will be created is defined"
    echo "in: /etc/php/$requested_ver/fpm/pool.d/www.conf:"
    cat /etc/php/$requested_ver/fpm/pool.d/www.conf | grep sock
    # ^ according to https://www.xspdf.com/resolution/58767959.html
    echo
fi
