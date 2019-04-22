#!/bin/bash
cat <<EOF
This script is unused since all the sourcecode in these directories is
zipped. Try make-localhost-git-Bucket_Game.sh instead."
EOF
exit 1
customDie() {
    echo
    echo "ERROR:"
    echo "  $@"
    #echo "  $1"
    echo
    echo
    exit 1
}
simulate=false
if [ "@$1" = "@--simulate" ]; then
    simulate=true
fi
me=`basename $0`
repo_name=linux-minetest-kit
# based on Jan Kruger "answered Dec 2 '13 at 13:04" Retrieved from https://stackoverflow.com/questions/20325089/hosting-a-git-server-on-localhost 2018-03-26
repo_url="$HOME/localrepos/$repo_name.git"
clones_path=$HOME/git
echo
echo
echo "$me recreates the git commit history on the 'server' as a local git repository directory $repo_url, by cloning to (and pushing several commits from) '$clones_path'."
mkdir -p "$repo_url" || customDie "Cannot mkdir $repo_url"
cd $repo_url || customDie "Cannot cd $repo_url"
git init --bare
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
    customDie "
The repo was already recreated. You will have to run:
    rm -Rf $repo_url && rm -Rf $cloned_path
    # to try again.
"
    #cd $repo_name || customDie "Cannot cd $repo_name"
    #git pull
    #cloned_path="`pwd`"
fi
if [ ! -d "$cloned_path" ]; then
    customDie "git could not create $cloned_path from $repo_url"
fi
releases="/home/owner/git/EnlivenMinetest/webapp/minetest-versions"
done_count=0
real_count=`ls -1 $releases | wc -l`
if [ "@$simulate" = "@false" ]; then
    echo "Processing commands..."
else
    echo "Simulating commands..."
fi
for version in 190204 190225 190315 190221 190313 190323
do
    if [ -d "$releases/linux-minetest-kit-$version" ]; then
	echo "Committing linux-minetest-kit-$version to '$repo_url'..."
	# NOTE: --exclude DOES prevent deleting the directory on the
	# destination.
	new_source="$releases/linux-minetest-kit-$version"
	echo "rsync -arc --delete --exclude .git \"$new_source/\" \"$cloned_path\""
	if [ "@$simulate" = "@false" ]; then
	    echo "sleep 2 (Ctrl C to cancel)"
	    sleep 2
	    rsync -arc --delete --exclude .git "$new_source/" "$cloned_path"
	fi
	let "done_count=done_count+1"
	cd "$cloned_path"
	echo "git add -A"
	if [ "@$simulate" = "@false" ]; then
	    git add -A
	fi
	echo "git commit -m \"release-$version\""
	if [ "@$simulate" = "@false" ]; then
	    git commit -m "release-$version"
	fi
	echo "git push origin master"
	if [ "@$simulate" = "@false" ]; then
	    git push origin master
	fi
    fi
done
if [ "$done_count" -ne "$real_count" ]; then
    echo "WARNING: there are $real_count releases in $releases"
    echo " (not $done_count which were expected and added)"
fi
# cd ..
# git clone $HOME/localrepos/$repo_name.git linux-minetest-kit2
# cd linux-minetest-kit2
# wow, all my files are here
