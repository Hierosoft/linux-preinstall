#!/bin/bash
# Description: Borg is a backup solution that is capable of using any
# number of local or remote repos. Each repo is most efficient when
# used by only one machine. A backup device can have any number of
# repos. The server does not have to be setup with root permissions, but
# for the client to backup system files, it does have to run as root.
# Server configuration: Create or use an unpriveleged user, and run
# the borg-server-nonroot.sh script included with linux-preinstall. The
# full path to the repo you create must match the one you use in the
# client's borgmatic config.yaml:
# location:
#     repositories:
#         - <user>@<remote_host>:<full_path_on_remote_machine>


#if [ "@$1" = "@postinstall" ]; then
    # The "nonroot" script calls this script with this option.

#    echo "Running post-install..."
#    mkdir -p /etc/borg/{keys,ssh}
#    mkdir -p /var/lib/borg/{cache,security}
    # INFO: run backup (only the client, not the server) as root.
    #if [ "@$2" = "@server" ]; then
        #UNPRIVU=$3
        #if [ -z "$UNPRIVU" ]; then
            #echo "ERROR: you must specify an unpriveleged user for postinstall"
            #exit 1
        #fi
    #fi
    # See https://torsion.org/borgmatic/docs/how-to/set-up-backups/
    # borgmatic init --encryption repokey

if [ "@$1" = "@client" ]; then
    echo "Installing dependencies..."
    apt install -y python3 python3-dev python3-pip python-virtualenv \
        libssl-dev openssl \
        libacl1-dev libacl1 \
        build-essential
    apt install -y libfuse-dev fuse pkg-config  # optional, for FUSE support
    #virtualenv --python=python3 ~/borg-env
    #source ~/borg-env/bin/activate
    #pip install --upgrade borgmatic
    pip3 install --user --upgrade borgbackup
    # NOTE: borgbackup[fuse] FAILS:
    # - running borg says:
    #   Traceback (most recent call last):
    #   File "/root/.local/lib/python3.5/site-packages/borg/archiver.py", line 37, in <module>
    #     from . import __version__
    #   ImportError: cannot import name '__version__'
    # - no output from `which borg`
    pip3 install --user --upgrade borgmatic
    echo 'export PATH="$PATH:~/.local/bin"' >> ~/.profile
    # INFO: borgmatic does NOT automatically install borg (?):
    # - "No such file or directory: 'borg'"
    # - so I tried: python3 -c "import borg"
    # - which results in:
    #   "ImportError: No module named 'condor'"
    # - so changed above from borg to borgbackup
    pip3 install --user --upgrade condor
    # - but I still get "No such file or directory: 'borg'"
    # - so see <https://docs.borgbase.com/setup/cli/>:


    generate-borgmatic-config
    wget -O borgmatic.service https://projects.torsion.org/witten/borgmatic/raw/branch/master/sample/systemd/borgmatic.service
    if [ $? -eq 0 ]; then
        wget -O borgmatic.timer https://projects.torsion.org/witten/borgmatic/raw/branch/master/sample/systemd/borgmatic.timer
        if [ $? -ne 0 ]; then
            echo "Downloading borgmatic.timer failed."
            exit 1
        fi
    else
        echo "Downloading borgmatic.service failed."
        exit 1
    fi
    ERR=0
    ENABLE_RELOAD=false
    if [ -f /etc/systemd/system/borgmatic.timer -o -f /etc/systemd/system/borgmatic.service ]; then
        ENABLE_RELOAD=true
        sudo systemctl disable --now borgmatic.timer
    fi
    sudo mv borgmatic.service borgmatic.timer /etc/systemd/system/ || ERR=$?
    if [ $ERR -eq 0 ]; then
        if [ "@$ENABLE_RELOAD" = "@true" ] then
            systemctl daemon-reload
            systemctl restart borgmatic.timer
        fi
        sudo systemctl enable --now borgmatic.timer || ERR=$?
        # TODO: detect issues somehow. The command above returns zero
        #   even if:
        # > The unit files have no installation config (WantedBy, RequiredBy, Also, Alias
        # > settings in the [Install] section, and DefaultInstance for template units).
        # > This means they are not meant to be enabled using systemctl.
        # > Possible reasons for having this kind of units are:
        # > . . .
        if [ $ERR -ne 0 ]; then
            echo "See:"
            echo "/etc/systemd/system/borgmatic.service"
            echo "/etc/systemd/system/borgmatic.timer"
        fi
    else
        echo "ERROR: 'mv borgmatic.service borgmatic.timer /etc/systemd/system/' failed in `pwd`."
    fi
    cat <<END

INFO: exclude_caches only works for directories containing a file named
  CACHEDIR.TAG
INFO: If you want to backup mysql/mariadb databases but get
  the error "Key 'mysql_databases' was not defined." be sure
  to uncomment "hooks:" (since mysql_databases must be in hooks).

Now you must manually edit:
/etc/borgmatic/config.yaml

- backup parts of this machine as desired (change ).
- Uncomment and change the following:
  remote_path: /home/owner/borg-env/bin/borg
  exclude_caches: true
  exclude_nodump: true

END
custom_backup="/opt/backup-all.sh"
if [ -f "$custom_backup" ]; then
    cat <<END
- Change the ExecStart line to:
ExecStart=$custom_backup

END
else
    cat <<END
- Change the ExecStart line to:
ExecStart=`which systemd-inhibit`

END
fi
cat <<END
- Then run the following command to notify you of any errors in your
  configuration:
  validate-borgmatic-config

- Then ensure you have run the following so you don't have to store
  your password in plaintext (alternatively, use gopass as per
  <https://morr.cc/backups/>):
  sudo su -
  ssh-keygen
  # FIRST: set REMOTE_BACKUP_HOST to your server's address.
  ssh-copy-id -i ~/.ssh/id_rsa owner@$REMOTE_BACKUP_HOST

END
else
    echo "You must first run ./borg-server-nonroot.sh on the server, then run this script with the client option."
fi
