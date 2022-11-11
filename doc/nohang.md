# nohang

I recommend nohang for everyone. It provides a low memory warning with
an option or eventual requirement to terminate large processes.
Something similar is built into Windows. I consider nohang or something
like it a necessity for using a computer for any sort of work, or in
general, anything you don't want to lose (the same rule of thumb that
applies to backup frequency). The nohang package is available on several distros and more
information is at the [nohang repo](https://github.com/hakavlad/nohang).

Running nohang seemed to fix my problems in Xfce and GNOME 3 (GNOME 40
or so). However, that isn't very comforting since maybe if I don't
click "yes" to terminate processes or in other situations maybe Xfce
and GNOME would still hang. This happened to me several times while
doing work for college (2020 on Fedora and Debian 10 (buster)) and I
kept losing work. I had to watch YouTube videos for college and have
many tabs open for research, plus my personal tabs. I like many tabs and
that caused me problems with 16GB of RAM especially with other programs
open (even with Marvellous Suspender which replaces
[malware-compromised The Great Suspender](https://thehackernews.com/2021/02/warning-hugely-popular-great-suspender.html#:~:text=WARNING%20%E2%80%94%20Hugely%20Popular%20'The%20Great%20Suspender'%20Chrome%20Extension%20Contains%20Malware,-%EE%A0%82February%2006&text=Google%20on%20Thursday%20removed%20The,deactivating%20it%20from%20users'%20computers.)).
Though I save frequently in *most* cases, it is never good to lose work
and I recommend [nohang](nohang.md) to everyone regardless of their DE.
I used KDE then LXQt for more speed to successfully to finish college
well. I was able to get out of low memory situations in KDE by closing
programs when the computer became slow.


## High Memory Use in General
The only significant crashing problem I've had with Linux (usually
solved by nohang), perhaps the only one other than performing kernel
updates without restarting, is using software with high memory usage.
This shouldn't be a problem with 16GB, but with much exasperation, I've
experienced that it is.

GNOME has placed a priority on it and as of 2019 or so made a big push
to identify memory leaks. However, I still have had ups and downs since
the supposed fix of
"[The Infamous GNOME Shell Memory Leak](https://feaneron.com/2018/04/20/the-infamous-gnome-shell-memory-leak/)"
of 2018. Also, GNOME itself has an off-putting approach to development:
The remove any features users want to change or fix, then people become
dependent on add-ons, but then the add-on API changes and the add-ons
become unusable (See also:
[GNOME is Deeply Flawed](https://poikilos.org/2021/04/21/gnome-is-deeply-flawed/)).
See also the discussion simply entitled:
"[The GNOME developers removed it](https://news.ycombinator.com/item?id=5729627)"
(askubuntu.com) written in 2013--The issue was already well-known back then.

MATE seems like the only reasonable option for me since I can add certain
[tweaks to modernize the interface](MATE).

Using another popular desktop environment (DE) either has one or the
other extreme: So minimalistic as to be clunky (remedied in
[MATE](MATE) article), or so large as to try to do everything and
majors on the minors which usually results in the flaws below.

My experiences with bloated desktops ended with GNOME 3 (above) and
KDE. Eventually I switched to LXQt to avoid KDE's dreaded Baloo. Baloo
is a file indexing daemon with high memory usage (eventually reaching
multiple GB), removal takes too many apps with it. Even basic
components of Plasma may require Baloo, so switching from Dolphin may
not be enough--This dependency on such a bloated daemon is
unacceptable. All methods available online for disabling or taming
Baloo failed for me.

My experiences with bloated distros ended with Fedora: I eventually
switched from Fedora to Devuan + [MATE plus some tweaks](MATE) to avoid
the dreaded pkgkit. Debian or Ubuntu may be reasonable choices but lack
[init freedom](https://www.devuan.org/os/init-freedom). The pkgkit
application basically cannot be removed nor tamed (methods online
didn't work for me) since package management itself depends upon it. It
has high memory usage (eventually reaching multiple GB). The bug
https://bugzilla.redhat.com/show_bug.cgi?id=2075598
(https://bugzilla.redhat.com/show_bug.cgi?id=2082251 closed as
duplicate) gets auto-closed on each Fedora release but they never fix
it! RedHat's policy of closing all issue with each Fedora release is
dodgy.


## Install
I recommend using the packaged version on Devuan 4 (See [From source](#from-source)).
- If using sysvinit (Devuan 4 also has the option of runit or OpenRC) it runs from:
  - /etc/init.d/nohang
- Ensure you are running sysvinit :
  - `pidof /sbin/init && echo "sysvinit" || echo "other"`

### From source
It never seems to run on Devuan 4 (chimaera) (based on Debian 11 (bullseye)).
