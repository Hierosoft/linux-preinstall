#!/bin/sh
# file_key: hourly
# dest_path: /etc/cron.hourly/iedu-mps-hourly
# post_install: chmod +750 "/etc/cron.hourly/iedu-mps-hourly"
# NOTE: /etc/cron.* folders do NOT EXIST and are not used on systems with systemd (which instead has Timers--see https://wiki.archlinux.org/index.php/Systemd/Timers )
me=`basename "$0"`
if [ `id -u` -ne 0 ]; then
   echo "This script must be run as root"
   sleep 1
   exit 1
fi

customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}


if [ -f /etc/os-release ]; then
  source /etc/os-release
fi

tz_offset=-4
utc_h=`date '+%H'`
local_h=`expr "$utc_h" + "$tz_offset"`
audible_hostname=`hostname`
audible_hostname=${audible_hostname:(-2)}
if [ "`expr substr $audible_hostname 1 1`" = "-" ]; then
  audible_hostname="`expr substr $audible_hostname 2 1`"
fi
integratoredu_url="$1" # "http://login.axlemedia.net/sign"
if [ -z "$integratoredu_url" ]; then
    echo "You must modify $me so integratoredu_url is your integratoredu instance."
    exit 1
fi
text_req_url="$integratoredu_url/cppr"
CONFIGS_PATH="/etc/iedu"
EVERYONE_PATH="$CONFIGS_PATH/everyone"
SIGNALS_PATH="$CONFIGS_PATH/everyone"
LOGS_PATH="/var/log/iedu"
LOCKS_PATH="/var/lock/iedu"
LOG_PATH="$LOGS_PATH/log.$me"
LOCK_PATH="$LOCKS_PATH/$me.lock"
#DATE=`date '+%Y-%m-%d %H:%M:%S'`
DATE=`date '+%Y-%m-%d '`
DATE="$DATE $local_h"
DATE="$DATE`date '+:%M:%S'`"
echo $DATE

LOCAL_USER=student
lu_path="$EVERYONE_PATH/local_user"
if [ -f "$lu_path" ]; then
  this_lu="`head -n 1 $lu_path`"
  if [ ! -z "$this_lu" ]; then
    LOCAL_USER="$this_lu"
  fi
fi
LU_HOME="/home/$LOCAL_USER"
lh_path="$EVERYONE_PATH/local_home"
if [ -f "$lh_path" ]; then
  this_lp="`head -n 1 $lh_path`"
  if [ ! -z "$this_lp" ]; then
    LU_HOME="$this_lp"
  fi
fi

if [ ! -d "$CONFIGS_PATH" ]; then
  mkdir "$CONFIGS_PATH"
fi
if [ ! -d "$EVERYONE_PATH" ]; then
  mkdir "$EVERYONE_PATH"
  chmod 777 "$EVERYONE_PATH"
fi
if [ ! -d "$LOGS_PATH" ]; then
  mkdir "$LOGS_PATH"
fi
if [ ! -d "$LOCKS_PATH" ]; then
  mkdir "$LOCKS_PATH"
fi
if [ -f "$LOCK_PATH" ]; then
  # running_time=`cat "$LOCK_PATH"`
  running_time=$(head -n 1 "$LOCK_PATH")
  msg="WARNING $DATE: Nothing done since already running '$me' since $running_time"
  echo "$msg"
  echo "$msg" > "$LOG_PATH"
  msg="  if lock is stale, and you're really sure it isn't running, try:"
  echo "$msg"
  echo "$msg" >> "$LOG_PATH"
  msg="  rm -f $LOCK_PATH"
  echo "$msg"
  echo "$msg" >> "$LOG_PATH"
  exit 1
  # NOTE: default for "$LOG_PATH" in this situation is 744
else
  if [ -f "$LOG_PATH" ]; then
    rm -f "$LOG_PATH"
  fi
fi
echo "$DATE" > "$LOCK_PATH"

audible_hostname_path="$CONFIGS_PATH/audible_hostname"
audible_hostname=`hostname`
if [ -f "$audible_hostname_path" ]; then
  audible_hostname="`cat "$audible_hostname_path"`"
else
  audible_hostname=${audible_hostname:(-2)}
  hyphen_audible_hostname=${audible_hostname:(-3)}
  if [ "`expr substr $audible_hostname 1 1`" = "-" ]; then
    audible_hostname="`expr substr $audible_hostname 2 1`"
  elif [ "`expr substr $hyphen_audible_hostname 1 1`" != "-" ]; then
    # computer name does not end in -?? nor -? so use full name for text-to-speech:
    audible_hostname=`hostname`
  fi
  echo "$audible_hostname" > "$audible_hostname_path"
fi

install_bin="dnf install -y"
remove_bin="dnf remove -y"
updates_cmd="dnf upgrade -y"
list_installed_cmd="dnf list installed"
p3tk="python3-tkinter"
if [ -f "`command -v pacman`" ]; then
  install_bin="pacman -Syyu --noconfirm"
  remove_bin="pacman -R --noconfirm"
  updates_cmd="pacman -Syyu --noconfirm"
  list_installed_cmd="pacman -Q"  # Qe lists packages explicitly installed (see pacman -Q --help)
  p3tk="tk"  # python-tkinter is an integral part of python in arch
fi
if [ -f "`command -v apt`" ]; then
  install_bin="apt install -y"
  remove_bin="apt remove -y"
  updates_cmd="apt upgrade"
  list_installed_cmd="apt list --installed"
  p3tk="python3-tk"
  # and update cache immediately since using a dependency resolver with non-smart cache
  apt update
fi
echo
echo "[ $me ] using package manager command: $install_bin"
echo
echo
if [ ! -f "`command -v wget`" ]; then
  $install_bin wget
fi

#if [ ! -f "/usr/lib64/flash-plugin/libflashplayer.so" ]; then
#  rpm -ivh http://linuxdownload.adobe.com/adobe-release/adobe-release-x86_64-1.0-1.noarch.rpm
#  rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-adobe-linux
#  dnf -y install flash-plugin
#fi

if [ ! -f /etc/pki/rpm-gpg/RPM-GPG-KEY-adobe-linux ]; then
  rpm -ivh http://linuxdownload.adobe.com/adobe-release/adobe-release-x86_64-1.0-1.noarch.rpm
  rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-adobe-linux
fi
if [ ! -f "/usr/lib64/flash-plugin/libflashplayer.so" ]; then
  dnf -y install flash-plugin
fi
#for Chromium (v31 as of 2018--release version on get.adobe.com/flashplayer is also 31):
if [ ! -f "/usr/lib64/flash-plugin/libpepflashplayer.so" ]; then
  dnf -y install flash-player-ppapi
fi
if [ ! -d ~/Downloads ]; then
  mkdir ~/Downloads
fi
cd ~/Downloads
name=flash_player_ppapi_linux.x86_64.tar.gz
lcb=/usr/lib64/chromium-browser
lcbp=$lcb/PepperFlash
if [ -d "$lcbp" ]; then
  if [ ! -f "$lcbp/libpepflashplayer.so" ]; then
    if [ ! -f "$name" ]; then
      wget https://fpdownload.adobe.com/pub/flashplayer/pdc/31.0.0.122/$name
    fi
    cd "$lcbp"
    tar -xf "$HOME/Downloads/$name"
    echo "Extracted to $lcbp:"
    ls "$lcbp"
  else
    echo "Already installed: $lcbp"
  fi
else
  echo "Skipping Chromium plugin since missing $lcbp"
fi
cd ~/Downloads


if [ ! -f "`command -v xterm`" ]; then
  dnf -y install xterm
fi

updates_enable="false"
#if [ "$local_h" -lt "8" ]; then
#  updates_enable="true"
#  # NOTE: will only happen once a day--see $date_s further down
#elif [ "$local_h" -gt "15" ]; then
if [ "$local_h" -gt "15" ]; then
  #if [ "`date '+%M'`" -gt "5" ]; then
    #M: minute
    #m: month
    updates_enable="true"
  #fi
fi
#if [ "$local_h" -gt "15" ]; then
#  if [ "`date '+%M'`" -gt "28" ]; then
#    #if [ "`date '+%u'`" -gt "6" ]; then  # for %u (1-7), 1 is Monday (see also man date)
#      if [ "`date '+%u'`" -lt "2" ]; then  # for %u (1-7), 1 is Monday (see also man date)
#        #M: minute
#        #m: month
#        updates_enable="true"
#      fi
#    #fi
#  fi
#fi

if [ -f "`command -v pacman`" ]; then
  # to update arch-based distros can be long&overkill so no automation:
  updates_enable="false"
fi

if [ "$updates_enable" = "true" ]; then
  date_s="`date '+%Y-%m-%d'`"
  update_date_path=$CONFIGS_PATH/update_date
  #NOTE: below (espeak) does NOT work unless runs under logged-in session
  #if not already updated via this script today:
  if [ ! -f "$update_date_path" ] || [ "`cat $update_date_path`" != "$date_s" ]; then
    echo "$date_s" > "$update_date_path"

    #first update flatpak and packages its post-install scriptlet uses, to avoid permanent freeze on Fedora 27 (see <https://bugzilla.redhat.com/show_bug.cgi?id=1599332>)
    $updates_cmd flatpak
    $updates_cmd --refresh
    $updates_cmd systemd
    $updates_cmd --refresh
    $updates_cmd dbus
    $updates_cmd --refresh
    $updates_cmd dbus flatpak systemd

    $updates_cmd
    #if [ "`date '+%u'`" -gt "6" ]; then  # for %u (1-7), 1 is Monday (see also man date)
    if [ "`date '+%u'`" -lt "2" ]; then  # for %u (1-7), 1 is Monday (see also man date)
      if [ -f "command -v espeak" ]; then
        espeak "Restarting computer $audible_hostname in 20 seconds"
      fi
      sleep 10
      if [ -f "command -v espeak" ]; then
        espeak "Restarting computer $audible_hostname in 10 seconds"
      fi
      sleep 5
      if [ -f "command -v espeak" ]; then
        espeak "Restarting computer $audible_hostname in 5 seconds"
      fi
      sleep 5
      if [ -f "/usr/local/bin/minetest" ]; then
        # force update from git:
        rm -f "/usr/local/bin/minetest"
      fi
      reboot
    fi
    #fi


  fi
fi

tmp=`id -u student`
# stated_username:
su_path="/etc/iedu/everyone/iedugear-last-user"
url_suffix="&unit=0&kernel=linux&access_level=root&hostname=`hostname`&username=$USER"
mgn_path="$CONFIGS_PATH/machine_group"
if [ -f "$CONFIGS_PATH/machine_group_name" ]; then
  # move deprecated file
  if [ ! -f "$mgn_path" ]; then
    mv -f "$CONFIGS_PATH/machine_group_name" "$mgn_path"
  else
    rm -f "$CONFIGS_PATH/machine_group_name"
  fi
fi
if [ -f "$mgn_path" ]; then
  url_suffix="$url_suffix&machine_group=`head -n 1 "$mgn_path"`"
else
  url_suffix="$url_suffix&machine_group=StudentMachines"
fi
MAC=`ip addr | grep link/ether | awk '{print $2}'`
# TODO: process $MAC; $MAC may now contain space-separated values (one value per network card); remove ':'
if [ -f "$su_path" ]; then
  # NOTE: must use double quotes inside grave accents with cat, or cat will wait for input if variable value is blank
  url_suffix="$url_suffix&stated_username=`head -n 1 "$su_path"`"
fi

if [ ! -z "$LOCAL_USER" ]; then
  url_suffix="$url_suffix&local_username=$LOCAL_USER"
fi
if [ -z "$tmp" ]; then
  adduser --password student12 --create-home student
else
  echo "student12" | passwd student --stdin
fi

msg="installing packages..."
echo "$msg"
echo "$msg" >> "$LOCK_PATH"
if [ ! -f "`command -v libreoffice`" ]; then
  # there is only one binary for libreoffice (run writer like libreoffice --writer)
  $install_bin libreoffice
fi
if [ ! -f "`command -v blender`" ]; then
  $install_bin blender
fi

installed_package_tkinter=`$list_installed_cmd | grep $p3tk`
# TODO: find a way to check for tkinter, such as emitting a trivial python script
# NOTE: python2-tkinter is a dep of something in this list already and was installed before adding this section
if [ -z "$installed_package_tkinter" ]; then
  $install_bin $p3tk
fi
if [ ! -f "`command -v FreeCAD`" ]; then
  #command is FreeCAD, but package is all lowercase
  $install_bin freecad
fi
if [ ! -f "`command -v audacity`" ]; then
  $install_bin audacity
fi
if [ ! -f "`command -v gedit`" ]; then
  $install_bin gedit
fi
if [ ! -f "`command -v stage`" ]; then
  $install_bin stage
fi
if [ ! -f "`command -v gimp`" ]; then
  $install_bin gimp
fi
if [ ! -f "`command -v lmms`" ]; then
  $install_bin lmms
fi
if [ ! -f "`command -v geany`" ]; then
  $install_bin geany
fi
if [ ! -f "`command -v python2`" ]; then
  $install_bin python2
fi
if [ ! -f "`command -v python3`" ]; then
  $install_bin python3
fi
if [ ! -f "`command -v smbclient`" ]; then
  $install_bin samba
  # TODO: on CentOS, install via pkg install samba-smbclient
fi
if [ ! -f "`command -v xdotool`" ]; then
  $install_bin xdotool
  # TODO: on CentOS, install via pkg install samba-smbclient
fi

if [ ! -f "`command -v java`" ]; then
# see https://fedoraproject.org/wiki/NetBeans
  $install_bin java-1.8.0-openjdk
  #cd /tmp
  # official installer is a GUI installer and says no jdk found after installing java-1.8.0-openjdk even if path is specified
  #wget http://download.netbeans.org/netbeans/8.2/final/bundles/netbeans-8.2-javase-linux.sh
  # sh netbeans-8.2-javase-linux.sh
fi
if [ ! -d "/usr/lib/jvm/java-openjdk" ]; then
  $install_bin java-1.8.0-openjdk-devel
fi
#TODO: calligra package AND binary naming is DIFFERENT on Ubuntu Xenial: see below
# if [ ! -f "`command -v calligrastage`" ]; then
  # $install_bin calligra
# fi

#if [ ! -f "`command -v minetest`" ]; then
#  $install_bin minetest
#fi

if [ ! -f "`command -v librecad`" ]; then
  $install_bin librecad
fi

try_file=$LU_HOME/Desktop/setup-integratoredu-policy.sh
if [ -f "$try_file" ]; then
  rm -f "$try_file"
fi

cd /tmp
# update the OTHER script:
src_name="daily"
cron_freq="daily"
msg="updating $src_name"
echo "$msg"
echo "$msg" >> "$LOCK_PATH"
local_name="iedu-mps-$src_name"
THIS_TRUE="true"
# don't state the good flag literally, or it will be read as a good flag
# (integratoredu webapp should automatically append the value of good_flag to the end as a comment)
good_flag="update_enable: $THIS_TRUE"

install_mp_file()
{
    dest_path=$1
    file_key=$2
    permissions_octal=$3
    ln_dest_path=$4
    cd /tmp
    local_name=$file_key
    wget --output-document="$local_name" "$text_req_url?file_key=$file_key$url_suffix"
    if grep -q "$good_flag" "$local_name"; then
      mv -f "$local_name" "$dest_path"
      if [ -f "$dest_path" ]; then
        echo "moved to $dest_path"
        if [ ! -z "$ln_dest_path" ]; then
          ln -s "$dest_path" "$ln_dest_path"
        fi
      else
        msg="ERROR: failed to move $local_name to $dest_path"
        echo $msg
        echo $msg > $LOG_PATH
        rm -f "$local_name"
      fi
    else
      echo "ERROR: not using $local_name since not downloaded properly (no $good_flag in):"
      cat "$local_name"
      rm -f "$local_name"
    fi
    if [ ! -z "$permissions_octal" ]; then
      chmod $permissions_octal "$dest_path"
    fi
}

install_mp_file "/etc/cron.$cron_freq/iedu-mps-$src_name" $src_name 750

# LAST, install netbeans (this is the big one)
SHORTCUT_NAME="netbeans-8.2.desktop"
if [ ! -f "`command -v netbeans`" ]; then
  echo "installing netbeans (this may take a while)..." >> "$LOCK_PATH"
  # must already have:
  # $install_bin java-1.8.0-openjdk
  # $install_bin java-1.8.0-openjdk-devel

  # SHORTCUT HIDES--see:
  #   /root/Desktop/netbeans-8.2.desktop
  # unless installer was run as current user,

  # icon is: /usr/local/netbeans-8.2/nb/netbeans.png

  cd /tmp
  # find existing binary stuff (and other unrelated stuff):
  # locate netbeans | grep -v incubator | grep -v .jar | grep -v .xml | grep -v profiler | grep -v platform | grep -v websvc | grep -v docs | grep -v javafx | grep -v mavan | grep -v modules | grep -v harness | grep -v nativeex | grep -v Windows2 | grep -v extide | grep -v maven
  # echo "NOTE: oracle only provides interactive graphical installer"



  # see also version-specific SHORTCUT_NAME above
  SRC_INSTALLER_NAME="netbeans-8.2-javase-linux.sh"
  SRC_INSTALLER_PATH="$SRC_INSTALLER_NAME"

  if [ -f "$SRC_INSTALLER_NAME" ]; then
    rm -f "$SRC_INSTALLER_NAME"
  fi
  wget http://download.netbeans.org/netbeans/8.2/final/bundles/$SRC_INSTALLER_NAME
  chmod +x $SRC_INSTALLER_NAME
  if [ -d "$LU_HOME" ]; then
  # for fault-tolerance (since can be installed in user space, let user run it--clicking it will work in KDE):
    DLS_PATH="$LU_HOME/Downloads"
    if [ ! -d "$DLS_PATH" ]; then
      mkdir "$DLS_PATH"
      chown $LOCAL_USER "$DLS_PATH"
    fi
    if [ ! -f "$LU_HOME/Downloads/$SRC_INSTALLER_NAME" ]; then
      DEST_INSTALLER_PATH="$DLS_PATH/$SRC_INSTALLER_NAME"
      cp "$SRC_INSTALLER_PATH" "$DEST_INSTALLER_PATH"
      chown $LOCAL_USER "$DEST_INSTALLER_PATH"
      chmod +x "$DEST_INSTALLER_PATH"
    fi
  else
    echo "WARNING: missing $LU_HOME (maybe put username in one-line file $EVERYONE_PATH/local_home)"
  fi
  echo "Running oracle NetBeans shell script installer with --silent option (this may take a while)..."
  ./$SRC_INSTALLER_PATH --silent
  echo "Done installing NetBeans"
  # version below doesn't work with jdk-1.8.0-openjdk-devel (see note at bottom)
  #echo "find the link to the latest incubator build on https://builds.apache.org/job/incubator-netbeans-linux/"
  # if [ -f "`command -v java`" ]; then
    # $remove_bin netbeans
  # fi
  # install devel as per https://ask.fedoraproject.org/en/question/59236/netbeans-8-wont-install-on-fedora-21/
  # wget https://builds.apache.org/job/incubator-netbeans-linux/lastSuccessfulBuild/artifact/nbbuild/NetBeans-dev-incubator-netbeans-linux-337-on-20180130-basic.zip
  # unzip NetBeans-dev-incubator-netbeans-linux-337-on-20180130-basic.zip
  # if [ -d incubator ]; then rm -Rf incubator; fi
  # mv netbeans incubator
  # mkdir -p /usr/local/share/netbeans
  # mv incubator /usr/local/share/netbeans/
  # chmod 751 /usr/local/share/netbeans/incubator/bin/netbeans
  # ln -s /usr/local/share/netbeans/incubator/bin/netbeans /usr/local/bin/netbeans
  # chmod 751 /usr/local/bin/netbeans
  # --still has lang exceptions when trying to run a sample program
  if [ ! -f "/usr/local/bin/netbeans" ]; then
    ln -s /usr/local/netbeans-8.2/bin/netbeans /usr/local/bin/netbeans
  fi
  # touch /etc/netbeans.conf
  # echo 'netbeans_jdkhome="/usr/lib/jvm/java-openjdk"' >> /etc/netbeans.conf
  # NOTE: default in 8.2 is `netbeans_jdkhome="/usr"` for some reason (prevents it from working--has error that it can't find jdk)
  good_line='netbeans_jdkhome="/usr/lib/jvm/java-openjdk"'
  conf_path='/usr/local/netbeans-8.2/etc/netbeans.conf'
  if [ -f "$conf_path" ]; then
    if grep -q "$good_line" "$local_name"; then
      echo "already set $good_line"
    else
      echo "$good_line" >> $conf_path
    fi
  else
    echo "ERROR: NetBeans is missing $conf_path"
  fi
  # NOTE: uninstall is (where value for LOCAL_USER is set to your username instead of student:
  # chmod +x /usr/local/netbeans-8.2/uninstall.sh
  # /usr/local/netbeans-8.2/uninstall.sh --silent
  rm -Rf $LU_HOME/.cache/netbeans
  rm -Rf $LU_HOME/.netbeans
  # in case ran as non-root:
  good_line='netbeans_jdkhome="/usr/lib/jvm/java-openjdk"'
  conf_path="$HOME/netbeans-8.2/etc/netbeans.conf"
  if [ -f "$conf_path" ]; then
    if grep -q "$good_line" "$local_name"; then
      echo "already set $good_line"
    else
      echo "$good_line" >> $conf_path
    fi
  else
    echo "NOTE: ignoring missing $conf_path since installed as root apparently"
  fi
  if [ ! -f "$HOME/Desktop/$SHORTCUT_NAME" ]; then
    echo "ERROR: Installer failed to create $HOME/Desktop/$SHORTCUT_NAME (maybe netbeans-install.sh is looking for the wrong shortcut)"
    # rm -f "$LOCK_PATH"
    # exit 1
  fi
fi

if [ ! -f "$LU_HOME/Desktop/$SHORTCUT_NAME" ]; then
  if [ -d "$LU_HOME" ]; then
    # if [ ! -f "$LU_HOME/Desktop/$SHORTCUT_NAME" ]; then
      if [ -f "$HOME/Desktop/$SHORTCUT_NAME" ]; then
        cp "$HOME/Desktop/$SHORTCUT_NAME" "$LU_HOME/Desktop/"
        chown root "$LU_HOME/Desktop/$SHORTCUT_NAME"
        chgrp root "$LU_HOME/Desktop/$SHORTCUT_NAME"
        chmod 755 "$LU_HOME/Desktop/$SHORTCUT_NAME"
      fi
    # fi
  else
    echo "WARNING: missing $LU_HOME (maybe put username in one-line file $CONFIGS_PATH/local_home)"
  fi
fi
msg="updating iedu components..."
echo "$msg"
echo "$msg" >> "$LOCK_PATH"

if [ ! -f "`command -v clamscan`" ]; then
  $install_bin clamav
fi

if [ ! -f "`command -v freshclam`" ]; then
  $install_bin clamav-update
fi

if [ ! -f "`command -v zbstudio`" ]; then
  # ZeroBrane Studio
  cd
  if [ ! -d Downloads ]; then
  mkdir Downloads
  fi
  cd Downloads
  SRC_INSTALLER_NAME="ZeroBraneStudioEduPack-1.70-linux.sh"
  wget -O $SRC_INSTALLER_NAME https://download.zerobrane.com/$SRC_INSTALLER_NAME
  chmod +x $SRC_INSTALLER_NAME
  ./$SRC_INSTALLER_NAME
  # NOTE: uninstall is `zbstudio-uninstall`
  rm $SRC_INSTALLER_NAME
fi

IEDU_DIR=/usr/local/lib/iedu
if [ ! -d "$IEDU_DIR" ]; then
  mkdir "$IEDU_DIR"
fi

# must be able to READ to run py files (not just execute):
install_mp_file "$IEDU_DIR/lankycrypt.py" "lankycrypt_py" 755
install_mp_file "$IEDU_DIR/iedusign.py" "iedusign_py" 755
install_mp_file "$IEDU_DIR/iedu-user-logout.sh" "iedu_user_logout_sh" 755
# NOTE: *iedu-user-start.sh CREATES* symlink to above DURING LOGIN so above is placed in EVERY user's KDE shutdown script folder:
#/etc/profile.d/* files need no permission change--644 with owner root is ok
install_mp_file "/etc/profile.d/iedu-user-start.sh" "iedu_user_start" 644
local_name=iedu-sign.desktop
dest_path="/usr/local/share/applications/$local_name"
if [ -f "$LU_HOME/Desktop/iedu_sign_desktop" ]; then
  rm "$LU_HOME/Desktop/iedu_sign_desktop"
fi
install_mp_file $dest_path "iedu_sign_desktop" 755 "$LU_HOME/Desktop/$local_name"
if [ -f "$dest_path" ]; then
  #make iedusign autostart AFTER desktop loads:
  $start_files_path=$LU_HOME/.config/autostart
  if [ ! -d "$start_files_path" ]; then
    mkdir -p "$start_files_path"
  fi
  $start_path=$start_files_path/$local_name
  if [ ! -f $start_path ]; then
    ln -s "$dest_path" "$start_path"
  fi
#else error already shown by install_mp_file
fi

install_mp_file "$IEDU_DIR/terminate-by-title" "terminate_by_title" 755
install_mp_file "$IEDU_DIR/network-attach" "attach" 750
install_mp_file "$IEDU_DIR/network-detach" "detach" 750
install_mp_file "$CONFIGS_PATH/iedugear.conf" "iedugear_conf" 750
#install_mp_file "$IEDU_DIR/iedugear.py" "iedugear_py" 750

cd /tmp
local_name=iedugear.py
file_key="iedugear_py"
# local_pid=`pgrep -f iedugear.py`  # will give you its pid
dest_path="$IEDU_DIR/$local_name"
iedugear_path="$dest_path"  # used further down
wget --output-document="$local_name" "$text_req_url?file_key=$file_key$url_suffix"
restart_gear_enable="false"
if grep -q "$good_flag" "$local_name"; then
  if [ ! -f "$dest_path" ] || [ ! -z "`diff "$local_name" "$dest_path"`" ]; then
    restart_gear_enable="true"
    if [ ! -d "/etc/systemd" ]; then
      pkill -9 -f iedugear.py  # kills the matching pid
    else
      if [ -f /etc/systemd/system/iedugear.service ]; then
        systemctl stop iedugear.service
      else
        # service is needed but was not installed yet, so kill process
        pkill -9 -f iedugear.py  # kills the matching pid
      fi
    fi
    mv -f "$local_name" "$dest_path"
    echo "moved to $dest_path"
  else
    echo "$local_name is already up to date."
    rm -f "$local_name"
  fi
else
  echo "ERROR: not using $local_name since not downloaded properly (no $good_flag in):"
  cat "$local_name"
  rm -f "$local_name"
fi
# should ONLY run as root:
chmod 750 "$dest_path"


if [ -d /etc/systemd ]; then
  cd /tmp
  local_name=iedugear.service
  file_key="iedugear_service"
  dest_path="/etc/systemd/system/$local_name"
  #service_enable_enable="false"
  #if [ ! -f "$dest_path" ]; then
  #  service_enable_enable="true"
  #fi
  wget --output-document="$local_name" "$text_req_url?file_key=$file_key$url_suffix"
  if grep -q "$good_flag" "$local_name"; then
    if [ ! -f "$dest_path" ] || [ ! -z "`diff "$local_name" "$dest_path"`" ]; then
      if [ "$restart_gear_enable" != "true" ]; then
        # must restart service when .service file changes even if process does not
        systemctl stop iedugear.service
        restart_gear_enable="true"
      fi
      mv -f "$local_name" "$dest_path"
      echo "moved to $dest_path"
    else
      echo "$local_name is already up to date"
      rm -f "$local_name"
    fi
  else
    echo "ERROR: not using $local_name since not downloaded properly (no $good_flag in):"
    cat "$local_name"
    rm -f "$local_name"
  fi
  if [ "$restart_gear_enable" == "true" ]; then
    if [ -f "$dest_path" ]; then
      chmod 644 $dest_path
      systemctl daemon-reload
      systemctl enable iedugear.service
      systemctl start iedugear.service
    else
      echo "WARNING: $dest_path is not present after update attempt"
    fi
  fi
  if [ -f "/etc/init.d/$local_name" ]; then
    # init.d is not used on systems with systemd, so remove old file:
    rm -f "/etc/init.d/$local_name"
  fi
else
  cd /tmp
  local_name=iedu-machine-init.sh
  file_key="iedu_machine_init"
  dest_path="/etc/init.d/$local_name"
  wget --output-document="$local_name" "$text_req_url?file_key=$file_key$url_suffix"
  if grep -q "$good_flag" "$local_name"; then
    mv -f "$local_name" "$dest_path"
    echo "moved to $dest_path"
  else
    echo "ERROR: not using $local_name since not downloaded properly (no $good_flag in):"
    cat "$local_name"
    rm -f "$local_name"
  fi
  if [ -f "$dest_path" ]; then
    chmod 750 "$dest_path"
  else
    echo "WARNING: $dest_path is not present after update attempt"
  fi
  if [ "$restart_gear_enable" == "true" ]; then
    if [ -f "$iedugear_path" ]; then
      nohup python3 $iedugear_path > /dev/null 2>&1 &
    fi
  fi
fi

cd
if [ ! -d "Downloads" ]; then
  mkdir Downloads
fi
git_minetest_path=/usr/local/bin/minetest
git_minetest_date=""
if [ -f "$git_minetest_path" ]; then
  MODDATE=$(stat -c %y $git_minetest_path)
  git_minetest_date=${MODDATE%% *}
fi
if [ -f "`command -v dnf`" ]; then
  # switch to git version of minetest:
  installed_package_minetest=`$list_installed_cmd | grep minetest | grep -v minetestserver`
  if [ ! -z "$installed_package_minetest" ]; then
    $remove_bin minetest
  fi
  installed_package_minetestserver=`$list_installed_cmd | grep minetestserver`
  build_what="-DBUILD_SERVER=off -DBUILD_CLIENT=on"
  if [ ! -z "$installed_package_minetestserver" ]; then
    $remove_bin minetestserver
    build_what="-DBUILD_SERVER=on -DBUILD_CLIENT=on"
  fi
  if [ -f "$git_minetest_path" ]; then
    if [ "$git_minetest_date" = "2018-04-02" ]; then
      rm "$git_minetest_path"
    fi
  fi
  if [ -f "`command -v minetestserver`" ]; then
    build_what="-DBUILD_SERVER=on -DBUILD_CLIENT=on"
  fi
  if [ ! -f "`command -v minetest`" ]; then
    # packaged version is gone, and compiled version was not found, so compile:
    $install_bin git

    #region based on one-line install
    $install_bin doxygen luajit-devel jsoncpp-devel freetype-devel postgresql-devel spatialindex-devel gcc-c++ irrlicht-devel gettext freetype cmake bzip2-devel libpng libjpeg-turbo libXxf86vm mesa-libGLU libsqlite3x-devel libogg-devel libvorbis-devel openal-devel curl-devel luajit-devel lua-devel leveldb-devel ncurses-devel redis hiredis-devel gmp-devel
    cd
    #git clone https://github.com/minetest/minetest.git
    #cd minetest/games
    #git clone https://github.com/minetest/minetest_game.git
    #cd ..
    #cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1
    #make -j$(nproc)
    #sudo make install
    #minetest
    #echo -e "\n\n\e[1;33mYou can run Minetest again by typing \"minetest\" in a terminal or selecting it in an applications menu.\nYou can install mods in ~/.minetest/mods, too.\e[0m"
    #endregion based on one-line install

    cd ~/Downloads
    if [ ! -d minetest ]; then
      git clone https://github.com/minetest/minetest.git
      cd minetest
      cd games
      git clone https://github.com/minetest/minetest_game.git
      cd ../
    else
      cd minetest
      git pull
      cd games
      if [ -d minetest_game ]; then
        cd minetest_game
        git pull
        cd ..
      else
        git clone https://github.com/minetest/minetest_game.git
      fi
      cd ../
    fi

    #get client with protocol version 36 since server only supports up to 36
    #cd ..
    GOOD_SHA1=d6f2a1c4
    if [ -d "minetest-$GOOD_SHA1" ]; then
      rm -Rf minetest-$GOOD_SHA1
    fi
    #mkdir minetest-$GOOD_SHA1
    #cd minetest-$GOOD_SHA1
    #git init
    #git remote add origin https://github.com/minetest/minetest
    #git fetch origin $GOOD_SHA1
    #git reset --hard FETCH_HEAD
    #cd games
    #git clone https://github.com/minetest/minetest_game
    #cd ..

    #from one-liner:
    #cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1 -DENABLE_REDIS=1
    #from EnlivenMinetest:
    #cmake . -DENABLE_GETTEXT=on -DENABLE_CURSES=on -DENABLE_FREETYPE=on -DENABLE_LEVELDB=on -DENABLE_CURL=on -DENABLE_GETTEXT=on -DENABLE_REDIS=on -DENABLE_POSTGRESQL=on -DRUN_IN_PLACE=off -DCMAKE_BUILD_TYPE=Release $build_what
    cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1 -DENABLE_REDIS=1 -DRUN_IN_PLACE=off -DCMAKE_BUILD_TYPE=Release $build_what
    make -j$(nproc)
    killall minetest
    make install
  fi
elif [ -f "`command -v apt`" ]; then
  # switch to git version of minetest:
  installed_package_minetest=`$list_installed_cmd | grep minetest | grep -v minetestserver`
  if [ ! -z "$installed_package_minetest" ]; then
    $remove_bin minetest
  fi
  installed_package_minetestserver=`$list_installed_cmd | grep minetestserver`
  build_what="-DBUILD_SERVER=off -DBUILD_CLIENT=on"
  if [ ! -z "$installed_package_minetestserver" ]; then
    $remove_bin minetestserver
    build_what="-DBUILD_SERVER=on -DBUILD_CLIENT=on"
  fi
  if [ -f "$git_minetest_path" ]; then
    if [ "$git_minetest_date" = "2018-04-02" ]; then
      rm "$git_minetest_path"
    fi
  fi
  if [ -f "`command -v minetestserver`" ]; then
    build_what="-DBUILD_SERVER=on -DBUILD_CLIENT=on"
  fi

  if [ ! -f "`command -v minetest`" ]; then
    #echo "WARNING: minetest compiling is not scripted for package manager '$install_bin'"
    #$install_bin git
    $install_bin build-essential cmake git libirrlicht-dev libbz2-dev libgettextpo-dev libfreetype6-dev libpng12-dev libjpeg8-dev libxxf86vm-dev libgl1-mesa-dev libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libhiredis-dev libcurl3-dev
    cd ~/Downloads
    if [ -d minetest-d6f2a1c4 ]; then
      #I'm not sure why this was here...
      rm -Rf minetest-d6f2a1c4
    fi
    if [ ! -d minetest ]; then
      echo "* cloning minetest..."
      git clone https://github.com/minetest/minetest.git
      cd minetest
      cd games
      echo "* cloning minetest_game..."
      git clone https://github.com/minetest/minetest_game.git
      cd ../
    else
      cd minetest
      echo "* pulling `pwd`..."
      git pull
      cd games
      if [ -d minetest_game ]; then
        cd minetest_game
        echo "* pulling `pwd`..."
        git pull
        cd ..
      else
        git clone https://github.com/minetest/minetest_game.git
      fi
      cd ../
    fi
    #from one-liner:
    #cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1 -DENABLE_REDIS=1
    #from EnlivenMinetest:
    #cmake . -DENABLE_GETTEXT=on -DENABLE_CURSES=on -DENABLE_FREETYPE=on -DENABLE_LEVELDB=on -DENABLE_CURL=on -DENABLE_GETTEXT=on -DENABLE_REDIS=on -DENABLE_POSTGRESQL=on -DRUN_IN_PLACE=off -DCMAKE_BUILD_TYPE=Release $build_what
    cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1 -DENABLE_REDIS=1 -DRUN_IN_PLACE=off -DCMAKE_BUILD_TYPE=Release $build_what
    #make -j$(grep -c processor /proc/cpuinfo)
    make -j$(nproc)
    echo "* done make in `pwd`..."
    killall minetest
    sudo make install
  fi
else
    echo "WARNING: minetest compiling is not scripted for package manager '$install_bin'"
fi


# value for ip was obtained via ip -6 addr
# TODO: set username to stated username; leave shortcut keys intact (?)
mt_runs="`ps -e | grep minetest`"
if [ -z "$mt_runs" ]; then
  if [ -d /home/$LOCAL_USER ]; then
    if [ ! -d /home/$LOCAL_USER/.minetest ]; then
      mkdir /home/$LOCAL_USER/.minetest
      chown $LOCAL_USER /home/$LOCAL_USER/.minetest
    fi
    install_mp_file /home/$LOCAL_USER/.minetest/minetest.conf minetest_conf 644
  fi
#else refrain from corrupting minetest.conf (corrupts if changed while running)
fi

if [ -f "`command -v dnf`" ]; then
  if [ ! -d "$HOME/Downloads" ]; then
    mkdir "$HOME/Downloads"
  fi
  cd ~/Downloads
  rpm_name=rpmfusion-free-release-$VERSION_ID.noarch.rpm
  installed_package_rpmfusion=`$list_installed_cmd | grep rpmfusion-free-release`
  if [ -z "$installed_package_rpmfusion" ]; then
    if [ ! -f "$rpm_name" ]; then
      wget https://download1.rpmfusion.org/free/fedora/$rpm_name
    fi
    rpm -i $rpm_name
  fi
  rpm_name=rpmfusion-nonfree-release-$VERSION_ID.noarch.rpm
  if [ ! -f "$rpm_name" ]; then
    wget https://download1.rpmfusion.org/nonfree/fedora/$rpm_name
    rpm -i $rpm_name
  fi
fi
exfat_enable="false"
#if [ -f "/usr/sbin/mount.exfat" ]; then
  # Fedora etc non-fuse version
#  exfat_enable="true"
if [ -f "/usr/sbin/mount.exfat-fuse" ]; then
  # Fedora etc
  exfat_enable="true"
elif [ -f "/sbin/mount.exfat-fuse" ]; then
  # Ubuntu Xenial etc
  exfat_enable="true"
fi

if [ "$exfat_enable" = "false" ]; then
  # NOTE: requires rpmfusion repo above IF using rpm-based distro
  $install_bin fuse-exfat
  $install_bin exfat-utils
  exfat_enable="true"
fi

#NOTE: there is also

if [ ! -f "`command -v vlc`" ]; then
  # NOTE: requires rpmfusion repo above
  $install_bin vlc
fi

# on Fedora, package is chromium, but command is chromium-browser:
if [ ! -f "`command -v chromium-browser`" ]; then
  dnf -y install chromium
fi
#AND MP4 & other media formats for Chromium (included in Chrome but not Chromium!):
this_pkg="chromium-libs-media-freeworld"
#if rpm -q $this_pkg
#then
#    echo "$this_pkg installed"
#else
#    echo "Installing $this_pkg..."
#fi
installed_pkg_clmf=`$list_installed_cmd | grep $this_pkg`
if [ -z "$installed_pkg_clmf" ]; then
# if [ ! -f "/usr/lib64/chromium-browser/libmedia.so.freeworld" ]; then
    echo "Installing $this_pkg (MP4 support for Chromium)..."
    $install_bin $this_pkg
fi


echo "removing lock..."
rm -f "$LOCK_PATH"
echo "used $url_suffix"
echo "finished ($me)."
# exit
# echo "uh oh ($me)"
