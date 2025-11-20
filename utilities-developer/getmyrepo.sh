#!/bin/bash
>&2 echo "Warning: this script is deprecated. Try 'getmyrepo'."
if [ ! -f "`command -v git`" ]; then
    echo "Error: git is not installed."
    exit 1
fi
#region settings
MY_GITHUB_USERNAME="Hierosoft"
# ^ Changed further down if not present there.
FORCE_GIT_DIR=~/git  # if this is blank, the repo will clone to getrepo's default.
#endregion settings

if [ -z "$1" ]; then
    "You must specify a repo name."
    exit 1
fi
code=0
if [ ! -z "$FORCE_GIT_DIR" ]; then
    getrepo "$@" --user $MY_GITHUB_USERNAME --repos_dir "$FORCE_GIT_DIR" --user_dir "$FORCE_GIT_DIR"
    code=$?
else
    getrepo "$@" --user $MY_GITHUB_USERNAME --repos_dir "`pwd`" --user_dir "`pwd`"
    code=$?
fi
if [ $code -ne 0 ]; then
    MY_GITHUB_USERNAME="Poikilos"
    echo "Trying $MY_GITHUB_USERNAME..."
else
    echo "getrepo returned success."
    exit 0
fi
if [ ! -z "$FORCE_GIT_DIR" ]; then
    getrepo "$@" --user $MY_GITHUB_USERNAME --repos_dir "$FORCE_GIT_DIR" --user_dir "$FORCE_GIT_DIR"
    code=$?
else
    getrepo "$@" --user $MY_GITHUB_USERNAME --repos_dir "`pwd`" --user_dir "`pwd`"
    code=$?
fi
exit $code
