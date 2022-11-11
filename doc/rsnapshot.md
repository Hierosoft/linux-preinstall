# rsnapshot

rsnapshot is a PERL application allowing using rsync for incremental backups.
Hardlinks allow each backup snapshot to appear complete but take up little space.

It can be installed using the distro's package manager usually.

Running rsnapshot **after** changing the conf file is typically simple: `rsnapshot alpha`.
- The "alpha" snapshot set is the most frequent.

It can be configured by editing /etc/rsnapshot.conf.
- Typically Poikilos machines or scripts copy the conf to a file such as: `/opt/rsnapshot.conf`
  - In that case it would instead be run like: `rsnapshot alpha -c /opt/rsnapshot.conf`

It is typically run using a cron job. The package installs a cron script with only comments: `/etc/cron.d/rsnapshot`
- Typically Poikilos machines or scripts copy the cron job to a file such as: `/etc/cron.d/rsnapshot-$(hostname)`
- Normally you could just uncomment alpha, beta, and gamma snapshot lines in the conf (delta is commented in the conf file by default).
  - **and** set the destination and other options.

The "before" script could be (or could run) `linux-preinstall/utilities/generate_exclude.py`. The script:
- could be symlinked by setting `LINUX_PREINSTALL` to the correct location of linux-preinstall then running: `cd /opt && sudo ln -s $LINUX_PREINSTALL/utilities/generate_exclude.py`
- generates `/opt/exclude_from_backup-absolute-generated.txt` from `$USERPROFILE/exclude_from_backup.txt` by prepending `/home/*/` to each line that doesn't start with `/home`
  - Then the rsnapshot.conf can set `exclude_file	/opt/rsnapshot/exclude_from_backup-absolute-generated.txt`
  - For further documentation see the docstring (long block comment at the top) of [../utilities/generate_exclude.py](../utilities/generate_exclude.py).

To know whether it ran, first ensure logging is enabled for cron. See [cron.md](cron.md).
- Also check that log for errors following the rsnapshot line.
