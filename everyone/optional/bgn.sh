#!/bin/bash
customExit() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    exit 1
}
cd
if [ ! -d "git" ]; then
    mkdir git
fi
cd ~/git || customExit "Cannot cd $HOME/git"
ffsURL=https://github.com/poikilos/ForwardFileSync.git

if [ ! -d "ForwardFileSync" ]; then
    echo "getting ForwardFileSync..."
    git clone $ffsURL || customExit "Cannot clone $ffsURL"
else
    cd ForwardFileSync
    echo "updating ForwardFileSync..."
    git pull || echo "Cannot update ForwardFileSync"
fi
cd ~/git || customExit "Cannot cd $HOME/git"
bgnURL=https://github.com/poikilos/BackupGoNow
if [ ! -d "BackupGoNow" ]; then
    echo "Getting BackupGoNow..."
    git clone $bgnURL || customExit "Cannot clone $bgnURL"
    cd "$HOME/git/BackupGoNow" || customExit "Cannot cd $HOME/git/BackupGoNow"
else
    echo "updating BackupGoNow..."
    cd "$HOME/git/BackupGoNow" || customExit "Cannot cd $HOME/git/BackupGoNow"
    git pull || echo "Cannot update BackupGoNow"
fi
bash build.sh
