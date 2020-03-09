#!/bin/bash

#ENABLE_SERVER=false
#if [ "@$1" = "--server" ]; then
#    ENABLE_SERVER=true
#fi
if [ -z "$BACKUP_DEST" ]; then
    BACKUP_DEST=$1
fi
if [ -z "$BACKUP_DEST" ]; then
    echo "You must specify a remote server path."
    exit 1
fi
# See <https://borgbackup.readthedocs.io/en/stable/installation.html
#      #distribution-package>
# AND <https://torsion.org/borgmatic/docs/how-to/set-up-backups/>
# (borgmatic)

# > In case you get complaints about permission denied on
# > /etc/fuse.conf: on Ubuntu this means your user is not in the fuse
# > group. Add yourself to that group, log out and log in again.

# IGNORE errors for the following command, as the fuse group doesn't
# exist:
sudo adduser $USER fuse

if [ ! -d ~/borg-env ]; then
    virtualenv --python=python3 ~/borg-env
    source ~/borg-env/bin/activate

    # install Borg + Python dependencies into virtualenv
    # pip install borgbackup
    # or alternatively (if you want FUSE support):
    pip install --upgrade borgbackup[fuse]
    pip install --upgrade borgmatic
else
    # update:
    pip install --upgrade borgbackup
    pip install --upgrade borgmatic
fi

sudo ln -s $HOME/borg-env/bin/borg /usr/local/bin/borg

deactivate

# borg init --encryption=repokey $BACKUP_DEST
# Running borg init here as per docs doesn't work, so instead see
# <https://roll.urown.net/desktop/borg-backup.html>
#if [ "@$ENABLE_SERVER" = "@false" ]; then
sudo ./borg postinstall
#fi
