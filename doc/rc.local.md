# rc.local

If you do not want systemd, consider [Devuan](devuan).

> As [I said about CentOS 7](https://unix.stackexchange.com/a/247543/5132) and [about Debian 8](https://unix.stackexchange.com/a/333003/5132) and [about Ubuntu 15](https://unix.stackexchange.com/a/202743/5132):
>
> You're using a systemd+Linux operating system. `/etc/rc.local` is a double backwards compatibility mechanism in systemd, because it is a backwards compatibility mechanism for a mechanism that was itself a compatibility mechanism in the van Smoorenburg System 5 `rc` clone.
>
> Using `/etc/rc.local` can go horribly wrong. People have been surprised by the fact that systemd doesn't run `rc.local` in quite the same way, in quite the same place in the bootstrap, as they are used to. (Or erroneously expect: It did not, in fact, run _last_ in the old system, as the OpenBSD manual still points out.) Others have been surprised by the fact that what they set up in `rc.local` expecting the old ways of doing things, is then completely undone by the likes of new `udev` rules, NetworkManager, `systemd-logind`, `systemd-resolved`, or various "Kit"s.
>
> As exemplified by "https://unix.stackexchange.com/questions/389289/", some operating systems already provide systemd _without_ the backwards compatibility features [such as the `systemd-rc-local-generator` generator](https://github.com/systemd/systemd/blob/044c2c7a2b322b6561d7e3cc5a48a548fee887f9/meson.build#L1912). [Whilst Debian still retains the backwards compatibility features](https://sources.debian.org/src/systemd/239-10/debian/rules/#L48), [Arch Linux builds systemd with them turned off](https://git.archlinux.org/svntogit/packages.git/tree/trunk/PKGBUILD?h=packages/systemd#n133). So on Arch and operating systems like it expect `/etc/rc.local` _to be entirely ignored_.
>
> Forget about `rc.local`. It's not the way to go. You have a systemd+Linux operating system. So make a proper systemd service unit, and don't begin from a point that is two levels of backwards compatibility away. (On Ubuntu and Fedora, it is _three_ times removed, the van Smoorenburg System 5 `rc` clone that followed `rc.local` having then been _itself twice_ superseded, over a decade ago, first by upstart and then by systemd.)
>
> Also remember [the first rule for migrating to systemd](https://jdebp.uk/FGA/systemd-house-of-horror/daemonize.html#first-rule).
>
> This is not even a new idea that is specific to systemd. On van Smoorenburg `rc` and Upstart systems, the thing to do was to make a proper van Smoorenburg `rc` script or Upstart job file rather than use `rc.local`. Even FreeBSD's manual notes that nowadays one creates a proper Mewburn `rc` script instead of using `/etc/rc.local`. Mewburn `rc` was introduced by NetBSD 1.5 in 2000.
>
> `/etc/rc.local` dates from the time of Seventh Edition Unix and before. It was superseded by `/etc/inittab` and a runlevel-based `rc` in AT&T Unix System 3 (with a slightly different `/etc/inittab` in AT&T Unix System 5) **in 1983**. Even _that_ is now history.
>
> Create proper native service definitions for your service management system, whether that be a service bundle for the nosh toolset's `service-manager` and `system-control`, an `/etc/rc.d/` script for Mewburn `rc`, a service unit file for systemd, a job file for Upstart, a service directory for runit/s6/daemontools-encore, or even an `/etc/init.d/` script for van Smoorenburg `rc`.
>
> In systemd, such administrator-added service unit files go in `/etc/systemd/system/` usually (or `/usr/local/lib/systemd/system/` rarely). With the nosh service manager, `/var/local/sv/` is a conventional place for local service bundles. Mewburn `rc` on FreeBSD uses `/usr/local/etc/rc.d/`. _Packaged_ service unit files and service bundles, if you are making them, go in different places, though.
> # Further reading
>
> - Lennart Poettering et al. (2014). [_systemd-rc-local-generator_](http://www.freedesktop.org/software/systemd/man/systemd-rc-local-generator.html). systemd manual pages. Freedesktop.org.
> - [`rc.local`](https://www.freebsd.org/cgi/man.cgi?query=rc.local&manpath=FreeBSD+11.2-RELEASE+and+Ports). _FreeBSD System Manager's Manual_. 2016-04-23.
> - [https://unix.stackexchange.com/a/233581/5132](https://unix.stackexchange.com/a/233581/5132)
> - Lennart Poettering (2011-08-29). _[Plese remove `/etc/rc.local` or `chmod -x` it](https://bugzilla.redhat.com/show_bug.cgi?id=734268)_. Redhat bug #734268.
> - [https://unix.stackexchange.com/a/211927/5132](https://unix.stackexchange.com/a/211927/5132)
> - Dirk Schmitt (2017-12-19). _[`rc.local` is starting to early](https://github.com/systemd/systemd/issues/7703)_. systemd bug #7703
> - [https://wiki.archlinux.org/index.php?title=Systemd&diff=378926&oldid=378924](https://wiki.archlinux.org/index.php?title=Systemd&diff=378926&oldid=378924)
> - Benjamin Cane (2011-12-30). _[When it's Ok and Not Ok to use `rc.local`](https://bencane.com/2011/12/30/when-its-ok-and-not-ok-to-use-rc-local/)_. bencane.com.
> - [https://unix.stackexchange.com/a/49636/5132](https://unix.stackexchange.com/a/49636/5132)
> - Lennart Poettering (2010-10-01). _[How Do I Convert A SysV Init Script Into A systemd Service File?](http://0pointer.de/blog/projects/systemd-for-admins-3.html)_. 0pointer.de.
> - [https://askubuntu.com/questions/523369/](https://askubuntu.com/questions/523369/)
> - Jonathan de Boyne Pollard (2015). [_`/etc/inittab` is a thing of the past._](https://jdebp.uk/FGA/inittab-is-history.html). Frequently Given Answers.
> - Jonathan de Boyne Pollard (2014). [_A side-by-side look at run scripts and service units._](https://jdebp.uk/FGA/run-scripts-and-service-units-side-by-side.html). Frequently Given Answers.
> - Jonathan de Boyne Pollard (2014). _[A real-world worked example of setting up and running a service with nosh](https://jdebp.uk/Softwares/nosh/worked-example.html)_. Softwares.
> - Jonathan de Boyne Pollard (2016). "[Missing system search paths from the `systemd.unit` manual page](https://jdebp.uk/FGA/systemd-documentation-errata.html#MissingUsrLocalLibSystemd)". _Errata for systemd doco_. Frequently Given Answers.

-JdeBP [answered Sep 27, 2018 at 16:06](https://unix.stackexchange.com/a/471871/343286), Stephen Kitt edited Jan 19 at 9:26 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)


## Debian 10


## Debian 11
### Deprecates rc.local

#### Workaround
This workaround is not for Devuan Chimera (based on Debian 10 Buster). It has a device called /etc/systemd/system/rc.local.service to emulate rc.local from a systemd perspective but does not have systemd.

A workaround is at [Home / Sysadmin / rc.local deprecated](https://mox.sh/sysadmin/rc-local-deprecated/) by mox.
- Make a systemd script to emulate rc.local (change "Wants" and "After" depending on what your script does! This one was modified to require networking which is probably good enough for most people.):
```
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/local/bin/rc.local

[Install]
WantedBy=multi-user.target

[Unit]
Wants=bluetooth.service
After=bluetooth.service
```
- Enable it: `systemctl enable local-starttasks.service`
