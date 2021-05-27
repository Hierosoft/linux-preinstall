#!/bin/sh

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

if [ -z "$ver" ]; then
    if [ -z "$1" ]; then
        echo "You must specify a php version such as 7.3"
        exit 1
    fi
    ver="$1"
fi

distro_install \
    php$ver-cli \
    php$ver-common \
    php$ver-bz2 \
    #php$ver-mysql
    php$ver-dev \
    php$ver-fpm \
    #php$ver-dompdf
    php$ver-apcu \
    #php$ver-server
    php$ver-redis
    #php$ver-smbclient
    #php$ver-ldap
# ^ MISSING from debian 10 buster:
#   - dompdf
# ^ installed (not in php-set-version*.sh):
#   - apcu bz2 dev redis
cat <<END
Done.
Make sure you run the php-set-version... script matching your distro to install packages common to your distro before running this script.
 To verify the system requirements, run:
 ./nextcloud-checkup.py $ver
You will probably have to reboot even if memcached and redis services say they are ok!
Try:
  - Truncate the log to move old errors and set ownership properly
    so that nextcloud can write to it.
    ```
    NC_WEB=/var/www/nextcloud
    # ^ where /var/www/nextcloud is your installation
    NC_LOG=/var/log/nextcloud.log
    # ^ where /var/log/nextcloud.log is the log specified in
    #   $NC_WEB/config/config.php
    if [ -f "$NC_LOG" ]; then
        if [ ! -f "$NC_LOG.1st" ]; then
            mv "$NC_LOG" "$NC_LOG.1st"
        else
            : > "$NC_LOG"
        fi
    else
        touch "$NC_LOG"
    fi
    chown www-data:www-data
    ```
  - visit the site using a browser or run:
    ```
    sudo -u www-data php $NC_WEB/index.php
    tail "$NC_LOG"
    ```

    (Ignore bool vs integer type errors related to IP address since that is merely a side effect from running index.php from a terminal instead of a browser.)
    - also try:
      ```
      tail "$NC_LOG" | grep Memcache
      ```
  - If you see:
    "Memcache \\OC\\Memcache\\Redis not available for local cache"
    then ensure that you have:
    - Run the 'php-set-version... $ver' before running this script again
      (where ... is the script matching your web server and distro)
    - reboot (even if you restart memcached, redis, and nginx and they say they are ok, you could still have to reboot!)
END
