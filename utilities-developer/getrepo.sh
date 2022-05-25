#!/bin/bash
echo
echo
me="$0"
echo "Started $0 `date '+%Y-%m-%d %T'`"
myPath="$0"
realMyPath="`readlink $myPath`"
if [ ! -z "$realMyPath" ]; then
    myPath="$realMyPath"
fi
myName="`basename "$0"`"
myDir="`dirname $myPath`"
repoDir="`dirname $myDir`"
tryRC="$repoDir/utilities/git.rc"
usage() {
    cat <<END
$0
-----------
Clone a github repo using only the name.

USAGE
The current directory name must be the user name.
Otherwise, specify --user then the username.
If the website is not GitHub, specify the base URL after --site,
such as https://gitlab.com

    $me <repo_name> [options]

(The first CLI argument that isn't a non-boolean "--" switch and doesn't
have one before it will be used as REPO_NAME.)

OPTIONS:
(Unless CUSTOM_URL is set directly, it is constructed as follows:
CUSTOM_URL="\$WEBSITE/\$REMOTE_GIT_USER/\$REPO_NAME.git")

--repos_dir        (REPOS_DIR) Set the base directory for repos.
--user             (REMOTE_GIT_USER) Set the repo user
--user_dir         (USER_DIR) Construct the local repo path from
                   \$USER_DIR/\$REPO_NAME instead of
                   \$DEFAULT_REPO_DIR/\$REMOTE_GIT_USER/\$REPO_NAME
                   (DEFAULT_REPO_DIR is in $tryRC)
--site             (WEBSITE) Set the base url for CUSTOM_URL. If it is
                   a known name (notabug, gitlab, or github), it will
                   be automatically converted to a URL and set
                   CUSTOM_URL.
--url              (CUSTOM_URL) Set the repo url directly. This option
                   overrides the WEBSITE option.

EXAMPLES
    $me basic_materials --user poikilos --site https://gitlab.com
    # ends up as ~/Downloads/git/poikilos/

    $me filter --user poikilos --repos_dir ~/git
    # - uses github.com/poikilos
    # - clones to ~/git/poikilos/filter

    $me filter --user poikilos --repos_dir ~/git --user_dir ~/git
    # - uses github.com/poikilos
    # - clones to ~/git/filter

    $me filter --site github
    # - uses github.com (doesn't check other git sites first)
    # - clones to ~/Downloads/git/poikilos/filter

END
}


. $tryRC
if [ $? -ne 0 ]; then
    echo "Error: \"$tryRC\" doesn't exist."
    exit 1
fi

customExit() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
# parentdir="$(dirname "`pwd`")"
THIS_DIR_NAME=${PWD##*/}
PARENT_DIR="$(dirname "`pwd`")"
if [ -z "$DEFAULT_REPOS_DIR" ]; then
    DEFAULT_REPOS_DIR="$HOME/Downloads/git"
fi

REPO_DIR_SUFFIX=
IS_MIRROR=false

OPTIONS=

_ENV_REPO_NAME="$REPO_NAME"  # in case user set env
REPO_NAME=""  # must start as zero length for logic below

if [ -z "$USER_DIR" ]; then
    USER_DIR=""
else
    echo "* using environment's USER_DIR: '$USER_DIR'"
fi

for var in "$@"
do
    if [ ! -z "$NEXT_VAR" ]; then
        if [ "$NEXT_VAR" = "--user" ]; then
            REMOTE_GIT_USER="$var"
        elif [ "$NEXT_VAR" = "--site" ]; then
            WEBSITE="$var"
            if [ "@$WEBSITE" = "@github" ]; then
                WEBSITE="https://github.com"
            elif [ "@$WEBSITE" = "@gitlab" ]; then
                WEBSITE="https://gitlab.com"
            elif [ "@$WEBSITE" = "@notabug"]; then
                WEBSITE="https://notabug.org"
            else
                echo "* unknown website will be used as repo base URL: $WEBSITE"
                WEBSITE=$(echo $var | sed 's:/*$::')  # remove trailing /'s
            fi
            echo "* using WEBSITE $WEBSITE"
            # CUSTOM_WEBSITE="$WEBSITE"
        elif [ "$NEXT_VAR" = "--url" ]; then
            CUSTOM_URL="$var"
            # CUSTOM_WEBSITE="$WEBSITE"
        elif [ "$NEXT_VAR" = "--repos_dir" ]; then
            REPOS_DIR="$var"
        elif [ "$NEXT_VAR" = "--user_dir" ]; then
            USER_DIR="$var"
            # echo "* You set the USER_DIR to '$USER_DIR'."
        else
            customExit "Unknown option: $NEXT_VAR"
        fi
        NEXT_VAR=""
    else
        if [ "@$var" = "@--help" ]; then
            usage
            exit 0
        elif [ "@$var" = "@--user" ]; then
            NEXT_VAR="$var"
        elif [ "@$var" = "@--site" ]; then
            NEXT_VAR="$var"
        elif [ "@$var" = "@--repos_dir" ]; then
            NEXT_VAR="$var"
        elif [ "@$var" = "@--user_dir" ]; then
            NEXT_VAR="$var"
        elif [ "@$var" = "@--url" ]; then
            NEXT_VAR="$var"
        elif [ "@$var" = "@--mirror" ]; then
            OPTIONS="$OPTIONS --mirror"
            REPO_DIR_SUFFIX=".git"
            IS_MIRROR=true
        elif [ "@$REPO_NAME" = "@" ]; then
            REPO_NAME="$var"
            if [ ! -z "$_ENV_REPO_NAME" ]; then
                echo "* WARNING: you specified REPO_NAME (first sequential argument), which overrides an existing REPO_NAME value in the environment: \"$_ENV_REPO_NAME\""
            #else
                #echo "* REPO_NAME is now '$REPO_NAME'"
            fi
        else
            usage
            customExit "unknown option: $var"
        fi
    fi
done

if [ "@$USER_DIR" != "@" ]; then
    echo "* USER_DIR: '$USER_DIR'."
fi

WEBSITE_GITHUB="https://github.com"
WEBSITE_GITLAB="https://gitlab.com"
WEBSITE_NOTABUG="https://notabug.org"
# if [ -z "$WEBSITE" ]; then
#     WEBSITE="$WEBSITE_GITHUB"
#     echo "* assuming website is GitHub since you did not specify one (others will be tried first just in case the repo was migrated and is maintained more elsewhere)"
# fi

if [ ! -z "$REPOS_DIR" ]; then
    if [ ! -z "$USER_DIR" ]; then
        # REPOS_DIR="$(dirname "$USER_DIR")"
        REPOS_DIR="$USER_DIR"
        echo "* changing REPOS_DIR to '$REPOS_DIR' based on USER_DIR ('$USER_DIR')"
    fi
    echo "* using REPOS_DIR=\"$REPOS_DIR\""
else
    if [ ! -z "$USER_DIR" ]; then
        # REPOS_DIR="$(dirname "$USER_DIR")"
        REPOS_DIR="$USER_DIR"
        echo "* changing REPOS_DIR to '$REPOS_DIR' based on USER_DIR ('$USER_DIR')"
    fi
    # REPOS_DIR="$(dirname "`pwd`")"
    # REPOS_DIR="$(dirname "$DEFAULT_REPOS_DIR")"
    # REPOS_DIR="$PARENT_DIR"
    REPOS_DIR="$DEFAULT_REPOS_DIR"
    echo "* --repos_dir (or REPOS_DIR environment variable) was not specified (defaulted to \"$REPOS_DIR\")"
fi
UNUSED_REPOS_DIR="<REPOS_DIR should not have been used>"
if [ ! -z "$REMOTE_GIT_USER" ]; then
    if [ ! -z "$USER_DIR" ]; then
        # NOT: USER_DIR="$(dirname "$USER_DIR")"
        # since custom path negates the USER_DIR mechanism.
        REPOS_DIR="$UNUSED_REPOS_DIR"  # REPOS_DIR="$USER_DIR/.."  # ignored from now on
        echo "* --user_dir or USER_DIR superseded per-user directories, so $REMOTE_GIT_USER's repos will go under: $USER_DIR"
    else
        USER_DIR="$REPOS_DIR/$REMOTE_GIT_USER"
        echo "* $REMOTE_GIT_USER's repos will go under: '$USER_DIR' (since USER_DIR is not set)"
    fi

    if [ ! -d "$USER_DIR" ]; then
        mkdir "$USER_DIR" || customExit "'mkdir \"$USER_DIR\"' failed."
        echo "* created \"$USER_DIR\""
    fi
else
    if [ "$REPOS_DIR" == "$DEFAULT_REPOS_DIR" ]; then
        REMOTE_GIT_USER="$THIS_DIR_NAME"
        echo "* assuming user from current directory: $REMOTE_GIT_USER"
        USER_DIR="$REPOS_DIR/$REMOTE_GIT_USER"
        echo "* The user's repos will go under: '$USER_DIR' (under DEFAULT_REPOS_DIR \"$DEFAULT_REPOS_DIR\")"
    else
        customExit "You didn't provide the --user option and you are not in a directory under the REPOS_DIR (\"$REPOS_DIR\"), so the username cannot be assumed to be the current directory name \"$THIS_DIR_NAME\" (If you run this script from a directory under \"$DEFAULT_REPOS_DIR\" (DEFAULT_REPOS_DIR) and it matches REPOS_DIR (such as if you do not set other options for custom directories), then you do not have to provide the --user option)."
    fi
fi


if [ "$REPOS_DIR" != "$UNUSED_REPOS_DIR" ]; then
    # This is just a sanity check. The next cd command will go to USER_DIR.

    # if [ "$PWD" != "$USER_DIR" ]; then
    cd "$REPOS_DIR" || customExit "Cannot cd to specified REPOS_DIR: \"$REPOS_DIR\""
    # fi
fi
#if [ "$PWD" != "$USER_DIR" ]; then
if [ ! -d "$USER_DIR" ]; then
    usage
    echo
    echo "Error: \"$USER_DIR\" doesn't exist (You are in \"`pwd`\")"
    exit 1
fi
cd "$USER_DIR" || customExit "Cannot cd to specified USER_DIR: \"$USER_DIR\" (You are in \"`pwd`\")."
echo "* cd \"$USER_DIR\""
#fi

echo "  - USER (--user) directories such as \"$REMOTE_GIT_USER\" will appear under USER_DIR ('$USER_DIR')"
echo "    - Repo directories will appear under that."


if [ "@$WEBSITE" = "@" ]; then
    WEBSITE=""
else
    echo "* using WEBSITE: $WEBSITE"
    if [ "@$CUSTOM_URL" = "@" ]; then
        CUSTOM_URL="$WEBSITE/$REMOTE_GIT_USER/$REPO_NAME.git"
        echo "  * constructed CUSTOM_URL: \"$CUSTOM_URL\""
    else
        echo "  * overridden by CUSTOM_URL: \"$CUSTOM_URL\""
    fi
fi

if [ "@$CUSTOM_URL" = "@" ]; then
    CUSTOM_URL=""
else
    echo "* using CUSTOM_URL: $CUSTOM_URL"
    if [ "@$WEBSITE" != "@" ]; then
        echo "  * Warning: CUSTOM_URL overrides WEBSITE \"$WEBSITE\"."
    fi
fi

# At this point, the WEBSITE, REPOS_DIR, and REMOTE_GIT_USER are set.



if [ -z "$REPO_NAME" ]; then
    REPO_NAME="$_ENV_REPO_NAME"
    echo "* using REPO_NAME from environment: $REPO_NAME"
fi
if [ -z "$REPO_NAME" ]; then
    usage
    customExit "You did not specify a repo name."
fi

if [ "`pwd`" != "$USER_DIR" ]; then
    customExit "The script failed to end up in $USER_DIR (PWD is '$PWD' accidentally)"
fi


GITHUB_URL="$WEBSITE_GITHUB/$REMOTE_GIT_USER/$REPO_NAME.git"
# CUSTOM_URL="$WEBSITE/$REMOTE_GIT_USER/$REPO_NAME.git"
# URL="$CUSTOM_URL"
URL=""
GITLAB_URL="$WEBSITE_GITLAB/$REMOTE_GIT_USER/$REPO_NAME.git"
NOTABUG_URL="$WEBSITE_NOTABUG/$REMOTE_GIT_USER/$REPO_NAME.git"
LOCAL_REPO_NAME="$REPO_NAME$REPO_DIR_SUFFIX"
DEST="$USER_DIR/$LOCAL_REPO_NAME"
# if [ ! -d "$REPO_NAME" ]; then
_found=false
_path_suffix=""
if [ ! -d "$DEST" ]; then
    if [ "@$CUSTOM_URL" != "@" ]; then
        echo "* [$myName] using CUSTOM_URL $CUSTOM_URL..."
        echo "\n\n" | git ls-remote $CUSTOM_URL -q
        if [ $? -eq 0 ]; then
            # echo "* [$myName] detected $WEBSITE repo"
            URL="$CUSTOM_URL"
            if [ "$_found" = "true" ]; then
                if [ "$CUSTOM_URL" = "$GITHUB_URL" ]; then
                    _path_suffix="/1.github"
                else
                    _path_suffix="/1.custom_git_site"
                fi
                DEST="$USER_DIR$_path_suffix/$LOCAL_REPO_NAME"
            fi
            echo "* cloning $URL to $DEST (OPTIONS=$OPTIONS)"
            _found=true
            # git clone $OPTIONS $CUSTOM_URL $DEST
            update_repo $DEST $URL $OPTIONS
        else
            echo "  * not found"
        fi
        if [ "$_found" != "true" ]; then
            echo "Error: A git URL $REMOTE_GIT_USER/$REPO_NAME wasn't detected (tried git ls-remote <url> -q) in $NOTABUG_URL, $GITLAB_URL or $WEBSITE."
            exit 1
        fi
    else
    echo "* checking for $NOTABUG_URL..."
    echo "\n\n" | git ls-remote $NOTABUG_URL -q
    if [ $? -eq 0 ]; then
        echo "* [$myName] detected $NOTABUG_URL repo"
        _found=true
        URL="$NOTABUG_URL"
        echo "* cloning the detected $URL in `pwd` (OPTIONS=$OPTIONS)"
        # git clone $OPTIONS $NOTABUG_URL $DEST
        update_repo $DEST $URL $OPTIONS
    else
        echo "  * not found"
    fi
    echo "* checking for $GITLAB_URL..."
    yes | git ls-remote -h --exit-code $GITLAB_URL
    # ^ For some reason, -q makes it fail with 2 (--exit-code should only produce 2 when no matching remote refs)
    if [ $? -eq 0 ]; then
        echo "* [$myName] detected $GITLAB_URL repo"
        if [ "$_found" = "true" ]; then
            _path_suffix="/1.gitlab"
            DEST="$USER_DIR$_path_suffix/$LOCAL_REPO_NAME"
        fi
        _found=true
        URL="$GITLAB_URL"
        echo "* cloning $URL to $DEST (OPTIONS=$OPTIONS)"
        # git clone $OPTIONS $GITLAB_URL $DEST
        update_repo $DEST $URL $OPTIONS
    else
        echo "  * not found: yes | git ls-remote -h --exit-code $GITLAB_URL -q"
    fi
    echo "* checking for $GITHUB_URL last..."
    echo "\n\n" | git ls-remote $GITHUB_URL -q
    if [ $? -eq 0 ]; then
        echo "* [$myName] detected $WEBSITE_GITHUB repo"
        URL="$GITHUB_URL"
        if [ "$_found" = "true" ]; then
            if [ "$GITHUB_URL" = "$GITHUB_URL" ]; then
                _path_suffix="/1.github"
            else
                _path_suffix="/1.custom_git_site"
            fi
            DEST="$USER_DIR$_path_suffix/$LOCAL_REPO_NAME"
        fi
        echo "* cloning $URL to $DEST (OPTIONS=$OPTIONS)"
        _found=true
        # git clone $OPTIONS $GITHUB_URL $DEST
        update_repo $DEST $URL $OPTIONS
    else
        echo "  * not found"
    fi
    if [ "$_found" != "true" ]; then
        echo "Error: A git URL $REMOTE_GIT_USER/$REPO_NAME wasn't detected (tried git ls-remote <url> -q) in $NOTABUG_URL, $GITLAB_URL or $WEBSITE."
        exit 1
    fi
    # git clone $URL $USER_DIR/$REPO_NAME
    # git clone $URL || customExit "'git clone $URL' failed in '`pwd`'"
    fi
else
    cd "$DEST" || customExit "'cd \"$DEST\"' failed in '`pwd`'"
    if [ "@$IS_MIRROR" = "@true" ]; then
        git remote update || customExit "'git remote update' failed in '`pwd`'"
    else
        git pull --no-rebase || customExit "'git pull' failed in '`pwd`'"
    fi
fi
if [ $? -eq 0 ]; then
    echo "[$myName] OK"
else
    echo "[$myName] Error: There was an untracked error."
fi
