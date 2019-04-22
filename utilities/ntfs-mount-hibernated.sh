#!/bin/sh
#This script mounts a drive owned by you as long as you are a sudoer. 
echo "`id -u`" /tmp/this_uid
echo "`id -g`" /tmp/this_gid
#sudo mount -t ntfs-3g -o ro /dev/sdi3 /media/windows
#sudo mount -t ntfs-3g -o rw,remove_hiberfile /dev/sdi3 /media/windows
#sudo ntfs-3g -o rw,remove_hiberfile /dev/sdi3 /media/windows
usage_s="You must specify a device and mount path such as /dev/sdg3 /run/media/owner/OS1"
if [ -z "$1" ]; then
  echo
  echo
  echo "$usage_s"
  echo
  echo
  exit 1
fi
if [ -z "$2" ]; then
  echo
  echo
  echo "$usage_s"
  echo
  echo
  exit 1
fi
if [ ! -d "$2" ]; then
  sudo mkdir "$2"
  if [ -d "$2" ]; then
    echo "created $2"
  else
    echo "ERROR: failed to create $2"
    exit 2
  fi
fi
sudo ntfs-3g -o recover,windows_names,remove_hiberfile,uid=`head -n 1 /tmp/this_uid`,gid=`head -n 1 /tmp/this_gid` $1 "$2"
# recover: clear windows log (default)
# windows_names: only use windows file names (no " * / : < > ? \ | nor any with code<0x20; though ntfs supports POSIX all chars but '/' and '\0')
# remove_hiberfile: destroy hibernated windows session to allow read-write mount
#if command shows usage screen, then change /dev/* to the correct block device (list them using lsblk)

