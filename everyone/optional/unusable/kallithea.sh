#!/bin/sh
dest_root=/tank/local
this_user=`whoami`
this_group=`id -g -n $this_user`
project_unix_name=kallithea
project_venv_name=kallithea-venv
user_services_path="$dest_root/services/$this_user"
project_dest_path="$user_services_path/$project_unix_name"

echo "Gitea is recommended instead, by the author of this script Jacob Gustafson. Only modify this script and remove exit 7 if you really want kallithea, which only has code management web interface and no project management (install steps were not tested)."
echo "Gitea is:"
echo "* Community-oriented fork of Gogs"
echo "* Similar to GitLab (which also has self-hosted version) but far lighter"
echo "* Written in Go"
echo "* MIT License"
#echo "OpenProject is recommended instead by the author of this script Jacob Gustafson. Only modify this script and remove exit 7 if you really want kallithea, which only has code management web interface and no project management (install steps were not tested)."
#echo "Kallithea release versions can be installed via:"
#echo "  python2 -m pip install"
#echo " only edit this script and uncomment exit 7 if you really know what you're doing (want to install latest mercurial version in virtualenv) and are aware of open issues in the mercurial version:"
#echo " https://bitbucket.org/conservancy/kallithea/issues?status=new&status=open"
exit 7
echo
echo
echo "Kallithea is a self-hosted code management platform for mercurial and git:"
echo " * member project of Free Software Conservancy,"
echo " * GPL fork of RhodeCode (the fully GPL-compliant parts thereof)"
echo " * Has authentication optionally via LDAP or ActiveDirectory"
echo "This script attempts to install on a server that has a ZFS drive named tank with a filesystem called $dest_root, so if that is not you're situation, modify this script and change the value of dest_root to a location that can contain the services directory which will contain the $project_unix_name folder which will be owned by $this_user."
#cache the password to prevent glitches with pasting this script into terminal and terminal thinking line after sudo line was a password:
sudo ls
if [ "$this_user" = "root" ]; then
  echo "This script must not be run as root--pip in virtualenv (as a non-priveleged user) is best, to avoid interfering with the system's python"
  exit 1
fi
if [ ! -d $dest_root ]; then
  echo "Please make sure $dest_root exists on this system or modify value of dest_root in this script before running. The $project_unix_name folder will then be automatically created there."
fi

if [ ! -d "$dest_root/services" ]; then
  sudo mkdir "$dest_root/services"
  if [ ! -d "$dest_root/services" ]; then
    echo "ERROR: Nothing done since can't create $dest_root/services"
    exit 2
  fi
  #sudo chown $this_user "$dest_root/services"
fi
if [ ! -d "$dest_root/services/$this_user" ]; then
  sudo mkdir "$dest_root/services/$this_user"
  if [ ! -d "$dest_root/services/$this_user" ]; then
    echo "ERROR: Nothing done since can't create $dest_root/services/$this_user"
    exit 2
  fi
  #sudo chown $this_user "$dest_root/services"
fi
if [ ! -d "$user_services_path" ]; then
  sudo mkdir "$user_services_path"
  if [ ! -d "$user_services_path" ]; then
    echo "ERROR: Nothing done since can't create $dest_root/services/project_unix_name"
    exit 2
  fi
  sudo chown $this_user "$user_services_path"
  sudo chgrp $this_group "$user_services_path"
  echo "$user_services_path created for $this_user (unpriveleged user is recommended [sudoer is ok])."
fi
if [ -f "$user_services_path/testperms.tmp" ]; then
  rm "$user_services_path/testperms.tmp"
  if [ -f "$user_services_path/testperms.tmp" ]; then
    echo "Cannot install to $user_services_path since $this_user does not have ownership of the directory (cannot remove $user_services_path/testperms.tmp)."
    exit 3
  fi
fi
touch "$user_services_path/testperms.tmp"
if [ ! -f "$user_services_path/testperms.tmp" ]; then
  echo "Cannot install to $user_services_path since $this_user does not have ownership of the directory (could not create testperms.tmp"
  exit 4
else
  rm "$user_services_path/testperms.tmp"
fi
if [ -f "$user_services_path/testperms.tmp" ]; then
  echo "Cannot install to $user_services_path since $this_user does not have ownership of the directory (could not remove testperms.tmp"
  exit 5
fi
cd "$user_services_path"
#below (except conditions and python version specific calls) is from https://pythonhosted.org/Kallithea/installation.html :
if [ -d "$project_dest_path" ]; then
  echo "WARNING: Nothing cloned since $project_dest_path already exists. Delete or rename the directory first to get latest version"
else
  hg clone https://kallithea-scm.org/repos/kallithea -u stable
fi
if [ -d "$project_dest_path" ]; then
  cd "$project_dest_path"
else
  echo "ERROR: Nothing done since can't clone to $project_dest_path"
  exit 7
fi
if [ -d "$user_services_path/$project_venv_name" ]; then
  echo "WARNING: virtualenv not created since $project_dest_path/$project_venv_name already exists. Delete or rename the directory first for clean reinstall of $project_unix_name."
else
  virtualenv ../$project_venv_name
fi

if [ ! -d ../$project_venv_name ]; then
  "ERROR: Could not install since user has no permission to create virtualenv folder , or virtualenv is not installed."
  exit 8
fi
source ../$project_venv_name/bin/activate
#pip install --upgrade pip setuptools
python2 -m pip install --upgrade pip setuptools
#pip install -e .
python2 -m pip install -e .
python2 setup.py compile_catalog   # for translation of the UI
echo
echo
