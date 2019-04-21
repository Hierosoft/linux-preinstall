# Fedora 28 Notes

#see also $HOME/git/integratoredu/data/units/0/tm/files/(system)/iedu-mps-hourly

## for home only
# * faster owncloud if on same network:
# su -c 'echo "192.168.1.5 login.axlemedia.net" >> /etc/hosts'

## auto-install
wget https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-28.noarch.rpm
wget https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-28.noarch.rpm
rpm -iv rpmfusion-free-release-28.noarch.rpm
dnf -y upgrade
rpm -iv rpmfusion-nonfree-release-28.noarch.rpm
dnf -y install blender inkscape gimp thunderbird chromium owncloud-client git-cola obs-studio keepassxc geany python python2-pillow python3-pillow speedcrunch filezilla darktable avidemux codeblocks qt-creator mypaint krita kate lmms vinagre scantailor vlc mpv librecad freecad gedit catfish meld hexchat ghex simple-scan audacity-freeworld gxmms2 python2-pygame gucharmap tiled evince fontforge qdirstat kdenlive frei0r-plugins redshift redshift-gtk plasma-applet-redshift-control projectM-pulseaudio eclipse-jdt java-1.8.0-openjdk-devel java-1.8.0-openjdk icedtea-web maven shotcut chromium-libs-media-freeworld exfat-utils fuse-exfat unetbootin gimp-elsamuko gimp-resynthesizer gimp-wavelet-denoise-plugin gimp-paint-studio gimp-lqr-plugin gimp-normalmap gimp-lensfun gimp-data-extras GREYCstoration-gimp star sloccount icoutils ladspa-cmt-plugins ladspa-autotalent-plugins ladspa-zam-plugins ladspa-rev-plugins PersonalCopy-Lite-soundfont ardour5 rhythmbox scribus discord libreoffice remarkable discord icoutils python3-pycodestyle gmic-gimp gnome-terminal screen
#NOT lxmusic
#NOT bluez-hid2hci etc (see below for why using builtin KDE functionality instead)
#NOT retext (markdown editor for reStructuredText but not GitHub-style Markdown)

#Save git password without KDE keyring:
dnf -y install libsecret
# see also run as unpriveleged user (git config --global credential.helper libsecret automatically edits:
# echo > ~/.gitconfig <<END
# [credential]
# helper = libsecret
#END


# wayback_machine_downloader (has option to filter by min or max date of snapshot, such as 20150424112013 for irc.minetest.ru--see ~/Downloads/websites/got.sh)
sudo dnf -y install ruby
gem install wayback_machine_downloader
# Usage: it will make a ./websites/* directories automatically when run on a specific web address.

#remarkable: Markdown editor with GitHub markdown syntax support
#projectM-pulseaudio: The projectM visualization plugin for pulseaudio
#sloccount: Measures source lines of code (SLOC) in programs
#privacy-oriented browser:
sudo dnf config-manager --add-repo https://brave-browser-rpm-release.s3.brave.com/x86_64/
dnf -y install brave-keyring brave-browser

#for kivy:
dnf -y install python-devel ffmpeg-libs SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel portmidi-devel libavdevice libavc1394-devel zlibrary-devel ccache mesa-libGL mesa-libGL-devel
dnf -y install python3-pip python2-pip xclip

#compatibility:
dnf -y msttcore-fonts wine-fonts wine-tahoma-fonts-system wine-times-new-roman-fonts-system wine-wingdings-fonts-system

# see manually-install-userspace.sh for:
# * gimp export selection plugin,:
runuser -l owner -c 'sh always-install-Fedora-unpriveleged-user.sh'

# IF GIMP 2.9.8 (works with stylus better supposedly--see https://www.daviesmediadesign.com/project/set-wacom-drawing-tablet-gimp-2018/) is not yet available on your distro's repo (such as Fedora 28 Jan 2018), install the flatpak:
# dnf -y remove gimp
# BUT that will sacrifice all plugins installed above, so reinstall them (see always-install-Fedora-dev-unpriveleged-user.sh)
echo
echo
echo "Installing GIMP flatpak (for more recent version) will require privs to install the repo itself, but GIMP can be still installed as unpriveleged user."
echo
flatpak_icons="/var/lib/flatpak/exports/share/applications"
flatpak_icons_gimp="$flatpak_icons/org.gimp.GIMP.desktop"
flatpak_gimp="/var/lib/flatpak/app/org.gimp.GIMP"
flatpak_gimp_icons="$flatpak_gimp/current/active/export/share/applications"
flatpak_gimp_icon="$flatpak_gimp_icons/org.gimp.GIMP.desktop"
if [ -d "$var_gimp_overlay_dir" ]; then
  echo "WARNING: $var_gimp_overlay_dir already exists. Installing flatpak over it (Ctrl C to cancel)..."
  echo "3..."
  sleep 1
  echo "2..."
  sleep 1
  echo "1..."
  sleep 1
fi
flatpak install https://flathub.org/repo/appstream/org.gimp.GIMP.flatpakref
if [ ! -d "$var_gimp_overlay_dir" ]; then
  echo "ERROR: installing flatpak did not result in '$var_gimp_overlay_dir' for user."
else
  echo "Installed to $var_gimp_overlay_dir"
fi

var_gimp_overlay_dir="$HOME/.var/app/org.gimp.GIMP"
if [ ! -d "$var_gimp_overlay_dir" ]; then
  echo "ERROR: installing flatpak did not result in '$var_gimp_overlay_dir' for user."
else
  echo "Installed to $var_gimp_overlay_dir"
fi
usr_icons="/usr/share/applications"
usr_gimp_icon="$usr_icons/gimp.desktop"
if [ -f "$usr_gimp_icon" ];then
  echo "WARNING: $usr_gimp_icon already exists, so flatpak version will appear alongside it in the application menu"
  echo "since icons in /var/lib/flatpak/exports/share/applications are used by your desktop in addition to $usr_icons (if configured automatically by your version of flatpak)."
fi
usr_icons="/usr/local/share/applications"
usr_gimp_icon="$usr_icons/gimp.desktop"
if [ -f "$usr_gimp_icon" ];then
  echo "WARNING: $usr_gimp_icon already exists, so flatpak version will appear alongside it in the application menu since icons in"
  echo " '/var/lib/flatpak/exports/share/applications' are used by your desktop in addition to $usr_icons (if configured automatically by your version of flatpak)."
  echo " You can manually edit $flatpak_gimp_icon (symlink to it is $flatpak_icons_gimp)"
fi



dnf config-manager --add-repo https://download.sublimetext.com/rpm/stable/x86_64/sublime-text.repo
dnf install sublime-text


#fix No valid kits found error in qtcreator
#(see <https://stackoverflow.com/questions/40978510/qt-creator-on-fedora-25-no-valid-kits-found>):
dnf -y install make gcc-c++ gdb qt5*-devel
#qt5-devel

#ignore xgalaga-sdl -- says works with SDL2 but configure fails on finding SDL (should compile with SDL1.2-devel packages though)
#SDL_gfxPrimitves (with alpha), SDL_rotozoom, SDL_framerate, SDL_imageFilter (with MMX), SDL_gfxBlitFunc (Custom Blit functions)
#such as for xgalaga-sdl `mkdir -p ~/Downloads/git && cd ~/Downloads/git && https://github.com/frank-zago/xgalaga-sdl.git`
#(successor to SDL_gfxPrimitives):
#dnf -y install SDL2_gfx-devel

#such as for XGalaga++ (C++ rewrite of XGalaga, but still pure X11):
dnf -y install libXpm-devel

#autoconf (including autoreconf etc):
dnf groupinstall "C Development Tools and Libraries"

#configure redshift (location for yourself can be found via Google Maps):
#where 5600 is day temp and 3400 is night temp
#redshift -l 40.3832256:-75.2748652 -t 5600:3400
#Has to remain running, so use GUI instead (drag widget to KDE panel, then right-click to configure:
# * turn on smooth transitions
# * set temps to 5600 and 3400
# * click Locate [if fails, use coords for your location such as above]
# * Apply

#projectM-pulseaudio: a GUI program for viewing audio input using MilkDrop scripts!
# * controlled using hotkeys (see F1 for help, and https://wiki.archlinux.org/index.php/ProjectM)
#

# BLUETOOTH:
# bluez-tools bluez-hid2hci blueman
# blueman pulls in: bluez-obexd (others didn't install anything additional)
# rfkill is not removeable. It was never manually installed (dnf history list rfkill says: "No transaction which manipulates package 'rfkill' was found.") and it can't be removed without removing systemd.
# Doing the above causes KDE to prompt for privs after login for both blueman and RfKill (separate prompt for each)
# Doing the above also results in two bluetooth symbol icons on the task tray (one blurry blue blueman one, plus one themed one)

source_fonts_path=/usr/share/wine/fonts
this_font_name=arial.ttf
this_font_path="$source_fonts_path/$this_font_name"
my_fonts_path=/usr/local/share/fonts/wine
if [ -f "$this_font_path" ]; then
  if [ ! -d "$my_fonts_path" ]; then
    sudo mkdir -p "$my_fonts_path"
  fi
  this_dest_path="$my_fonts_path/$this_font_name"
  if [ ! -f "$this_dest_path" ]; then
    if [ ! -L "$this_dest_path" ]; then
      echo "making symlink to $this_font_path..."
      sudo ln -s "$this_font_path" "$this_dest_path"
    else
      echo "NOTICE: redoing existing symlink $this_dest_path"
      sudo rm -f "$this_dest_path"
      sudo ln -s "$this_font_path" "$this_dest_path"
    fi
  else
    if [ ! -L "$this_dest_path" ]; then
      echo "WARNING: skipping font symlink $this_dest_path which is already a real file"
    else
      echo "NOTICE: redoing existing symlink $this_dest_path"
      sudo rm -f "$this_dest_path"
      sudo ln -s "$this_font_path" "$this_dest_path"
    fi
  fi
else
  echo "WARNING, font not present: $this_font_path"
fi

#also: wine-fonts wine-tahoma-fonts-system wine-times-new-roman-fonts-system wine-wingdings-fonts-system
#wine-*-system: wine font families system integration
#Calibri and Cambria compatible fonts (are installed by default?) respectively are:
sudo dnf -y install google-crosextra-carlito-fonts google-crosextra-caladea-fonts
#Make substitutions in libreoffice (see https://ask.libreoffice.org/en/question/15041/calibri-and-cambria-fonts-in-libreoffice/ which links to https://wiki.debian.org/SubstitutingCalibriAndCambriaFonts):

# * should already be in /etc/fonts/conf.d/
# * but will not work on new documents, only documents created on a computer with Calibri and Cambria
#Rename them (see https://superuser.com/questions/472102/change-font-family-rename-font):
sudo dnf -y install fontforge
# * open fontforge (gui)
if [ ! -d "$HOME/tmp/google-crosextra-carlito-as-calibri" ]; then

  mkdir -p "$HOME/tmp/google-crosextra-caladea-as-cambria"
  cp /usr/share/fonts/google-crosextra-caladea/* "$HOME/tmp/google-crosextra-caladea-as-cambria/"
  cd "$HOME/tmp/google-crosextra-caladea-as-cambria"
  mv Caladea-BoldItalic.ttf Cambria-BoldItalic.ttf
  mv Caladea-Bold.ttf Cambria-Bold.ttf
  mv Caladea-Italic.ttf Cambria-Italic.ttf
  mv Caladea-Regular.ttf Cambria-Regular.ttf

  mkdir -p "$HOME/tmp/google-crosextra-carlito-as-calibri"
  cp /usr/share/fonts/google-crosextra-carlito/* "$HOME/tmp/google-crosextra-carlito-as-calibri/"
  cd "$HOME/tmp/google-crosextra-carlito-as-calibri"
  mv Carlito-BoldItalic.ttf Calibri-BoldItalic.ttf
  mv Carlito-Bold.ttf Calibri-Bold.ttf
  mv Carlito-Italic.ttf Calibri-Italic.ttf
  mv Carlito-Regular.ttf Calibri-Regular.ttf

  # * fontforge "$HOME/tmp/google-crosextra-carlito-as-calibri/"
  # * fontforge "$HOME/tmp/google-crosextra-caladea-as-cambria"
  # * manually change names using fontforge or TTFEdit (java) or fpedit (Windows) from https://www.microsoft.com/typography/property/fpedit.htm
fi
  # * Element, Font Info...
#audacity-freeworld installs audacity with MP3 support
#evince: (aka "Document Viewer") pdf viewer better than okular

#optional
dnf -y install youtube-dl

cd
if [ ! -d "Downloads" ]; then
  mkdir Downloads
fi
wget http://download.brother.com/welcome/dlf006893/linux-brprinter-installer-2.2.0-1.gz
#or get latest from <http://support.brother.com/g/b/downloadhowto.aspx?c=us&lang=en&prod=mfcl2740dw_us_eu_as&os=127&dlid=dlf006893_000&flang=4&type3=625>
gunzip linux-brprinter-installer-2.2.0-1.gz
sudo bash linux-brprinter-installer-2.2.0-1 MFC-L2740DW

sudo dnf groupinstall "Development Tools"
echo "The correct package is `sudo dnf grouplist | grep Development | grep -v "D Development"`"

exit 0
echo "See 'Manually Install' section of this file for additional packages to install."
## obsolete
#gnome-mplayer

## manually install
bluegriffon
zerobrane-studio
gespeaker
tsMuxeR
COLMAP  # (2D to 3D) structure from motion
GeekBench
hardinfo  # System Profiler and Benchmark

### Allow write to device over MTP
(such as phone connected via USB)
```bash
mkdir -p ~/.kde/share/apps/solid/actions
cp /usr/share/kde4/apps/solid/actions/solid_mtp.desktop ~/.kde/share/apps/solid/actions/
nano ~/.kde/share/apps/solid/actions/solid_mtp.desktop
# change Exec=kioclient exec mtp:udi=%i/
# to
# Exec=dolphin "mtp:/"
# as per https://forum.kde.org/viewtopic.php?f=22&t=120685
# which references http://forums.opensuse.org/showthread.php/490795-kde-mtp-device-file-transfer-fix
```

echo "from source:"
echo "kdenlive, openshot, minetest, kivy (see above for dependencies)"
echo
echo "via GUI:"
echo "* For QT 5.* if you face error at Kits, like No Valid Kits Found, go to Options->Build&Run-> then you see a Manual Option which included Desktop as a default. --"
echo "* Set hotkeys for Geany (Edit, Preferences, Keybindings, Format; Ctrl 3 is already 'Send to custom command 3'):"
echo "  * Ctrl Shift 3: comment"
echo "  * Alt Shift 3: uncomment"
echo
echo "see also (installed as dep):"
echo "* python3-mutagen (python module to handle audio meta-data)"
echo
echo "tips:"
echo "* experiment and get good at G'MIC plugins section of gimp filters, because they can also be used in terminal and in other programs: Flowblade, Krita"
