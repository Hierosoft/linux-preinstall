#!/bin/bash
if [ ! -f "`command -v git`" ]; then
    echo "Error: git is not installed."
    exit 1
fi
#region settings
MY_GITHUB_USERNAME="Poikilos"
# ^ Changed further down if not present there.
FORCE_GIT_DIR=~/git  # if this is blank, the repo will clone to the current directory.
#endregion settings


if [ -z "$1" ]; then
    "You must specify a repo name."
fi
if [ ! -z "$FORCE_GIT_DIR" ]; then
    getrepo.sh "$@" --user $MY_GITHUB_USERNAME --repos_dir "$FORCE_GIT_DIR" --user_dir "$FORCE_GIT_DIR"
else
    getrepo.sh "$@" --user $MY_GITHUB_USERNAME --repos_dir "`pwd`" --user_dir "`pwd`"
fi
if [ $? -ne 0 ]; then
    MY_GITHUB_USERNAME="hierosoft"
else
    exit 0
fi
if [ ! -z "$FORCE_GIT_DIR" ]; then
    getrepo.sh "$@" --user $MY_GITHUB_USERNAME --repos_dir "$FORCE_GIT_DIR" --user_dir "$FORCE_GIT_DIR"
else
    getrepo.sh "$@" --user $MY_GITHUB_USERNAME --repos_dir "`pwd`" --user_dir "`pwd`"
fi
