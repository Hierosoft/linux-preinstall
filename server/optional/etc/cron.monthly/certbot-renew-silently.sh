#!/bin/sh
#certbot renew > /root/certbotrenew.monthly.lastrun.txt
# cron runs *ly scripts with runparts --report, so don't redirect output.
certbot renew
