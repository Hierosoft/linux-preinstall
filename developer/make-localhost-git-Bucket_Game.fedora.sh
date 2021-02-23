#!/bin/bash
REPO_OWNER="The minetest.org Team"
parent_name=linux-minetest-kit
repo_name="Bucket_Game"

me=`basename $0`
DATE=`date '+%Y-%m-%d %H:%M:%S'`
enable_update=false

customDieIfNew() {
    if [ "@$enable_update" = "@false" ]; then
	customDie "$@"
    fi
}

customDie() {
    echo
    echo "ERROR:"
    echo "  $@"
    # echo "  $1"
    echo
    echo
    exit 1
}

usage() {
cat <<END
--simulate       Show variables and commands but don't use rsync or git.
--update <path>  Use a source as a commit (instead of failing if server
                   or client directories were already created).
END
}

enable_simulate=false
use_next_as_source=false
single_source=""
for var in "$@"
do
    if [ "@$use_next_as_source" = "@true" ]; then
	use_next_as_source=false
	single_source="$var"
    fi
    if [ "@$var" = "@--simulate" ]; then
	enable_simulate=true
    elif [ "@$var" = "@--update" ]; then
	enable_update=true
	use_next_as_source=true
    else
	customDie "Unknown param: $var"
    fi
done
if [ "@$enable_update" = "@true" ]; then
    if [ -z "$single_source" ]; then
	usage
	echo
	customDie "You must specify a path after the '--update' option."
	echo
	echo
    fi
fi
# based on Jan Kruger "answered Dec 2 '13 at 13:04" Retrieved from https://stackoverflow.com/questions/20325089/hosting-a-git-server-on-localhost 2018-03-26
repos_url="$HOME/localrepos"
repo_url="$repos_url/$repo_name.git"
clones_path=$HOME/git
echo
echo
echo "$me recreates the git commit history on the 'server' as a local git repository directory $repo_url, by cloning to (and pushing several commits from) '$clones_path'."
enable_init=false
if [ "@$enable_update" = "@false" ]; then
    mkdir -p "$repo_url" || customDie "Cannot mkdir $repo_url"
    enable_init=true
fi

cd $repo_url || customDie "Cannot cd $repo_url"

if [ "@$enable_init" = "@true" ]; then
    git init --bare
# desc_file="$HOME/localrepos/Bucket_Game.git/description"
desc_file="$repo_url/description"
# if [ ! -f "$desc_file" ]; then
# non-empty by default: "Unnamed repository; edit this file 'description' to name the repository."
    echo "Local copy of Bucket_Game from minetest.org linux-minetest-kit releases as git commits to $DATE" >> "$desc_file"
# fi
cat > $repo_url/config <<EOF
[gitweb]
owner = "$REPO_OWNER"
EOF
fi

if [ ! -d "$clones_path" ]; then
    mkdir $clones_path || customDie "Cannot mkdir $clones_path"
fi
cd $clones_path || customDie "Cannot cd $clones_path"
cloned_path="$HOME/git/$repo_name"
if [ ! -d $repo_name ]; then
    git clone $repo_url
    cd $repo_name || customDie "Cannot cd $repo_name"
    cloned_path="`pwd`"
else
    customDieIfNew "
The repo was already recreated. You will have to run:
    rm -Rf $repo_url && rm -Rf $cloned_path
    # and if you're not sure it worked well, then also:
    #   rm $cloned_path/../*-untracked.txt
    # to try again.
"
    cd $repo_name || customDie "Cannot cd $repo_name"
    git pull
    cloned_path="`pwd`"
fi
if [ ! -d "$cloned_path" ]; then
    customDie "git could not create $cloned_path from $repo_url"
fi
releases="$HOME/git/EnlivenMinetest/webapp/minetest-versions"
done_count=0
sleep_count=5
real_count=`ls -1 $releases | wc -l`
if [ "@$enable_simulate" = "@false" ]; then
    echo "Processing commands..."
else
    echo "Simulating commands..."
fi

push_source() {
    src_path="$1"
    version="$2"
    if [ -z "$version" ]; then
	echo
	echo
	echo "detecting version... (Ctrl C to cancel)"
	sleep 2
	if [ ! -f "$src_path/release.txt" ]; then
	    echo
	    echo
	    echo "* '$src_path' remains$destroy_msg."
	    customDie "Missing $src_path/release.txt"
	fi
	release_line="`head -n 1 $src_path/release.txt`"
	version="${release_line##* }"  # get second word
	version_len=${#version}
	if [ "$version_len" -ne "6" ]; then
	    customDie "Unexpected version scheme (not 6 characters): '$version'"
	fi
    fi
    echo "  Detected version $version... (Ctrl C to cancel)"
    sleep 2
    if [ -d "$src_path" ]; then
	echo "Committing $parent_name-$version to '$repo_url'..."
	# NOTE: --exclude DOES prevent deleting the directory on the
	# destination.
	new_source="$src_path"
	unzipped_sources="/tmp/simulate_git"
	if [ ! -d "$unzipped_sources" ]; then
	    mkdir $unzipped_sources || customDie "Cannot mkdir $unzipped_sources"
	fi
	unzipped_source="$unzipped_sources/Bucket_Game"
	if [ -d "$unzipped_source" ]; then
	    echo "Removing previous $unzipped_source..."
	    rm -Rf "$unzipped_source" || customDie "Cannot remove $unzipped_source"
	fi
	subproject_zip="$new_source/mtsrc/newline/Bucket_Game.zip"
	if [ ! -f "$subproject_zip" ]; then
	    customDie "ERROR: missing '$subproject_zip'"
	fi
	cd $unzipped_sources || customDie "Cannot cd $unzipped_sources"
	unzip "$subproject_zip"
	if [ ! -d "$unzipped_source" ]; then
	    customDie "ERROR: extracting $subproject_zip did not result in '$unzipped_source'"
	fi


	# echo "rsync -arc --delete --exclude .git \"$unzipped_source/\" \"$cloned_path\""
	if [ "@$enable_simulate" = "@false" ]; then
	    echo "sleep $sleep_count (Ctrl C to cancel)"
	    sleep $sleep_count
	    sleep_count=0
	    echo "# rsync ... $unzipped_source/ ..."
	    #rsync -avrc --delete --exclude .git "$new_source/" "$cloned_path"
	    rsync -arc --delete --exclude .git "$unzipped_source/" "$cloned_path"
	    # -c, --checksum              skip based on checksum, not mod-time & size
	else
	    echo "# rsync ... $unzipped_source/ ..."
	fi
	echo "cd \"$cloned_path\""
	cd "$cloned_path"
	let "done_count=done_count+1"
	echo "git add ..."

	if [ "@$enable_simulate" = "@false" ]; then
	    git ls-files -o --exclude-standard > ../$repo_name-$version-untracked.txt
	    git add --all || customDie "Could not git add --update (tracked files) in `pwd`"
	    # git add --update || customDie "Could not git add --update (tracked files) in `pwd`"
	    # git add $(git ls-files -o --exclude-standard)
	    # stage untracked [git add $(...)], fails with:
	    # fatal: pathspec 'mods/coderbuild/birthstones/etc/1.etc' did not match any files
	fi
	echo "git commit -m \"release-$version\""
	if [ "@$enable_simulate" = "@false" ]; then
	    git commit -m "release-$version" || customDie "Could not git commit -m \"$release-version\" in `pwd`"
	fi
	echo "git push origin master"
	if [ "@$enable_simulate" = "@false" ]; then
	    git push origin master || customDie "Could not push origin master in `pwd`"
	fi
	echo "# done in `pwd`"
    fi
}

if [ ! -z "$single_source" ]; then
    echo
    echo "Pushing $single_source..."
    push_source "$single_source" ""
else
    for version in 190204 190225 190315 190221 190313 190323
	push_source "$releases/$parent_name-$version" "$version"
    do
    done
    if [ "$done_count" -ne "$real_count" ]; then
	echo "WARNING: there are $real_count releases in $releases"
	echo " (not $done_count which were expected and added)"
    fi
fi
#echo "Remember to restart apache to get gitweb to read $repo_url/config and $repo_url/description:"
#echo "  sudo systemctl restart httpd"
echo "Remember if you have installed git-instaweb, you can get it to read the newly created $repo_url/config and $repo_url/description:"
echo "  sudo systemctl restart lighttpd"
echo "  cd $repos_url"
echo "  git instaweb"
# You can really clone that:
# cd $HOME/git || customDie "Cannot cd $HOME/git"
# git clone $HOME/localrepos/$repo_name.git $repo_name-2
# cd $repo_name-2
