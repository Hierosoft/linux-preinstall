# Always Do (Linux)

## Note caveats for users
* Alt Right-click and scroll wheel zooms in and out of entire screen

## Always Remove
* Mono is broken often, so:
```bash
pacman -R dbus-sharp fsharp gdata-sharp gtk-sharp-2 gtk-sharp-3 keepass mono-addins mono-zeroconf monodevelop-stable msbuild-15-bin nuget referenceassemblies-pcl taglib-sharp-git banshee dbus-sharp-glib gconf-sharp gio-sharp gkeyfile-sharp gnome-keyring-sharp gudev-sharp mono-upnp notify-sharp pinta gtk-sharp-beans
```

## Remaining Issues
* Graphical corruption in gtk3 (seems to be mostly wxgtk applications such as FileZilla and codeblocks) where window draws itself though it shouldn't have focus, then is gradually drawn over by other applications as you use them (problem seems to go away when application is minimized)
  * Didn't try:
    * Application menu, Settings, Window Manager Tweaks:
      * [OPTIONAL) Focus: [fix breakage from Mono applications where application gaining focus causes partial window overlay errors]
        * "Activate focus stealing prevention": No (default is No; only works with "focus follows mouse"  according to TheAmigo from <https://unix.stackexchange.com/questions/156515/how-to-forbid-windows-from-stealing-focus-in-xfce4>) but that is not desirable since bumping mouse will switch focus.
        * "Honor ICCCM focus hint": No (default is Yes)
        * When a window raises itself: Do nothing (default is "Bring window on current workspace")

* monodevelop doesn't work, try building mono a tricky way (idea: install then remove mono, so you have the optional dependencies):
```
### remaining configuration issues
#(happens even if installed: clang)
#(can't find any mt [manifest tool] equivalent in arch)
#(no errors, all seem to be optional):
#checking for mt... no
#checking if : is a manifest tool... no
#checking sys/filio.h usability... no
#checking sys/filio.h presence... no
#checking for sys/filio.h... no
#checking sys/sockio.h usability... no
#checking sys/sockio.h presence... no
#checking for sys/sockio.h... no
#checking sys/mkdev.h usability... no
#checking sys/mkdev.h presence... no
#checking for sys/mkdev.h... no
#checking for sys/sysctl.h... yes
#checking libproc.h usability... no
#checking libproc.h presence... no
#checking for libproc.h... no
#checking sys/prctl.h usability... yes
#checking ieeefp.h usability... no
#checking ieeefp.h presence... no
#checking for ieeefp.h... no
#checking for _finite... no
#checking for _finite in math.h... no
#checking for clang... no
#checking pthread_np.h usability... no
#checking pthread_np.h presence... no
#checking for pthread_np.h... no
#checking for pthread_mutex_timedlock... yes
#checking for pthread_getattr_np... yes
#checking for pthread_attr_get_np... no
#checking for pthread_setname_np... yes
#checking for pthread_cond_timedwait_relative_np... no
#checking sys/event.h usability... no
#checking sys/event.h presence... no
#checking for sys/event.h... no
#checking for kqueue... (cached) no
#checking checklist.h usability... no
#checking checklist.h presence... no
#checking for checklist.h... no
#checking pathconf.h usability... no
#checking pathconf.h presence... no
#checking for pathconf.h... no
#checking for sys/statvfs.h... yes
#checking sys/statfs.h usability... yes
#checking sys/statfs.h presence... yes
#checking for sys/statfs.h... yes
#checking sys/vfstab.h usability... no
#checking sys/vfstab.h presence... no
#checking for sys/vfstab.h... no
#checking for struct kinfo_proc.kp_proc... no
#checking CommonCrypto/CommonDigest.h usability... no
#checking CommonCrypto/CommonDigest.h presence... no
#checking for CommonCrypto/CommonDigest.h... no
#checking localcharset.h usability... no
#checking localcharset.h presence... no
#checking for localcharset.h... no
#checking for locale_charset in -liconv... no
#checking for locale_charset in -lcharset... no
#still unresolved:
#checking for aintl in -lsunmath... no
#checking if big-arrays are to be enabled... no
cd $HOME
if [ ! -d Downloads ]; mkdir Downloads
#the following error happens even if gettext is installed in Antergos:
#Unhandled Exception:
#System.MissingMethodException: Method 'System.Globalization.CultureInfo.set_CurrentUICulture' not found.
if [ -f "$(command -v apt)" ]; then sudo apt install git autoconf libtool automake build-essential mono-devel gettext cmake; fi
#if [ -f "$(command -v pacman)" ]; then sudo pacman -Syu base-devel; fi
#NOTE: base-devel is included with base install
if [ -f "$(command -v pacman)" ]; then sudo pacman -Syu git autoconf libtool automake gettext cmake; fi
#NOTE: an arch equivalent for mono-devel doesn't seem to exist, but building works anyway
git clone https://github.com/mono/mono.git
cd mono
sudo pacman -R mono
#just get mcs, a trick from the  [README.md](https://github.com/mono/mono/blob/master/README.md) (NOT from [compiling mono in linux](http://www.mono-project.com/docs/compiling-mono/linux/)):
PREFIX=/usr/local
./autogen.sh --prefix=$PREFIX
make get-monolite-latest
make
#optional (test suite): make check
sudo make install
```

## For Everyone

Install
* Xfce group (things don't go well  unless you install the whole group)
and: xfce-polkit xfce4-whiskermenu-plugin xfce4-dockbarx-plugin xfce4-pulseaudio-plugin mugshot fontweak
  * xfce-polkit (so user gets prompted to run certain GUI programs with sudo)
  * xfce4-whiskermenu-plugin
  * xfce4-dockbarx-plugin (advantage of dockbarx is that it will let you right-click and "create custom launcher" if can't pin (it can therefore effectively pin any program that other docks can't)
  * xfce4-pulseaudio-plugin
  * yaourt -Syyu --noconfirm --aur mugshot -- if not installed, double-clicking your generic profile picture on the top left in the whisker menu causes dialog box with "Error" "Failed to edit profile." "Failed to execute child process “mugshot” (No such file or directory)"
  * fontweak is "a GUI front-end of fontconfig" [sic] (controls font rendering settings)
* Manually login as the user, then manually implement Xfce4 user-side settings:
  `echo "gtk-error-bell = 0" >> ~/.gtkrc-2.0` (remove beep when say, backspacing in FileZilla dialogs or search bar in Thunar)
    * CentOS: `echo 'set bell-style none' >> ~/.inputrc` as per https://unix.stackexchange.com/questions/152691/how-to-disable-beep-sound-in-linux-centos-7-command-line/152694#152694
    * see also `set bell-style none` /etc/inputrc (may work system-wide, and has a premade line for it to uncomment)
  * Remove bottom bar
  * move top bar to bottom
  * remove menu & add whiskermenu there
  * add places menu next
  * add dockbarx plugin next
  * add spacer (with Expand option)
  * add clock
  * place notification area next
  * then trash
  * then pulseaudio plugin
  * always last: Show desktop
  * instruct user on finding items and pinning open applications
  * give them the icons that can't be found in Whisker menu, from my ownCloud/Linux/AlwaysInstall
  * Set window to not maximize (Instead, remember): Whisker Menu, Settings, Window Manager, Advanced, Double click action: change from "Maximize" to "None"
  * In Thunar, show file time (instead of "Today," "Yesterday" or date): Open Thunar, click Edit, Preferences, then change Format under Date.
  * Application menu, Settings, Window Manager:
    * Style:
      * remove shade button by dragging it to "Hidden" category
    * Advanced:
      * "Double click action": "Maximize window" (default is Shade window(?))
  * Application menu, Settings, Window Manager Tweaks:
    * Accessibility:
      * "Use mouse wheel on title bar to roll up the window": No
      * "Notify of urgency by making window's decoration blink": Yes (default is No)
    * Workspaces:
      * "Use the mouse wheel on the desktop to switch workspaces": No
  * set borders to Numix (has 4px instead of 1px bottom: see [Xfwm4: improve accessibility (wider bottom edge)](https://github.com/MaxKh/numix-gtk-theme/commit/6057a2d907a2e3014ae9e268e1aed8dc819a55c8))
Install Xfce and whisker menu
Install a volume button daemon if keyboard has volume controls
* try a community repo, otherwise try a shell script: https://bbs.archlinux.org/viewtopic.php?id=124513
Disable window rollup feature (xfce >= 4.8):
```
xfconf-query -c xfwm4 -p /general/mousewheel_rollup -s false
#Allow installing firefox-nightly install to succeed:
#see https://aur.archlinux.org/packages/firefox-nightly/
#(running with sudo doesn't work for some reason--I ran with & didn't work then without then it worked)
#sudo gpg --keyserver pgp.mit.edu --recv-keys 14F26682D0916CDD81E37B6D61B7B526D98F0353
#and firefox-developer
#see https://aur.archlinux.org/packages/firefox-nightly/
#sudo gpg --recv-keys --keyserver hkp://pgp.mit.edu 1C69C4E55E9905DB
gpg --keyserver pgp.mit.edu --recv-keys 14F26682D0916CDD81E37B6D61B7B526D98F0353
#and firefox-developer
#see https://aur.archlinux.org/packages/firefox-nightly/
gpg --recv-keys --keyserver hkp://pgp.mit.edu 1C69C4E55E9905DB
#change hostname permanently
```

#### Ubuntu Xenial
```
echo
echo "forcing updated Blender build"
echo "see also http://ubuntuhandbook.org/index.php/2017/09/blender-2-79-released-install-it-in-ubuntu/"
echo
sudo add-apt-repository ppa:thomas-schiex/blender
sudo apt update
sudo apt install blender
echo "Remove via:"
echo "  sudo ppa-purge ppa:thomas-schiex/blender"
echo "  sudo add-apt-repository --remove ppa:thomas-schiex/blender"
echo "  #see also https://unix.stackexchange.com/questions/60595/how-to-undo-sudo-add-apt-repository"

```

#### Arch
```
# use the binary version of webgitgtk
# since it takes (up to 13) hours to compile and as of Jan 2018 says missing enchant-2.2 even when enchant-pure (2.2) is installed; webgitgtk AUR maintainer says to install testing version of enchant-pure but I don't want to install the testing repo
su root
echo "[archlinuxcn]" >> /etc/pacman.conf
# using single-quotes, '$' doesn't have to be escaped:
echo 'Server = https://cdn.repo.archlinuxcn.org/$arch' >> /etc/pacman.conf
```

##### Antergos
```
pacman -Syu reflector
#get US servers updated in last 12 hrs and write to mirrorlist:
reflector --country 'United States' --age 12 --protocol https --sort rate --save /etc/pacman.d/mirrorlist
pacman -Syu git
if [ ! -d $HOME/tmp ]; then   mkdir $HOME/tmp; fi
if [ ! -d $HOME/tmp/pamac-build-$USER ]; then   mkdir $HOME/tmp/pamac-build-$USER; fi
echo "You must manually set pamac to use $HOME/tmp/pamac-build-$USER for build tmp"

if [ ! -d $HOME/tmp/yaourt-tmp-$USER ]; then
  if [ -d /tmp/yaourt-tmp-$USER ]; then
    mv /tmp/yaourt-tmp-$USER $HOME/tmp/
  else
    mkdir $HOME/tmp/yaourt-tmp-$USER
  fi
fi
if [ ! -d /tmp/yaourt-tmp-$USER ]; then   rm -Rf /tmp/yaourt-tmp-$USER; fi
cd /tmp
#manually change TMPDIR to that folder:
#sudo nano /etc/yaourtrc
#or automatically since commented by default:
echo "TMPDIR=$HOME/tmp" > /tmp/my_yaourt_tmp
#tmp file is needed to store user name since su only knows root
su -c "cat /tmp/my_yaourt_tmp >> /etc/yaourtrc"
#then for double safety (though anything in  tmp can't be guaranteed to stay):
ln -s $HOME/tmp/yaourt-tmp-$USER
echo "NOTE: yaourt-tmp-$USER subfolder is ALWAYS appended to TMPDIR by yaourt but NOT by pamac (gui) so the full path must be chosen manually in gui"

echo "using AUR version of mono since git version of monodevelop requires mono>=5.4.0 (which is version of mono-stable) [and official arch package mono-addins (required by official arch monodevelop package) has broken signing] as of 2017-11 (requires removing non-git versions, which conflict)..."
sudo pacman -R mono nuget gtk-sharp-3 gtk-sharp-2 mono-addins msbuild-bin
yaourt -R gtk-sharp-3 gtk-sharp-2 mono-addins-git
echo "installing fsharp (fsharpc command is expected while building monodevelop from git)..."
yaourt -Sy fsharp
#yaourt -Sy mono-git
echo "installing mono-stable which will use mono to compile then remove mono..."
yaourt -Sy mono-stable
echo "using AUR msbuild-stable instead of msbuild-bin to avoid problems (see <https://aur.archlinux.org/packages/msbuild-bin/>)..."
yaourt -Sy msbuild-stable
echo "mono-addins (required by monodevelop)..."
echo "using git version since ASSUMING signing for non-git mono-addins is still broken (see <https://bugs.archlinux.org/task/56234>)"
#since 'u' option doesn't ever find package:
yaourt -Sy mono-addins-git
echo "installing referenceassemblies-pcl (required by monodevelop)..."
sudo pacman -Syu referenceassemblies-pcl
echo "using git version of monodevelop since ASSUMING other versions still don't build..."
yaourt -Sy monodevelop-git

#didn't work, so
git clone https://github.com/mono/monodevelop.git
git clone https://github.com/mono/mono-addins.git
cd mono-addins
```

### Developer


* successor to jslint which was merged with kate when Kate-plugins (still a python wheel) was, but then removed from Kate since people considered jslint to be too opinionated -- see https://stackoverflow.com/questions/10707869/what-is-the-most-effective-javascript-syntax-checking-solution/10708007#10708007 and https://stackoverflow.com/questions/17935343/how-to-install-kate-plugins
```
yaourt -Syu nodejs-jshint
```

#### Power user tips
* scrollback in console when using a process via the screen command: Ctrl A then [
  (see <http://www.pixelbeat.org/lkdb/screen.html>)
* sort processes by memory usage
  `ps aux --sort -rss`
* REISUB (restart even if frozen): DISABLED BY DEFAULT in many modern distros, for security (since these magic keys can be sent via remote terminal)
  by Phoenix from <https://askubuntu.com/questions/4408/what-should-i-do-when-ubuntu-freezes/36717#36717> edited 1 Sep 2015
  If it locks up completely, you can REISUB it, which is a safer alternative to just cold rebooting the computer.
```
  Do "REISUB" as follows:

  While holding Alt and the SysReq (Print Screen) keys, type REISUB.

  R:  Switch to XLATE mode
  E:  Send Terminate signal to all processes except for init
  I:  Send Kill signal to all processes except for init
  S:  Sync all mounted file-systems
  U:  Remount file-systems as read-only
  B:  Reboot
  REISUB is BUSIER backwards, as in "The System is busier than it should be", if you need to remember it. Or mnemonically - R eboot; E ven; I f; S ystem; U tterly; B roken.

  NOTE: There exists less radical way than rebooting the whole system. If SysReq key works, you can kill processes one-by-one using Alt+SysReq+F. Kernel will kill the mostly «expensive» process each time. If you want to kill all processes for one console, you can issue Alt+SysReq+K.

  NOTE: You should explicitly enable these key combinations. Ubuntu ships with sysrq default setting 176 (128+32+16), which allows to run only SUB part of REISUB combination. You can change it to 1 or, which is potentially less harmful, 244. To do this:

  sudo nano /etc/sysctl.d/10-magic-sysrq.conf
  and switch 176 to 244; then

  echo 244 | sudo tee /proc/sys/kernel/sysrq
  It will immediately work! You can test this by pressing Alt+SysReq+F. For me, it killed active browser tab, then all extensions. And if you will continue, you can reach X Server restart.

  More info on all the Alt+SysReq functions [here](http://en.wikipedia.org/wiki/Magic_SysRq_key).
```

### Machine Owned by Tech Support Provider

(any GNU/Linux System)
* avoid bash wierdness by asking for sudo password first before anything bad happens like pasting this code causes it to thing you are pasting a password for the first sudo command:
```
sudo echo ""
sudo echo ""
if [ ! -f "$HOME/logmein-client.bak" ]; then
  if [ -f /usr/local/bin/logmein-client ]; then
    sudo mv /usr/local/bin/logmein-client "$HOME/logmein-client.bak"
  fi
fi
sudo echo "" > /usr/local/bin/logmein-client
sudo nano /usr/local/bin/logmein-client
```
* paste the following:


```
sudo chmod +x /usr/local/bin/logmein-client
#avoid breaking installation of arch-based distro
# yaourt -Syu packagename
# NOT -S and definitely not -Sy -- see https://www.reddit.com/r/archlinux/comments/6a4qh5/arch_completely_broken_due_to_missing_libssl_and/ :
#  gathered there was a short time window where people could get hit by this because pacman's new package and the library's new package weren't showing up at the exact same time. This weren't a lot of people. Then next, there are a lot of people that run "pacman -Sy" instead of "-S" or "-Syu". That was then the main round of people that had their system break.
#People do this "-Sy" stuff because it's occasionally getting recommended by someone, so this idea never dies. It's getting recommended when people ask why they get an error when they try to install a package with "-S name". The error comes from their local database being older than what's in the repos and meanwhile the package they try to install had a newer version. The "-Sy name" fixes it because the database gets synced, and they are happy that the package gets installed.
```

## Everyone
* Install: chromium


## Make Thunar default (such as for open containing folder of downloaded file in chromium etc):
```
touch ~/.local/share/applications/defaults.list
echo "[Default Applications]" >> ~/.local/share/applications/defaults.list
echo "inode/directory=thunar.desktop" >> ~/.local/share/applications/defaults.list
```
* To force other desktop files to point to Thunar without modifying
  builtin desktop files, override them in ~/.local as in method shown
  below "Using Midnight Commander" at
  <https://help.ubuntu.com/community/DefaultFileManager>:
  * `nano ~/.local/share/applications/nautilus-browser.desktop`
    then paste:
```
[Desktop Entry]
Encoding=UTF-8
Name=File Browser
Comment=Browse the file system with the file manager
TryExec=mcterm
Exec=mcterm %U
Icon=system-file-manager
Terminal=false
StartupNotify=true
Type=Application
NoDisplay=true
Categories=GNOME;GTK;System;Utility;Core;
OnlyShowIn=GNOME;
X-GNOME-Bugzilla-Bugzilla=GNOME
X-GNOME-Bugzilla-Product=nautilus
X-GNOME-Bugzilla-Component=general
X-GNOME-Bugzilla-Version=2.28.1
X-Ubuntu-Gettext-Domain=nautilus
```
  * `nano ~/.local/share/applications/nautilus-folder-handler.desktop`
    then paste:
```
[Desktop Entry]
Encoding=UTF-8
Name=Open Folder
TryExec=mcterm
Exec=mcterm %U
NoDisplay=true
Terminal=false
Icon=folder-open
StartupNotify=true
Type=Application
MimeType=x-directory/gnome-default-handler;x-directory/normal;inode/directory;application/x-gnome-saved-search;
OnlyShowIn=GNOME;
X-GNOME-Bugzilla-Bugzilla=GNOME
X-GNOME-Bugzilla-Product=nautilus
X-GNOME-Bugzilla-Component=general
X-GNOME-Bugzilla-Version=2.28.1
X-Ubuntu-Gettext-Domain=nautilus
```
  * `nano ~/.local/share/applications/nautilus-home.desktop`
    then paste:
```
[Desktop Entry]
Encoding=UTF-8
Name=Home Folder
Comment=Open your personal folder
TryExec=mcterm
Exec=mcterm
Icon=user-home
Terminal=false
StartupNotify=true
Type=Application
Categories=GNOME;GTK;Core;
OnlyShowIn=GNOME;
X-GNOME-Bugzilla-Bugzilla=GNOME
X-GNOME-Bugzilla-Product=nautilus
X-GNOME-Bugzilla-Component=general
X-Ubuntu-Gettext-Domain=nautilus
```


### OPTIONAL

* Install redshift: changes color temperature of screen based on your
  surroundings (as determined by GPS or manual position, and time)

* Force immediate save to bash_history:
(see http://web.archive.org/web/20090815205011/http://www.cuberick.com/2008/11/update-bash-history-in-realtime.html )
```
echo "shopt -s histappend" >> ~/.bashrc
echo "PROMPT_COMMAND=\"history -a;\$PROMPT_COMMAND\"" >> ~/.bashrc
```

* Install Shadow icons theme
* make pc speaker go away in nautilus on backspace or delete:
  * manual fix
  ```
  xsetboff_path=/etc/systemd/system/xsetboff.unit
  sudo nano $xsetboff_path
  #OR? sudo nano /etc/sysctl.d/xsetboff
```
  * NOTE: unit files installed by packages reside in /usr/lib/systemd/system/
  * (formerly init.d, but "Arch now uses systemd rather than openRC"-- see https://bbs.archlinux.org/viewtopic.php?id=194843 )
  * enter the following unit file then:
```
  sudo chmod +x $xsetboff_path
```
  * stuff that didn't work:
```
  #see https://unix.stackexchange.com/questions/214607/how-to-disable-beep-tone-in-xfce-when-the-delete-button-is-pressed
  #turn off bell for all X applications
  echo "xset b off" >> ~/.bashrc
  #only works after you open a terminal at least once
```

  * other stuff not tried:
```
  echo "set bell-style none" >> ~/.inputrc
  #then reload manually:
  bind -f ~/.inputrc
  #one answer is http://xfce.10915.n7.nabble.com/Beep-td8866.html
  echo "gtk-error-bell = 0" >> ~/.gtkrc-2.0
  #see also https://debian-administration.org/article/110/Removing_annoying_console_beeps
  # "actually affects all programs that use GNU Readline"
  echo 'set bell-style none' >> ~/.inputrc
```

## Fedora:

### Any Fedora:
* Install Fedy, then via Fedy install: Chrome, Flash Player, Skype, DVD Playback, Steam (optionally),
```bash
sudo sh -c 'curl https://www.folkswithhats.org/installer | bash'
```

### Fedora 25:
* gui method: http://labtestproject.com/using_linux/permanently_change_hostname_on_fedora
* terminal method (change $1 to desired hostname):
```
#(see https://fedoramagazine.org/set-hostname-fedora/ )
sudo hostnamectl set-hostname $1
```
* Set clock to 12hr format

## Development
* Change git username (replace $1 with your git username in the
  following): `git config --global user.name "$1"`

## Laptop Only
* sign into freesound.org and download battery low sound such as http://freesound.org/people/eggtimer/sounds/103057/ to /home/owner/ownCloud/Samples
* open in audacity, do Noise Reduction, Fade In, Fade Out, Compressor, export with 1b at end of filename
```
cd $HOME
ln -s /home/owner/ownCloud/Samples/127967__n-a-n-i__when-the-toys-go-winding-down1b.wav battery-low.wav
#ln -s /home/owner/ownCloud/Samples/103057__eggtimer__battery-low1b.wav battery-low.wav
```
* set low battery warning (such as in Xfce "Battery Monitor" item) to:
```
mplayer /home/owner/battery-low.wav
```

## Stuff that didn't work

* possibly change Geany Terminal (Edit, Preferences, Tools, Terminal) to:
  NOTE: `gnome-terminal -x "/bin/bash" %c` leaves Geany without the ability to detect terminal is still open
  (default is `xterm -e "/bin/sh %c"`)
  otherwise share clipboard with gui clipboard: `xterm -ls -xrm 'XTerm*selectToClipboard: true' -e "/bin/sh %c"`

### Plugins for Kate (such as jslint)
THESE STEPS DO NOT WORK, so use jshint instead and run manually redirecting > output (not 2> output) to err.txt (then run output inspector in same directory)
Below is repaired version of instructions from https://pypi.python.org/pypi/Kate-plugins
Changes:
* remove slash after parenthesis, since prefix includes slash
* before ln, mkdir (and assurances before mkdir, in case kde4 is not installed) since "kate" dir doesn't exist in user's kde4 config dir by default
* for ln, use the copy of kate-plugins that is in python2.7 site-packages
* use python2's pip, since python3's has python2 code in it still so install fails with:

```
    Complete output from command python setup.py egg_info:
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/tmp/pip-build-lzhmk_q7/pysmell/setup.py", line 27
        print post_install_message
                                 ^
    SyntaxError: Missing parentheses in call to 'print'. Did you mean print(print post_install_message)?
    ----------------------------------------
    Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-build-lzhmk_q7/pysmell/
```


...therefore you must switch to the python2 version of the package:

```
sudo pacman -Syu python2-pip
sudo python2 -m pip install --upgrade pip wheel setuptools
sudo python2 -m pip install Kate-plugins
#cd first to avoid being in a weird folder in case kde4-config is not present and something really strange happens causing -d to return true when kde4 is not installed.
cd
if [ -d "$(kde4-config --localprefix)" ]; then
  if [ ! -d "$(kde4-config --localprefix)share" ]; then
    mkdir $(kde4-config --localprefix)share
  fi
  if [ ! -d "$(kde4-config --localprefix)share/apps" ]; then
    mkdir $(kde4-config --localprefix)share/apps
  fi
  if [ ! -d "$(kde4-config --localprefix)share/apps/kate" ]; then
    mkdir $(kde4-config --localprefix)share/apps/kate
  fi
  if [ ! -d "$(kde4-config --localprefix)share/apps/kate/pate" ]; then
    mkdir $(kde4-config --localprefix)share/apps/kate/pate
  fi
  #ln -s /PATH/OF/THE/EGG/kate_plugins/ $(kde4-config --localprefix)/share/apps/kate/pate
  #1st param after -s is example and param after that has extra slash, so instead do:
  ln -s /usr/lib/python2.7/site-packages/kate_plugins/ $(kde4-config --localprefix)share/apps/kate/pate
  echo "Finished attempting to create symlink to python2 site-packages version of kate_plugins"
else
  echo "ERROR: Nothing was done since you need (Kate and hence) kde4 installed in order to use kde4-config to get user's plugins folder"
fi
```


