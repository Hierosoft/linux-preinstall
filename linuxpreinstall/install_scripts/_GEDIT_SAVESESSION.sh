#!/bin/bash
THIS_MAINTAINER=poikilos
if [ ! -d "$HOME/git" ]; then mkdir -p "$HOME/git"; fi
cd "$HOME/git"
#if [ -d "Gedit-External-Tools-SaveSession" ]; then rm -Rf "Gedit-External-Tools-SaveSession"; fi
git_url=https://github.com/$THIS_MAINTAINER/Gedit-External-Tools-SaveSession.git
if [ ! -d "Gedit-External-Tools-SaveSession" ]; then
    git clone $git_url
else
    cd Gedit-External-Tools-SaveSession
    git pull
    cd ..
fi
if [ ! -d "Gedit-External-Tools-SaveSession" ]; then
    echo "FAILED to get Gedit-External-Tools-SaveSession from $git_url" >> $postinstall
else
    cd "Gedit-External-Tools-SaveSession"
    bash install || echo "cd Gedit-External-Tools-SaveSession && bash install # FAILED" >> $postinstall
fi
