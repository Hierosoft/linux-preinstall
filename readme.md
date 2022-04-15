# linux-preinstall
Put first-time setup in easy mode for GNU+Linux systems! Make the system ready to use from day one.

These scripts automatically install programs and configure settings many users expect, and inform you of any manual steps needed. I regularly update and use these scripts for myself and people I help. These scripts have been in development since 2016, but due to growth and specialization I've added them to git to make installation even easier (web install from git).

Install only the packages you want for the specific task (such as development, video, streaming, desktop publishing, etc), but don't miss any you need (These groups may be lighter or heavier than distro-specific groups defined in the repositories, but usually lighter and more comprehensive for creators of any sort. The project is moving toward using metadata and Python to avoid the overlap between different groups and reduce the size of each group).

Installing the linuxpreinstall python module also adds some useful commands:
- findmime: Find files by full/partial mimetype (such as "jpeg" or "image"!) in the current directory.
- cleanif: remove files from directory 1 if they exist in directory 2 (great for if you unzip or copy a load of files to the wrong place!)

## GOALS
* Make the GNU+Linux system ready to use from day one.
* Separate scripts by distro (Ubuntu, Fedora).
* Separate scripts by workflow (end user, developer, server).
* Move as many features to the python linuxpreinstall module as seems
  reasonable.


## Related Projects
Related projects
- [nopackage](https://github.com/poikilos/nopackage): Install any AppImage, archive, deb, or binary as an icon (download icons automatically when known!) on any GNU+Linux system!
  - formerly the linux-preinstall tool called install_any.py
- [rotocanvas](https://github.com/poikilos/rotocanvas): has several useful commands related to image sequences including (browseable) image "playlists".


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
