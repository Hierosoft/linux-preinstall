#!/bin/bash
me=`basename "$0"`
usage() {
    echo "$me <user1 [&2] GitHub project name> <user1 (yours, won't be pulled if exists)> <user2> [<person2 full url if not GitHub>]"
    echo "* User 1 project will go in $HOME/git"
    echo "* User 2 project will go in $HOME/Downloads/git/<user2>/<project>"
}
customDie() {
    if [ -z "$1" ]; then echo "Unknown error."; fi
    echo "$1"
    exit 1
}
if [ -z "$1" ]; then
    usage
    exit 1
fi
if [ -z "$2" ]; then
    usage
    exit 1
fi
projectName="$1"
user1="$2"
url1="https://github.com/$user1/$projectName"
if [ -z "$3" ]; then
    usage
    exit 1
fi
user2="$3"
url2="https://github.com/$user2/$projectName"
if [ ! -z "$4" ]; then
    url2="$4"
fi

if [ ! -d "$HOME/git" ]; then
    mkdir "$HOME/git" || customDie "ERROR: cannot create '$HOME/git'"
fi
cd "$HOME/git" || customDie "ERROR: Cannot cd '$HOME/git'"
dest1="$HOME/git/$projectName"
if [ -d "$projectName" ]; then
    cd "$dest1" || customDie "ERROR: Cannot cd '$HOME/git/$projectName'"
    # don't pull this--assume it is one's own project
    # git pull || customDie "ERROR: failed to pull '$url1'"
    cd ..
else
    git clone "$url1" || customDie "ERROR: failed to clone '$url1'"
fi

if [ ! -d "$HOME/Downloads/git/$user2" ]; then
    mkdir -p "$HOME/Downloads/git/$user2" || customDie "ERROR: Cannot create '$HOME/Downloads/git/$user2'"
fi
cd "$HOME/Downloads/git/$user2" || customDie "ERROR: Cannot cd '$HOME/Downloads/git/$user2'"
dest2="$HOME/Downloads/git/$user2/$projectName"
if [ -d "$projectName" ]; then
    cd "$dest2" || customDie "ERROR: Cannot cd '$HOME/Downloads/git/$user2/$projectName'"
    git pull || customDie "ERROR: failed to pull '$url2'"
    cd ..
else
    git clone "$url2" || customDie "ERROR: failed to clone '$url2'"
fi
if [ -f "`command -v meld`" ]; then
    echo "* meld '$dest1' '$dest2'"
    meld "$dest1" "$dest2" &
else
    echo "WARNING: meld is not installed so manually run"
    echo "  diff '$dest1' '$dest2'"
fi
