# MongoDB
Below is my solution to ["MongoDB not working. "ERROR: dbpath (/data/db) does not exist."](https://stackoverflow.com/questions/24599119/mongodb-not-working-error-dbpath-data-db-does-not-exist)

Daemons (usually ending with d) are normally started as services. Starting the service (daemon) will allow mongodb to work as designed (without permission changes if integrates well with your distro). I start it using the service named mongodb instead of starting mongod directly--on distro with systemd enable on startup then run like:
```
sudo systemctl enable mongodb
sudo systemctl start mongodb
```

or, on distro with upstart (if you have /etc/init) or init (if you have /etc/init.d) ( https://www.tecmint.com/systemd-replaces-init-in-linux/ ) instead run:
```
sudo service mongodb enable
sudo service mongodb start
```

If you have a distro with rc ("run commands") such as Gentoo (settings in /etc/init.d) (https://forums.gentoo.org/viewtopic-t-854138-start-0.html) run:
```
rc-update add mongodb default
/etc/init.d/mongodb start
```

In a distro/version of FreeBSD which still has rc (check whether your version switched to systemd, otherwise see below):

- add the following line to /etc/rc.conf:
```
mongod_enable="YES"
```

- then:
```
sudo service mongod start
```


After starting the service, an unpriveleged user can use mongo, and each user will have separate data.

edited Apr 20, 2018 at 19:53
answered Sep 8, 2017 at 14:49
￼

See also:
- [daemons](daemons.md)
