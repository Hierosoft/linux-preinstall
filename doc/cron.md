# cron

## Logging
By default, all logging may be turned off.

To turn it on:
- To log standard messages, plus jobs with exit status != 0: In /etc/default/cron, set `EXTRA_OPTS='-L 5'`
- To separate the cron log from /var/log/messages: In /etc/rsyslog.conf (or /etc/syslog.conf in some cases), uncomment `cron.*                         /var/log/cron.log`
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

## Troubleshooting
### No MTA installed
If the log says "No MTA installed, discarding output" after a failed command, try the following:
Install the postfix package, then as per <https://askubuntu.com/a/199453> (as your Thundbird user, not root), run:
- `echo "$USER@localhost" | sudo tee -a /root/.forward`
- `sudo adduser $USER mail`
