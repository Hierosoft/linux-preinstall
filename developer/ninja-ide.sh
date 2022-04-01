#!/bin/bash
echo "* Try samurai-ide instead for an updated fork (samurai-ide.sh), otherwise pass --force."
if [ "@$1" != "--force" ]; then
    exit 0
fi

#!/bin/bash
REPO_USER="ninja-ide"
REPOS_DIR="$HOME/Downloads/git/$REPO_USER"
REPO_NAME="ninja-ide"
module_name="ninja_ide"
ExecName="ninja-ide.py"
if [ -d "$HOME/git/ninja-ide" ]; then
    REPOS_DIR=~/git
else
    mkdir -p $REPOS_DIR
fi
if [ $? -ne 0 ]; then exit; fi
cd "$REPOS_DIR"
if [ $? -ne 0 ]; then exit; fi
REPO_PATH="$REPOS_DIR/$REPO_NAME"
# git clone git://github.com/$REPO_USER/$REPO_NAME.git
# ^ Use https:// instead, since git:// causes:
# > Cloning into '$$REPO_NAME'...
# > fatal: remote error:
# >   The unauthenticated git protocol on port 9418 is no longer supported.
# > Please see https://github.blog/2021-09-01-improving-git-protocol-security-github/ for more information.
if [ ! -d "$REPO_PATH" ]; then
    git clone https://github.com/$REPO_USER/$REPO_NAME.git "$REPO_PATH"
    if [ $? -ne 0 ]; then exit; fi
    cd "$REPO_PATH"
    if [ $? -ne 0 ]; then exit; fi
else
    cd "$REPO_PATH"
    if [ $? -ne 0 ]; then exit; fi
    git pull --ff-only
    if [ $? -ne 0 ]; then exit; fi
fi
if [ $? -ne 0 ]; then exit; fi
echo "* installing requirements from `realpath requirements.txt`"
python3 -m pip install --user -r requirements.txt
# ^ -r avoids:
# > ERROR: Could not find a version that satisfies the requirement requirements.txt (from versions: none)
# > HINT: You are attempting to install a package literally named "requirements.txt" (which cannot exist). Consider using the '-r' flag to install the packages listed in requirements.txt
# > ERROR: No matching distribution found for requirements.txt
# ^ --user avoids "Defaulting to user installation because normal site-packages is not writeable"
if [ $? -ne 0 ]; then exit; fi
if grep -q "FIXME: when LSP works, delete this" $module_name/intellisensei/python_intellisense.py; then
    echo "Your `realpath $module_name/intellisensei/python_intellisense.py` file has \"FIXME: when LSP works, delete this\" so it needs jedi. Installing python3 jedi..."
    python3 -m pip install --user jedi
else
    echo "Your `realpath $module_name/intellisensei/python_intellisense.py` file doesn't contain \"FIXME: when LSP works, delete this\" so it apparently doesn't need jedi."
fi
echo "* Now you can try to run:"
echo "  `realpath $ExecName`"
# python3 $ExecName
# exit $?
