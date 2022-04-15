# linux-preinstall
Put first-time setup in easy mode for GNU+Linux systems! Make the system ready to use from day one.

These scripts automatically install programs and configure settings many users expect, and inform you of any manual steps needed. I regularly update and use these scripts for myself and people I help. These scripts have been in development since 2016, but due to growth and specialization I've added them to git to make installation even easier (web install from git).

Install only the packages you want for the specific task (such as development, video, streaming, desktop publishing, etc), but don't miss any you need (These groups may be lighter or heavier than distro-specific groups defined in the repositories, but usually lighter and more comprehensive for creators of any sort. The project is moving toward using metadata and Python to avoid the overlap between different groups and reduce the size of each group).

Installing the linuxpreinstall python module also adds some useful commands:
- `findmime`: Find files by full/partial mimetype (such as "jpeg" or "image"!) in the current directory.
- `cleanif`: remove files from directory 1 if they exist in directory 2 (great for if you unzip or copy a load of files to the wrong place!)

## GOALS
* Make the GNU+Linux system ready to use from day one.
* Separate scripts by distro (Ubuntu, Fedora).
* Separate scripts by workflow (end user, developer, server).
* Move as many features to the python linuxpreinstall module as seems
  reasonable.
  - [ ] A major feature that would have to be ported is selecting the
    correct package name depending on the distro (See the bash-based [api.rc](api.rc) and the python-based
    [linuxpreinstall/package_names.csv](linuxpreinstall/package_names.csv) (WIP)).

## Design Choices
- Flatpaks are installed as root. In edge cases, that fixes small issues related to permissions and accessibility of binary paths, shortcuts, etc.
- The flatpak is preferred over another package usually, for the most up-to-date version, and one that can be updated in one command rather than many which is the case for AppImage. For help with AppImage "install" and "uninstall" including icons (trimmed to one command each!) See [nopackage](https://github.com/poikilos/nopackage).
- The "Overview" section describes more about how linux-preinstall is unique.

## Overview

In some cases, instructions for beginners are included. Scripts such as those listed below may be helpful for you if you are starting linux or starting someone else on linux:
- [Lubuntu - most essential tips only.md](Lubuntu%20-%20most%20essential%20tips%20only.md)
  - [GettingStarted-LXQt.md](GettingStarted-LXQt.md)

Where there may be things that are too simple to script but too obscure to memorize, various tutorials and/or examples are included, such as:
- [Always Install (any GNU+Linux System).md](Always%20Install%20(any%20GNU+Linux%20System).md)
- [AlwaysAdd/](AlwaysAdd)
- [AlwaysRemove/](AlwaysRemove)
- [MissingMimetypes/](MissingMimetypes)
- [drivers/Broadcom_B43_Wifi.ubuntu.sh](drivers/Broadcom_B43_Wifi.ubuntu.sh)
- [Camera.md](Camera.md)
- [game listings and stores, Linux.md](game%20listings%20and%20stores,%20Linux.md)
  - [Games for linux, semi-popular.md](Games%20for%20linux,%20semi-popular.md)
  - [games, casual from AUR.md](games,%20casual%20from%20AUR.md) (applies to Arch-based distros including Manjaro).
- [JNLP files, launching.md](JNLP%20files,%20launching.md)
- [centos kiosk with screensaver picture list sync from windows via samba](samba-examples/centos-kiosk/)
- [TV Tuners, analog.md](TV%20Tuners,%20analog.md)
- [tar.md](tar.md)
- [forensic imaging tools.md](forensic%20imaging%20tools.md)
  - See also [rotocanvas](https://github.com/poikilos/rotocanvas) (visual diff and algorithmic (non-ai) similarity search).
- [macOS](macOS)

WIP (Work in progress) documents:
- [Music.md](Music.md)
- [Fedora tips - with notes on 26.md](Fedora%20tips%20-%20with%20notes%20on%2026.md)
- [troubleshooting-developer/](troubleshooting-developer/)
- [Word or Writer image extraction via unzip and emf conversion.md](Word%20or%20Writer%20image%20extraction%20via%20unzip%20and%20emf%20conversion.md)
- [doc](doc): Additional and WIP documentation for linux-preinstall or programs with which linux-preinstall assists.
- [projects](projects): This generally contains project files content that becomes part of linux-preinstall (not necessarily WIP, but may have previous WIP versions as separate files or layers).

## IT
This section explains scripts and usage of this repo that is specific to IT work (fixing computers and networks usually typifies the Information Technology field).

There are some parts of linux-preinstall that are in current use for computer clients:
- One use for the documents such as ones above is that you can place a link to them on a person's desktop, and then update them with git automatically such as a cron job running git pull as that user (`cd /home/user/git/linux-preinstall && sudo -u user git pull # where user is the username`).
- The "expertmultimedia-managed" folder is only for setting up computers to "phone home" (provide self-identification and an IP address for remoting) to Expert Multimedia, and isn't for general use.

## Scripts
Beyond tutorials and examples, there are many scripts.

The most frequent type of script included is one that installs a program that is hard to install or installs a list of programs related to a specific type of user or workflow. This is more effective than `tasksel` (for Debian/Ubuntu) or `groupinstall` (for RedHat/Fedora) because the programs and groups here are recommendations not merely a full list that may leave you unsure of what will work well, or a list that is only for a fixed role of a computer rather than a circumstantially elected or self-selected role of a person. In the case of the server folder here, that is a computer role, but that is mostly an exception and applies to webmasters. It is also more fine-grained than an "x server" group in group systems (where "x" is LAMP [Linux-Apache-MySQL-PHP] or something like that) in that each of this repo's scripts handles installation for a specific workflow and not more.

In other words, the selections are "opinionated": The individual software packages are scripted here because they are recommended based on effectiveness, fit, and whether software is maintained well. The result is that you get programs you may not know existed but may be the best for what you are doing. The software packages are grouped by script, by folder, or scripted individually are each included based on recommendation, rather than on the best (or selected as default based on opinion) of what one particular distro has to offer. The recommended packages are installed by any means necessary: install necessary repos and/or PPAs, or use flatpaks or AppImages.

The lists are more comprehensive and/or have more updated versions in some cases as well (including ones significantly more up-to-date on flathub or as an AppImage or only available via flathub or AppImage).

This project recommends installing certain programs as flatpaks, AppImages or unpackaged binary distributions. In Debian-based distros, such versions are especially useful if you want only versions of system packages vetted according to their philosophy but want cutting-edge versions of desktop applications. Even beyond those distros, some of these programs are maintained well (perhaps better than you think if you only look at releases) but don't provide distro-specific packages often (or the distro doesn't accept or vet them). See the lists of programs currently recommended to be obtained by special means:
- [Flatpaks.list](Flatpaks.list) (maintained on developer's computer via `cd projects && flatpak list --app | cut -f1 > Flatpaks.list`)
  - except ignore those in [projects/Flatpak-only_for_testing.list](projects/Flatpak-only_for_testing.list).
  - or see projects/Flatpaks-all.md but ignore those also in that list or in [projects/Flatpak-runtimes.list](projects/Flatpak-runtimes.list) (Runtime packages are automatically installed as dependencies for the installed apps). NOTE: There is at least one that has an asterisk since each version has a different package name (The version number is in the package name). The list was made manually by comparing Flatpaks.list to projects/Flatpaks-all.list.
  - Flatpaks can be installed system-wide with sudo then automatically updated in one shot via `sudo flatpak update`!
- [AppImages.list](AppImages.list): This list is manually maintained such as by comparing it to the result of `ls ~/.local/lib64/ | grep mage` (those installed using [nopackage](https://github.com/poikilos/nopackage); only old versions would be somewhere like `ls ~/Downloads/1.InstallManually | grep mage`) on the developer's computer.
- [Unpackaged.list](Unpackaged.list) (generated manually on the developer's computer such as by comparing it to `ls ~/.local/lib64/ | grep -v mage` and `ls ~/.local/lib`)
  - Unpackaged versions of Blender are available via Poikilos' [blendernightly](https://github.com/poikilos/blendernightly) project.
  - Some of these programs are recommended to be built from source. In such cases, usually a scripts to build the software from source (or a document describing how) is in the linux-preinstall project.
  - Some applications are in zip/gz/etc. binary distributions and have install scripts in this project historically (predating the nopackage project), but in such cases instead use [nopackage](https://github.com/poikilos/nopackage) to install the software and report any errors at the Issues section on that repository.
  - world_clock is available via Poikilos' [world_clock](https://github.com/poikilos/world_clock) repo.
  - bfg is a tool for stripping old data from git repos to save space and increase the speed of many operations done over the internet.
  - Ulauncher is an application launcher with a fast and comprehensive search feature.
  - Umlet is a UML diagram creation tool.

The lists and individual program install scripts make programs in linux-preinstall generally easier to install.

Install scripts are categorized by a person's role and/or workflow, and specified by OS when necessary (if a distro is not not specified in the filename [deb means Debian/Ubuntu/variants], the script attempts to adapt to all popular distros), such as:
- [everyone](everyone)
- [drivers](drivers)
- [developer](developer)
- [educational](educational)
- [migration](migration)

Additional scripts (scripts that do things rather than install things) are for IT and developer use, but may serve other people as well:
- [utilities](utilities)
- [utilities-developer](utilities-developer)

After installing scripts, post-install instructions are often appended to PostInstallInstructions.md.

See also:
- expertmultimedia-managed in the "IT" section.

If there is a program that is not available in a repo and not available on here, it may yet be within one of the scripts (suchas developer/developer.fedora.sh). If not, it may be on flathub even if not in any install script in this repo. Otherwise, if only an AppImage, zipped build, or single binary is available, you can usually use [nopackage](https://github.com/poikilos/nopackage) to install it (and an icon!) in one shot.




## Developer Tools
There are various useful tools for developers in the developer folder, including:
- An improved fork of a geany-openscad highlighter.

## Server Tools
- ./server/optional/php-set-version.apache.ubuntu.sh or ./server/optional/php-set-version.nginx.deb.sh: Choose a specific version of php as the system's php and get all of the matching dependencies such as for WordPress, and uninstall all other versions and their packages.


## Related Projects
Related projects
- [nopackage](https://github.com/poikilos/nopackage): Install any AppImage, archive, deb, or binary as an icon (download icons automatically when known!) on any GNU+Linux system!
  - formerly the linux-preinstall tool called install_any.py
- [rotocanvas](https://github.com/poikilos/rotocanvas): has several useful commands related to image sequences including (browseable) image "playlists".
- [TemperatureSanitizer](https://github.com/poikilos/TemperatureSanitizer): See also TEMPerV1 verbose output files (files named with -vvv) for technical info.


## Usage
Open terminal, then cd to the repo directory. If you don't have it yet,
run the following to install/update from the web:
```
cd ~
if [ ! -d git ]; then mkdir Downloads; fi
cd git
if [ ! -d linux-preinstall ]; then
  git clone https://github.com/poikilos/linux-preinstall.git
  cd linux-preinstall
else
  cd linux-preinstall
  git pull
fi

echo "Installing `pwd`..."
python3 -m pip install --user `pwd`
```
For best results, the following usage order is recommended. All scripts
except `*-nonroot.sh` scripts must run as `root` (or with `sudo bash`):
* distro-specific folders (such as everyone-fedora)
* universal folders that are not distro-specific (such as everyone)
* nonroot scripts (run as regular user without sudo, though some of the
  scripts call sudo but change settings for the current user).

Folders named "unused" are not recommended, and there may be a better
option. For example, VirtualBox is not recommended, and qemu install
scripts are provided instead.

Script names:
- If the name includes .debian.*, then it is known to work on Debian and may work on Ubuntu.
- If the name includes .ubuntu.*, then it is known to work on Ubuntu and probably will not work on Debian.
- If the name includes .deb.*, then it may work on both Debian and Ubuntu.
- If the name includes .fedora.*, then it will work on Fedora but may not work on other rpm distros.

### Modular Features

#### sortversion
The linuxpreinstall.versioning module helps identify version strings
inside of names. A "." will only be included as part of the version if
a number follows. Otherwise it will end the version, since it would
seem to be the start of a file extension in that case. The usual use of
it is using the utilities/sortversion command such as via:
```bash
ls | sortversion
```

To use the `sortversion` command in the utilities folder you must
either have the linuxpreinstall module in your path or install
`sortversion` as a symlink such as via (replace
`/home/user/git/linux-preinstall` or `~/git/linux-preinstall` with the
location of your cloned linux-preinstall repo in the following
commands!):
```
echo "If you copied and pasted this without changing it, don't expect it to work--You failed to follow the documentation."
sudo ln -s /home/user/git/linux-preinstall/utilities/sortversion /usr/local/bin/
# or:
# ln -s ~/git/linux-preinstall/utilities/sortversion ~/.local/bin/
# if that is in your user PATH. It can be added to your path in ~/.bash_profile (or whatever file is appropriate for your os) like:
# PATH=$PATH:$HOME/.local/bin:$HOME/bin
# # ^ before the "export PATH" line, otherwise add that afterward.
```

#### nopackage
The old install_any.py script's features have been moved to
<https://github.com/poikilos/nopackage> which provides the new command
`nopackage`:

You can use `nopackage` to install almost anything, such as a single file (AppImage or other), a zip file, or to install a deb package on any distro in your profile, all without superuser priveleges!

## Changelog
See [changelog.md](changelog.md)

## References
See [References.md](References.md)
