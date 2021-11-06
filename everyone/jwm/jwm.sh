#!/bin/bash
cat <<END
2021-11-04 IRC PM
<Poikilos> There is one other thing with jwm: (I'm pretty sure it started happening when I switched from the devuan version to compiled) Maximizing a window or putting a game into full screen mode spans both of my monitors so it is split in two, instead of using the screen where it was started.
<Poikilos> The same actually happens to jwm itself now too: I have to set the width to 1920 or the bottom panel will be split onto both screens.
<Poikilos> I switched from sddm to lightdm recently but that didn't resolve the issue.
<Poikilos> I can't find any answers or even questions about it online. I posted in issue in the jwm repo weeks ago but got no replies.
<OldCoder> r
<OldCoder> Build it w/several features disabled
<OldCoder> and it should work
<OldCoder> Minute
<OldCoder> In fact, you need to do this regardless
<OldCoder> There's a memory leak and this will fix it...
<OldCoder> git clone https://github.com/joewing/jwm.git
<OldCoder> cd jwm
<OldCoder> ./autogen.sh
<OldCoder> ./configure --disable-xrender --disable-xinerama --disable-xmu --disable-shape
...
<OldCoder> make
<OldCoder> make install
END

REPO_USER=joewing
REPO_NAME=jwm
REPOS_PATH=~/Downloads/git/$REPO_USER
REPO_PATH=~/Downloads/git/$REPO_USER/$REPO_NAME
REPO_URL=https://github.com/$REPO_USER/$REPO_NAME.git

mkdir -p $REPOS_PATH \
    && cd $REPOS_PATH
if [ $? -ne 0 ]; then exit 1; fi
if [ ! -d "$REPO_PATH" ]; then
    git clone $REPO_URL $REPO_PATH
    if [ $? -ne 0 ]; then exit 1; fi
    cd $REPO_PATH
    if [ $? -ne 0 ]; then exit 1; fi
else
    cd $REPO_PATH
    if [ $? -ne 0 ]; then exit 1; fi
    git pull --no-rebase --verbose
    if [ $? -ne 0 ]; then exit 1; fi
fi
cd jwm
if [ $? -ne 0 ]; then
    echo "Error: The Joe's Window Manager repo is expected to have a jwm directory but 'cd jwm' failed in \"`pwd`\"."
    exit 1
fi
./autogen.sh
if [ $? -ne 0 ]; then exit 1; fi
./configure --disable-xrender --disable-xinerama --disable-xmu --disable-shape
if [ $? -ne 0 ]; then exit 1; fi
make
if [ $? -ne 0 ]; then exit 1; fi
make install

if [ $? -ne 0 ]; then
    echo "Error: make install failed. Ensure you're running as root."
else
    cat <<END
<Poikilos> Ok, recompiling as shown above didn't solve the issue.
<Poikilos> I found out how to add jwm to the sessions selection in DMs though: https://ubuntuforums.org/showthread.php?t=919534
<Poikilos> (I just changed it to use /usr/local/bin/jwm)
END
fi
echo "* An example ~/.jwmrc file from OldCoder requires laclin in some cases such as icon paths, but if you add other icon and program paths you can modify it and use it:"
echo "  jwmrc_from_oldcoder.org.txt"
