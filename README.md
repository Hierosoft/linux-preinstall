# linux-preinstall
Put first-time setup in easy mode for GNU+Linux systems! Make the system ready to use from day one.

These scripts automatically install programs and configure settings many users expect, and inform you of any manual steps needed. I regularly update and use these scripts for myself and people I help. These scripts have been in development since 2016, but due to growth and specialization I've added them to git to make installation even easier (web install from git).

## GOALS
* Make the GNU+Linux system ready to use from day one.
* Separate scripts by distro (Ubuntu, Fedora).
* Separate scripts by workflow (end user, developer, server).

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
```
For best results, the following usage order is recommended. All scripts
except `*-nonroot.sh` scripts must run as `root` (or with `sudo bash`):
* distro-specific folders (such as everyone-fedora)
* universal folders that are not distro-specific (such as everyone)
* nonroot scripts (run as regular user without sudo, though some of the
  scripts call sudo but change settings for the current user).

### Notable Features
* You can use utilities/install_any.py to install deb packages!
  - It seems to only be able to use tar to exctact xz files if you use
    Python 3 (Python 2 doesn't work).
![Screenshot of using install_any.py and the resulting installed
shortcuts from a directories, archive, deb, or appimage](media/screenshot-install_any.jpg)


## Developer notes
* For silent installation, dealing with files marked
  `linux_preinstall_interactive=true` somehow is necessary (either
  automating them more, or noting how to proceed in $postinstall doc)
  - [ ] A code audit is needed: all script files that aren't silent
    installs should have the boolean value.
  - See "developer-fedora/mysql-community-server.sh" for an example.
