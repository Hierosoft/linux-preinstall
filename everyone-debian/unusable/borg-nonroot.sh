#!/bin/bash






cat <<END
The script borg-nonroot.sh is deprecated, since the client backup
process should run as root (as recommended by authors regarding the
question of reading files from /etc).
END
exit 0







ENABLE_SERVER=false
#if [ "@$1" = "--server" ]; then
#    ENABLE_SERVER=true
#else
if [ -z "$BACKUP_DEST" ]; then
    BACKUP_DEST=$1
fi
if [ -z "$BACKUP_DEST" ]; then
    echo "You must specify a remote server path."
    exit 1
fi
#fi
# See <https://borgbackup.readthedocs.io/en/stable/installation.html
#      #distribution-package>
# AND <https://torsion.org/borgmatic/docs/how-to/set-up-backups/>
# (borgmatic)

# > In case you get complaints about permission denied on
# > /etc/fuse.conf: on Ubuntu this means your user is not in the fuse
# > group. Add yourself to that group, log out and log in again.

# IGNORE errors for the following command, as the fuse group doesn't
# exist on Debian 9 (does exist on Ubuntu 18.04):
sudo adduser $USER fuse

virtualenv --python=python3 ~/borg-env
source ~/borg-env/bin/activate

# INFO: borgmatic is for the CLIENT

if [ ! -d ~/borg-env ]; then
    # install Borg + Python dependencies into virtualenv
    # pip install borgbackup
    # or alternatively (if you want FUSE support):
    pip install --upgrade borgmatic
else
    # update:
    pip install --upgrade borgmatic
fi

deactivate

# borg init --encryption=repokey $BACKUP_DEST
# Running borg init here as per docs doesn't work, so instead see
# <https://roll.urown.net/desktop/borg-backup.html>
#if [ "@$ENABLE_SERVER" = "@true" ]; then
    # sudo ln -s $HOME/borg-env/bin/generate-borgmatic-config /usr/local/bin/
    # sudo ./borg postinstall server $USER
#    echo "Server components are installed."
#else
sudo ./borg postinstall
#fi
