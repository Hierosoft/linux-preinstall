# cron

## Logging
By default, all logging may be turned off.

To turn it on:
- In /etc/default/cron, to log standard messages, plus jobs with exit status != 0, set `EXTRA_OPTS='-L 5'`
- In /etc/rsyslog.conf (or /etc/syslog.conf in some cases), to separate the cron log from /var/log/messages, uncomment `cron.*                         /var/log/cron.log`
  - Note that cron is also mentioned in the catch-all section:

```
*.=debug;\
        auth,authpriv.none;\
        mail.none               -/var/log/debug
*.=info;*.=notice;*.=warn;\
        auth,authpriv.none;\
        cron,daemon.none;\
        mail.none               -/var/log/messages
```
- Before changing the log location, the log entries could be found like:
  - `sudo cat /var/log/messages | grep -v flatpak_policy | grep -v evince-thumbnailer | tail -n 200`
