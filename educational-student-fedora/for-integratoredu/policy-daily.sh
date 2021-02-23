#!/bin/sh
# file_key: daily
# dest_path: /etc/cron.daily/iedu-mps-daily
# post_install: chmod +750 "/etc/cron.daily/iedu-mps-daily"
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
DATE=`date '+%Y-%m-%d %H:%M:%S'`

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
echo "using home path $LU_HOME"

INSTALL_CMD="dnf install -y"
REMOVE_CMD="dnf remove -y"
UPGRADE_CMD="dnf upgrade -y"
REFRESH_CMD="dnf --refresh"
LIST_INSTALLED_CMD="dnf list installed"
P3TK_PKG="python3-tkinter"
if [ -f "`command -v pacman`" ]; then
  INSTALL_CMD="pacman -Syyu --noconfirm"
  REMOVE_CMD="pacman -R --noconfirm"
  UPGRADE_CMD="pacman -Syyu --noconfirm"
  #REFRESH_CMD="pacman -Scc"
  REFRESH_CMD="#nothing do refresh since using pacman (pacman -Scc clears cache but that's rather brutal)...  # "
  LIST_INSTALLED_CMD="pacman -Q"  # Qe lists packages explicitly installed (see pacman -Q --help)
  P3TK_PKG="tk"  # python-tkinter is an integral part of python in arch
fi
if [ -f "`command -v apt`" ]; then
  INSTALL_CMD="apt install -y"
  REMOVE_CMD="apt remove -y"
  UPGRADE_CMD="apt upgrade"
  REFRESH_CMD="apt update"
  LIST_INSTALLED_CMD="apt list --installed"
  P3TK_PKG="python3-tk"
  # and update cache immediately since using a dependency resolver with non-smart cache
  apt update
fi
# ^ pasted into https://github.com/linux-preinstall/api.rc
# ^ should match policy-hourly.sh
echo
echo "[ $me ] using package manager command: $INSTALL_CMD"
echo
echo


if [ ! -f "`command -v wget`" ]; then
  $INSTALL_CMD wget
fi

cd /tmp

url_suffix="&unit=0&kernel=linux&access_level=root&hostname=`hostname`&user=$USER"
mgn_path="$CONFIGS_PATH/machine_group_name"
if [ -f "$mgn_path" ]; then
  url_suffix="$url_suffix&machine_group=`head -n 1 "$mgn_path"`"
else
  url_suffix="$url_suffix&machine_group=StudentMachines"
fi
if [ -f "$su_path" ]; then
  # NOTE: must use double quotes inside grave accents with cat, or cat will wait for input if variable value is blank
  url_suffix="$url_suffix&stated_username=`head -n 1 "$su_path"`"
fi

if [ ! -z "$LOCAL_USER" ]; then
  url_suffix="$url_suffix&local_username=$LOCAL_USER"
fi

# update the OTHER script:
src_name="hourly"
cron_freq="hourly"
local_name="iedu-mps-$src_name"
HR_LOCK_PATH="$LOCKS_PATH/$local_name"
if [ -f "$HR_LOCK_PATH" ]; then
  # TODO: wget and send the error in the request
  this_ymd=`date '+%Y-%m-%d'`
  running_time=$(head -n 1 "$HR_LOCK_PATH")
  if [[ "$running_time" != *"$this_ymd"* ]]; then
    # remove stale lock from before today:
    rm -f "$HR_LOCK_PATH"
  fi
fi

# remove outdated name:
dest_path="/etc/cron.$cron_freq/iedu-cs-$src_name"
if [ -f "$dest_path" ]; then
  rm -f "$dest_path"
fi

dest_path="/etc/cron.$cron_freq/iedu-mps-$src_name"

# remove leftovers:
if [ -f "$local_name" ]; then
  rm -f "$local_name"
fi
# if [ -f "$dest_path" ]; then
  # rm -f "$dest_path"
# fi
wget --output-document="$local_name" "$text_req_url?file_key=$src_name$url_suffix"
update_enable="true"
# don't state the good flag literally, or it will be read as a good flag
# (integratoredu webapp should automatically append the value of good_flag to the end as a comment)
good_flag="update_enable: $update_enable"
if grep -q "$good_flag" "$local_name"; then
  mv -f "$local_name" "$dest_path"
  chmod 750 "$dest_path"
  # and run it NOW:
  if [ ! -f "$HR_LOCK_PATH" ]; then
    echo "running $dest_path..."
    # MUST exit now, since $dest_path script updates this script!
    $dest_path && echo "finished ($me)" && exit 0
  else
    running_time=$(head -n 1 "$HR_LOCK_PATH")
    echo "not running hourly script since already running since $running_time"
  fi
else
  echo "failed to get $local_name with $good_flag"
fi

# only do full system update if before 7am or after 5pm
if [ "`date '+%-H'`" -lt 7 ]; then
  $UPGRADE_CMD
else
  if [ "`date '+%-H'`" -gt 17 ]; then
    $UPGRADE_CMD
  fi
fi
echo "used $url_suffix"
echo "updating OS (daily runs after computer is up for 5 mins between 3am-10pm)..."
$UPGRADE_CMD flatpak
$UPGRADE_CMD --refresh
$UPGRADE_CMD systemd
$UPGRADE_CMD --refresh
$UPGRADE_CMD dbus
$UPGRADE_CMD --refresh
$UPGRADE_CMD dbus flatpak systemd

$UPGRADE_CMD

echo "finished ($me)"
# exit
# echo "uh oh ($me)"
