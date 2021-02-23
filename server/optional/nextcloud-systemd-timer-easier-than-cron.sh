#!/bin/sh
customExit() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
if [ -z "$nextcloudDirName" ]; then
    if [ -z "$1" ]; then
        echo "You must specify an existing nextcloud directory name such as nextcloud (or owncloud if you migrated from owncloud)."
        exit 1
    else
        nextcloudDirName="$1"
    fi
fi
src=""
if [ -d /var/www/$nextcloudDirName ]; then
    src="etc/systemd/system/nextcloudcron (in var www $nextcloudDirName).service"
    if [ -d /var/www/nextcloud ]; then
	cat <<END
WARNING: You also have /var/www/nextcloud but it will be ignored. After
this script runs, make sure that
/etc/systemd/system/nextcloudcron.service
refers to the instance you are actually hosting.

END
    if [ -f /etc/apache2/sites-enabled/$nextcloudDirName.conf ]; then
        echo "See below (/etc/apache2/sites-enabled/$nextcloudDirName.conf):"
        cat /etc/apache2/sites-enabled/$nextcloudDirName.conf
    elif [ -f /etc/apache2/sites-enabled/nextcloud.conf ]; then
        echo "See below (/etc/apache2/sites-enabled/nextcloud.conf):"
        cat /etc/apache2/sites-enabled/nextcloud.conf
    else
        cat <<END
You don't have any /etc/apache2/sites-enabled/$nextcloudDirName.conf
nor a /etc/apache2/sites-enabled/nextcloud.conf,
so you'll have to look deeper in your apache configuration to see
exactly how or if you are hosting nextcloud (so you know which folder
to put in /etc/systemd/system/nextcloudcron.service)

END
    fi
elif [ -d /var/www/nextcloud ]; then
    src="etc/systemd/system/nextcloudcron.service"
else
    customExit "You don't have nextcloud in /var/www/$nextcloudDirName nor /var/www/nextcloud"
fi

cp "$src" /etc/systemd/system/nextcloudcron.service
cp "etc/systemd/system/nextcloudcron.timer" /etc/systemd/system/nextcloudcron.timer
systemctl start nextcloudcron.timer
systemctl enable nextcloudcron.timer
echo "Remember to set Nextcloud settings to 'Cron' (if set to AJAX,"
echo "  Nextcloud would still manually run jobs during every page load)"
# systemctl list-timers --all
# systemctl status nextcloudcron
