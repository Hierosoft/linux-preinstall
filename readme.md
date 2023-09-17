# linux-preinstall
Put first-time setup in easy mode for GNU+Linux systems! Make the system ready to use from day one.

These scripts automatically install programs and configure settings many users expect, and inform you of any manual steps needed. I regularly update and use these scripts for myself and people I help. These scripts have been in development since 2016, but due to growth and specialization I've added them to git to make installation even easier (web install from git).

Install only the packages you want for the specific task (such as development, video, streaming, desktop publishing, etc), but don't miss any you need (These groups may be lighter or heavier than distro-specific groups defined in the repositories, but usually lighter and more comprehensive for creators of any sort. The project is moving toward using metadata and Python to avoid the overlap between different groups and reduce the size of each group).

Installing the linuxpreinstall python module also adds some useful commands (See the "[Modular Features](#modular-features)" section).

## GOALS
* Make the GNU+Linux system ready to use from day one.
* Separate scripts by distro (Ubuntu, Fedora).
* Separate scripts by workflow (end user, developer, server).
* Move as many features to the python linuxpreinstall module as seems
  reasonable.
  - [ ] A major feature that would have to be ported is selecting the
    correct package name depending on the distro (See the bash-based [api.rc](api.rc) and the python-based
    [linuxpreinstall/static/package_names.csv](linuxpreinstall/static/package_names.csv) (WIP)).

## Design Choices
- Flatpaks are installed as root. In edge cases, that fixes small issues related to permissions and accessibility of binary paths, shortcuts, etc.
- The flatpak is preferred over another package usually, for the most up-to-date version, and one that can be updated in one command rather than many which is the case for AppImage. For help with AppImage "install" and "uninstall" including icons (trimmed to one command each!) See [nopackage](https://github.com/poikilos/nopackage).
- The "[Overview](#overview)" section describes more about how linux-preinstall is unique.


## Install
Open terminal, then cd to the repo directory. If you don't have it yet,
run the following to install/update from the web:
```
cd ~
if [ ! -d git ]; then mkdir git; fi
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

## Overview
There are some things that are for everyone that Linux distros don't provide for various reasons such as:
- The package isn't well-maintained but works fine.
- There is no packaged version for the distro's package manager (There is no RPM or deb, or at least one not submitted to the distro nor upstream distro's repo if any). In other words, the maintainer of the project doesn't compile such a package and there is no separate package maintainer (That's where you can help if you learn how!).

Linux Preinstall aims to solve that.

[doc](doc) contains Additional and WIP documentation for linux-preinstall or programs with which linux-preinstall assists.

Where there may be things that are too simple to script (one line or requires clicks) but too obscure to memorize, various tutorials and/or examples are included, such as:
- [Always Install](doc/always_install.md) (any GNU+Linux System)
- [AlwaysAdd/](AlwaysAdd)
- [AlwaysRemove/](AlwaysRemove)
  - See also [keyring](doc/keyring.md) for help with annoying keyring popups, though a keyring generally is required and not automatic except in KDE for some reason :(
- [MissingMimetypes/](MissingMimetypes)
- [drivers/Broadcom_B43_Wifi.ubuntu.sh](drivers/Broadcom_B43_Wifi.ubuntu.sh)
- [JNLP format.md](doc/JNLP_format.md)
- [centos kiosk with screensaver picture list sync from windows via samba](samba-examples/centos-kiosk/)
- [TV Tuners](doc/TV_tuners.md) (analog)
- [tar.md](tar.md)
- [list of forensic_imaging_tools.md](doc/list_of_forensic_imaging_tools.md)
  - See also [rotocanvas](https://github.com/poikilos/rotocanvas) (visual diff and algorithmic (non-ai) similarity search).
- [macOS](macOS)

In some cases, instructions for beginners are included. Scripts such as those listed below may be helpful for you if you are starting linux or starting someone else on linux:
- [camera essentials](doc/camera-essentials.md)
- [Fedora Linux](doc/Fedora_Linux.md) (formerly "Fedora tips - with notes on 26.md")
- [list of linux games](doc/list_of_linux_games.md) (formerly Games for linux, semi-popular; game listings and stores, Linux; and games, casual from AUR (applies to Arch-based distros including Manjaro))
- [Lubuntu essentials](doc/Lubuntu-essentials.md)
- [LXQt essentials](doc/LXQt-essentials.md)
- [music essentials](doc/music-essentials.md)
- ..and any other files that may be named with "essentials" in [doc](doc)

WIP (Work in progress) documents:
- [troubleshooting-developer/](troubleshooting-developer/)
- [doc/developer/document_etl.md](doc/developer/document_etl.md) (Word or Writer image extraction via unzip and emf conversion)
- [projects](projects): This generally contains project files content that becomes part of linux-preinstall (not necessarily WIP, but may have previous WIP versions as separate files or layers).


## IT
This section explains scripts and usage of this repo that is specific to IT work (fixing computers and networks usually typifies the Information Technology field).

There are some parts of linux-preinstall that are in current use for computer clients:
- One use for the documents such as ones above is that you can place a link to them on a person's desktop, and then update them with git automatically such as a cron job running git pull as that user (`cd /home/user/git/linux-preinstall && sudo -u user git pull # where user is the username`).
- The "expertmultimedia-managed" folder is only for setting up computers to "phone home" (provide self-identification and an IP address for remoting) to Expert Multimedia, and isn't for general use.


## Scripts
Beyond tutorials and examples, linux-preinstall includes many usable (See disclaimer in [license](license.txt)) scripts.

The following long subsections describe each category of scripts.

### Software and Software Group Installation
The most frequent type of script included is one that installs a program that is hard to install or installs a list of programs related to a specific type of user or workflow. This is more effective than `tasksel` (for Debian/Ubuntu) or `groupinstall` (for RedHat/Fedora) because the programs and groups here are recommendations not merely a full list that may leave you unsure of what will work well, or a list that is only for a fixed role of a computer rather than a circumstantially elected or self-selected role of a person. In the case of the server folder here, that is a computer role, but that is mostly an exception and applies to webmasters. It is also more fine-grained than an "x server" group in group systems (where "x" is LAMP [Linux-Apache-MySQL-PHP] or something like that) in that each of this repo's scripts handles installation for a specific workflow and not more.

In other words, the selections are "opinionated": The individual software packages are scripted here because they are recommended based on effectiveness, fit, and whether software is maintained well. The result is that you get programs you may not know existed but may be the best for what you are doing. The software packages are grouped by script, by folder, or scripted individually are each included based on recommendation, rather than on the best (or selected as default based on opinion) of what one particular distro has to offer. The recommended packages are installed by any means necessary: install necessary repos and/or PPAs, or use flatpaks, AppImages, or downloaded binary archives. Other advantages of using any means necessary are that lists are more comprehensive and/or have more updated versions (than on repos) in many cases.

This project recommends installing certain programs in those ways. In Debian-based distros, such versions are especially useful if you want only versions of system packages vetted according to their philosophy but want cutting-edge versions of desktop applications. Even beyond such distros, some of these programs are maintained well (perhaps better than you think if you only look at releases) but don't provide distro-specific packages or even releases often (or the distro doesn't vet, process, or accept the packages due to lack of help or by choice). See the lists of programs currently recommended to be obtained by special means:
- [Flatpaks.list](Flatpaks.list) (maintained on developer's computer via `cd projects && flatpak list --app | cut -f1 > Flatpaks.list`)
  - except ignore those in [projects/Flatpaks-only_for_testing.list](projects/Flatpaks-only_for_testing.list).
    - For installing **Minetest**, you should normally use Poikilos' [EnlivenMinetest](https:/github.com/poikilos/EnlivenMinetest) instead for the minetest.org version with a stable API and official support for many mods. Minetest documents or scripts in linux-preinstall are secondary if present and may be removed at any time or may download EnlivenMinetest scripts.
  - or see projects/Flatpaks-all.list but ignore those also in that list or in projects/Flatpaks-runtimes.list (Runtime packages are automatically installed as dependencies for the installed apps). NOTE: There is at least one that has an asterisk since each version has a different package name (The version number is in the package name). The list was made manually by comparing Flatpaks.list to projects/Flatpaks-all.list.
  - Flatpaks can be installed system-wide with sudo then automatically updated in one shot via `sudo flatpak update`!
- [AppImages.list](AppImages.list): This list is manually maintained such as by comparing it to the result of `ls ~/.local/lib64/ | grep mage` (those installed using [nopackage](https://github.com/poikilos/nopackage); only old versions would be somewhere like `ls ~/Downloads/1.InstallManually | grep mage`) on the developer's computer.
- [Unpackaged.list](Unpackaged.list) (generated manually on the developer's computer such as by comparing it to `ls ~/.local/lib64/ | grep -v mage` and `ls ~/.local/lib`)
  - Unpackaged versions of Blender are available via Poikilos' [blendernightly](https://github.com/poikilos/blendernightly) project.
  - Some of these programs are recommended to be built from source. In such cases, usually a scripts to build the software from source (or a document describing how) is in the linux-preinstall project.
  - Some applications are in zip/gz/etc. binary distributions and have install scripts in this project historically (predating the nopackage project), but in such cases instead use [nopackage](https://github.com/poikilos/nopackage) to install the software and report any errors at the Issues section on that repository.
  - **world_clock** is available via Poikilos' [world_clock](https://github.com/poikilos/world_clock) repo.
  - **bfg** is a tool for stripping old data from git repos to save space and increase the speed of many operations done over the internet. It may be easier than purging using the git-filter-repo python add-on for git. See "[How to remove/delete a large file from commit history in the Git repository?](https://stackoverflow.com/questions/2100907/how-to-remove-delete-a-large-file-from-commit-history-in-the-git-repository)] on StackOverflow for details on both methods to avoid the older and more complex "git-filter-branch" method.
  - **Ulauncher** is an application launcher with a fast and comprehensive search feature.
  - **Umlet** is a UML diagram creation tool.

The lists and individual program install scripts make programs in linux-preinstall generally easier to install.

Install scripts are categorized by a person's role and/or workflow, such as:
- [everyone](everyone)
- [drivers](drivers)
- [developer](developer)
- [educational](educational)
- [migration](migration)

Folders named "unused" are not recommended, and there may be a better
option. For example, VirtualBox is not recommended, and qemu install
scripts are provided instead.

For an explanation of the expertmultimedia-managed folder, see the "[IT](#IT)" section above.

The names of scripts specify the distro when necessary. See the "[Script Naming Conventions](#script-naming-conventions)" section below for more information.

After running install scripts, post-install instructions are often appended
to a file called PostInstallInstructions.md (It should appear on the
Desktop--See [issue
#18](https://github.com/poikilos/linux-preinstall/issues/18) for more
feature status).

If there is a program that is not available in a repo and not available
on here, it may yet be within one of the scripts (suchas
developer/developer.fedora.sh). If not, it may be on flathub even if
not in any install script in this repo. Otherwise, if only an AppImage,
zipped build, or single binary is available, you can usually use
[nopackage](https://github.com/poikilos/nopackage) to install it (and
an icon!) in one shot.

#### Developer Tools
The linux-preinstall project includes various useful tools for developers in the developer folder, including:
- An improved fork of a geany-openscad highlighter.

#### Server Tools
- `./server/optional/php-set-version.apache.ubuntu.sh` or `./server/optional/php-set-version.nginx.deb.sh`: Choose (specify as a parameter) a specific version of php as the system's php and get all of the matching dependencies such as for WordPress, and uninstall all other versions and their packages. Only use the script that matches your chosen server technology (Apache or NGINX)!

##### Server Scripts
- See [System commands][#system-commands].

#### Configuration Tools
##### MATE
The linuxpreinstall.mate module manages the MATE desktop environment.

For managing panels, the list of IDs is a list of strings, but each
object definition is a different path. Use the id to construct the path.
The structure is clear when browsing org/mate/panel/objects using
dconf-editor:

Each item has the following values (IDs/values in parens
below are only examples). This list is a list of values for one item
(the example item is org/mate/panel/objects/object-1/, which varies
depending on your configuration (the actual ID folder would be in
`gsettings get org.mate.panel object-id-list`.
- enumeration action-type 'The action type this button represents.
  Possible values are "lock", "logout", "run", "search" and
  "screenshot". This key is only relevant if the object_type key is
  "action-applet".'
  - Default: 'none'
  - Current value: Default value
- string applet-iid:
  - "WnckletFactory::ShowDesktopApplet" (object-1)
- string attached-toplevel-id "Panel attached to drawer"
  (default '', Current value: Default value)
- string custom-icon
- Boolean has-arrow (true)
- string launcher-location
  (default '', Current value: Default value)
- Boolean locked
- menu-string path 'The path from which the menu contents is
  [constructed]. This key is only relevant if the use_menu_path key is true
  and the object_type key is "menu-object".' [fixed spelling]
  - Default: 'applications:/'
  - Current value: Default value
- enumeration object-type
  - Default: 'launcher'
  - Current value: 'applet'
- Boolean panel-right-stick 'Interpret position relative to the
  bottom/right edge'
- i (Signed 32-bit integer) position: "...number of pixels from the
  left (or top if vertical) panel edge." -- See also
  `panel-right-stick`.
- string tooltip
- string toplevel-id: "Toplevel panel containing object"
  - Default: ''
  - Current value: 'top'
- Boolean use-custom-con
- Boolean use-menu-path: "Use custom path for menu contents"
  - Default: false
  - Current value: Default value


### Script Naming Conventions
Pick which folders and scripts to run based on whatever you want to do
(See the "[Software and Software Group
Installation](#software-and-software-group-installation)" section).

For best results, the following usage order is recommended:
1. Run the chosen script without `*-nonroot` in the name if present, and
   run any such script as `root` (or via `sudo bash` followed by the
   script name).
2. Run the matching script where the name is the same except with
   "-nonroot" or "-sudoer" added to the name if there is one. Run the
   "-nonroot" script as regular user (without sudo).
   - Some of the scripts call sudo but change settings for the current
     user. Such scripts (should) have "sudoer" in the name.

- If the name includes .debian.*, then it is known to work on Debian and may work on Ubuntu.
- If the name includes .ubuntu.*, then it is known to work on Ubuntu and probably will not work on Debian.
- If the name includes .deb.*, then it may work on Debian, Ubuntu or any other deb-based distro.
- If the name includes .fedora.*, then it will work on Fedora but may not work on other rpm-based distros.
- If the name doesn't include any distro name, the script attempts to adapt to all popular distros *(If such a script fails to detect a known package installer command or other known and applicable distro-specific feature, it will show an error and return non-zero on exit)*.

### Utility Scripts
Additional scripts (scripts that do things rather than install things) are for IT and developer use, but may serve other people as well:
- [utilities](utilities)
- [utilities-developer](utilities-developer)


## Related Projects
Related projects
- [nopackage](https://github.com/poikilos/nopackage): Install any AppImage, archive, deb, or binary as an icon (download icons automatically when known!) on any GNU+Linux system!
  - formerly the linux-preinstall tool called install_any.py
- [rotocanvas](https://github.com/poikilos/rotocanvas): has several useful commands related to image sequences including (browseable) image "playlists".
- [TemperatureSanitizer](https://github.com/poikilos/TemperatureSanitizer): See also TEMPerV1 verbose output files (files named with -vvv) for technical info.


## Modular Features
The linux-preinstall project makes some commands available to you to
use via any terminal (within the scope of the installation, whether
that be a root or user install). The following subsections describe
those features.  To get the linuxpreinstall (The Python module, as
opposed to scripts not in the linuxpreinstall directory but still
inside linux-preinstall), you must perform the Python installation (See
the "[Install](#install)" section).

### sortversion
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

### System commands
The system commands become available after installing the repository
via pip (See the "[Install](#install)" section).
- `findmime`: Find files by full/partial mimetype (such as "jpeg" or
  "image"!) in the current directory.
- `cleanif`: Remove files from directory 1 if they exist in directory 2
  (great for if you unzip or copy a load of files to the wrong place!)
- `unredirect_md`: Change every redirect in a Markdown file to a real
  URL, whether there is an encoded URL in any query param (such as
  `q=https%3A%2F%2Fblendermarket.com%2Fproducts%2FNatureClicker`)
  or there is a 302 response.
- `selectoutput`: Select an output using a fuzzy search string such as
  analog or HDMI (not case-sensitive; requires pulseaudio-utils).
  - For an automated reconnect to run first, see
    utilities/reconnect-audio.sh which calls `selectoutput hdmi` if
    `selectoutput` is in the path.
- `whichicon`: Find what icon (.desktop) file provides a given command.
- `sort-brisk-menu-favs`: can sort the favorites ("Favourites"
  (en_GB)) menu.
- `remove-bad-mate-items`: Remove bad mate items (if no param is
  specified, remove items with a blank `applet-iid`).
- `unthing`: See [linuxpreinstall/thingi.py](linuxpreinstall/thingi.py)
  for documentation.
- `thumbnails`: Clear thumbnail(s) for the specified file(s) so that the
  OS will regenerate the thumbnail cache for the specified file(s) on
  the next load/refresh of the folder in a File Explorer. See
  [linuxpreinstall/thumbnails.py](linuxpreinstall/thumbnails.py) for
  documentation.

#### pycodetool commands
The following scripts utilize <https://github.com/poikilos/pycodetool>:
- `changes`: Look for repos in the current directory and show what
  changes are not yet committed (including untracked).

#### System commands for servers
- [backup-nginx-symlinks](linuxpreinstall/server/backup_nginx_symlinks.py)


### Commands moved to other repos
#### nopackage
The old install_any.py script's features have been moved to
<https://github.com/poikilos/nopackage> which provides the new command
`nopackage`:

You can use `nopackage` to install almost anything, such as a single
file (AppImage or other), a zip file, or to install a deb package on
any distro in your profile, all without superuser priveleges!

#### ggrep
- `ggrep`: Get a geany command to go to the line in the file from grep
  (searching within file(s)). Recursively search directories by default.
  - Moved to [hierosoft](https://github.com/Hierosoft/hierosoft)


## More Information
See the [doc](doc) folder for fixes for your specific problem that may
not be scripted yet or to learn more about GNU+Linux systems.


## Changes
See [changelog.md](changelog.md)


## References
See [doc/references.md](doc/references.md)
