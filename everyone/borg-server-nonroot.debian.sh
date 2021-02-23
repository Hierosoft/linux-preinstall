#!/bin/bash

# There should be a repo for each computer to avoid slowness and
# concurrency issues according to
# https://borgbackup.readthedocs.io/en/stable/faq.html

if [ -z "@$LOCAL_BACKUP_REPO" ]; then
    LOCAL_BACKUP_REPO="$1"
fi
if [ -z "@$LOCAL_BACKUP_REPO" ]; then
cat <<END
You must specify a local directory for creating the repo on this server, such as:
  $0 /tank/local/Backup/computer1
- The most effective use of repos is to create a repo for each client,
  according to <https://borgbackup.readthedocs.io/en/stable/faq.html>.
END
    exit 1
fi

customDie() {
    echo
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
sudo ./borg.sh server || customDie "You must be in the directory as borg.sh such as linux-preinstall/."
# borgmatic init --encryption repokey
#./borg-nonroot.sh
virtualenv --python=python3 ~/borg-env
source ~/borg-env/bin/activate
pip install --upgrade borgbackup[fuse]
borg init --encryption=repokey $LOCAL_BACKUP_REPO
# See <https://borgbackup.readthedocs.io/en/stable/quickstart.html>
# sudo ln -s $HOME/borg-env/bin/borg /usr/local/bin/
cat <<END
#helpful commands:
borg list $LOCAL_BACKUP_REPO
# ^ lists all archives
borg list $LOCAL_BACKUP_REPO::ARCHIVE_NAME
END
