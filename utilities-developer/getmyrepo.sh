#!/bin/bash

#region settings
MY_GITHUB_USERNAME="poikilos"
FORCE_GIT_DIR=~/git  # if this is blank, the repo will clone to the current directory.
#endregion settings


if [ -z "$1" ]; then
    "You must specify a repo name."
fi
if [ ! -z "$FORCE_GIT_DIR" ]; then
    getrepo.sh $1 --user $MY_GITHUB_USERNAME --repos_dir "$FORCE_GIT_DIR" --user_dir "$FORCE_GIT_DIR"
else
    getrepo.sh $1 --user $MY_GITHUB_USERNAME --repos_dir "`pwd`" --user_dir "`pwd`"
fi
