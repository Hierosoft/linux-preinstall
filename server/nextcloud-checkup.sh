#!/bin/bash
cat <<END
You must manually type:

 sudo crontab -e"

Then enter/paste:

*/5  *  *  *  * sudo -u www-data php -f /var/www/nextcloud/cron.php > /var/log/cron--var-spool-cron-crontabs-root--nextcloud.log 2>&1
# or:
# */5  *  *  *  * date > /var/log/cron--var-spool-cron-crontabs-root--nextcloud.log && sudo -u www-data php -f /var/www/nextcloud/cron.php >> /var/log/cron--var-spool-cron-crontabs-root--nextcloud.log 2>&1

or whatever is the correct web server user.
for docker use something like:
*/5  *  *  *  * docker exec -i nextcloud sudo -u www-data php -f /config/www/nextcloud/cron.php

as per <https://discourse.linuxserver.io/t/getting-cron-working-in-nextcloud/4254/3>.

The "crontab -e" command will edit:
/var/spool/cron/crontabs/root


Remember to exclude the following Scribus patterns:
.*\_autosave_.*\.sla
.*\_autosave_.*\.sla\..*

Remember to exclude the following Scribus (old version) patterns:
.*\.sla.autosave
.*\.autosave

If you didn't do it before, clean up the trashbin using wildcards using webdav
(See <https://docs.nextcloud.com/server/latest/developer_manual/client_apis/WebDAV/trashbin.html>):
See my (Poikilos') project called nextcloudops.


Fixes for issues in Nextcloud admin overview are numbered below:

1. Fix "getenv("PATH")" returns blank

As per <https://help.nextcloud.com/t/problem-with-environmental-variables/8765>:
copy:

env[HOSTNAME] = $HOSTNAME
# env[PATH] = $PATH
# such as:
env[PATH] = /usr/local/bin:/usr/bin:/bin
# :/home/redacted/.local/bin
# ^ exclude user-specific stuff
# :/home/redacted/.rvm/bin
# ^ rvm is ruby (excluded since not necessary for Nextcloud nor can the www-data user access redacted's home directory)
env[TMP] = /tmp
env[TMPDIR] = /tmp
env[TEMP] = /tmp

to the conf used by nextcloud
such as via:
sudo nano /etc/php/7.3/fpm/pool.d/www.conf
- commented by default, so just uncomment the lines.
Then:
    sudo systemctl restart php7.3-fpm

2. The PHP memory limit is below the recommended value of 512MB.

sudo nano /etc/php/7.3/fpm/pool.d/www.conf
Change the variable below to:
    php_admin_value[memory_limit] = 512M
Then:
    sudo systemctl restart php7.3-fpm


3. The "Strict-Transport-Security" HTTP header is not set to at least "15552000" seconds. For enhanced security, it is recommended to enable HSTS as described in the security tips ↗.

Apache: See https://docs.nextcloud.com/server/19/admin_manual/installation/harden_server.html
<VirtualHost *:443>
  ServerName cloud.nextcloud.com
    <IfModule mod_headers.c>
      Header always set Strict-Transport-Security "max-age=15552000; includeSubDomains"
    </IfModule>
 </VirtualHost>

NGINX:
See https://www.nginx.com/blog/http-strict-transport-security-hsts-and-nginx/
Add the following to server & location /nextcloud (since it adds a new header according to the article above)
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

4. recommended packages are not installec
apt --fix-broken install
sudo apt install -y php7.3-bcmath php7.3-gmp

END
