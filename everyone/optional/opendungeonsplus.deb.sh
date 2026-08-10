#!/bin/bash
# based on https://github.com/OpenDungeons/OpenDungeons/wiki/How-to-compile-on-Ubuntu
sudo apt install -y g++ || exit $?
sudo apt install -y cmake || exit $?
sudo apt install -y git || exit $?
sudo apt install -y libois-dev || exit $?
sudo apt install -y libogre-1.9-dev || exit $?
sudo apt install -y libexpat-dev || exit $?
sudo apt install -y libfreetype6-dev || exit $?
sudo apt install -y libboost-filesystem-dev libboost-locale-dev libboost-program-options-dev libboost-date-time-dev libboost-thread-dev libboost-system-dev || exit $?
LOCAL_REPO=~/git/OpenDungeonsPlus
if [ ! -d "$LOCAL_REPO" ]; then
    mkdir -p ~/Downloads/git/tomluchowski || exit $?
    if [ ! -d ~/Downloads/git/tomluchowski/OpenDungeonsPlus ]; then
	git clone https://github.com/tomluchowski/OpenDungeonsPlus.git ~/Downloads/git/tomluchowski/OpenDungeonsPlus || exit $?
	cd ~/Downloads/git/tomluchowski/OpenDungeonsPlus || exit $?
    else
	cd ~/Downloads/git/tomluchowski/OpenDungeonsPlus || exit $?
	git pull
    fi
    LOCAL_REPO=~/Downloads/git/tomluchowski/OpenDungeonsPlus
else
    cd $LOCAL_REPO || exit $?
fi
