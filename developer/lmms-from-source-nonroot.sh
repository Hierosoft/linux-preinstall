#!/bin/bash

if [ -z "$COMBINED_ERR_PATH" ]; then
    COMBINED_ERR_PATH="/tmp/lmms-from-source-errors.txt"
fi

customCleanup() {
    if [ -f "$COMBINED_ERR_PATH" ]; then
        echo "* removing \"$COMBINED_ERR_PATH\"..."
        rm "$COMBINED_ERR_PATH"
    fi
    if [ ! -z "$BUILD_PATH" ]; then
        if [ -f "$BUILD_PATH/CMakeCache.txt" ]; then
            echo "Removing \"$BUILD_PATH/CMakeCache.txt\" as per cmake failure specifies as of 2020-03-13."
            rm "$BUILD_PATH/CMakeCache.txt"
        fi
    fi
}

customErr() {
    # If param 2 is set, exit $2.
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    if [ ! -z "$2" ]; then
        exit $2
    fi
}

customDie() {
    # End program (by adding param 2 so that customErr will exit).
    errorCode=1
    if [ ! -z "$2" ]; then
        errorCode=$2
    fi
    customErr "$1" $errorCode
}

customShutdown() {
    customErr "$1"
    errorCode=1
    if [ ! -z "$2" ]; then
        errorCode=$2
    fi
    if [ ! -z "$BUILD_PATH" ]; then
        if [ -f "$BUILD_PATH/CMakeCache.txt" ]; then
            echo "Removing \"$BUILD_PATH/CMakeCache.txt\" as per cmake failure specifies as of 2020-03-13."
            rm "$BUILD_PATH/CMakeCache.txt"
        fi

        TRY_PATH="$BUILD_PATH/CMakeFiles/CMakeOutput.log"
        if [ -f "$COMBINED_ERR_PATH" ]; then
            rm "$COMBINED_ERR_PATH" || customDie "rm \"$COMBINED_ERR_PATH\" failed."
        fi
        touch "$COMBINED_ERR_PATH" || customDie "touch \"$COMBINED_ERR_PATH\" failed."

        FOUND_ERR_PATHS=""
        if [ -f "$TRY_PATH" ]; then
            cat "$TRY_PATH" >> "$COMBINED_ERR_PATH"
            FOUND_ERR_PATHS="$FOUND_ERR_PATHS '$TRY_PATH'"
        fi
        TRY_PATH="$BUILD_PATH/CMakeFiles/CMakeError.log"
        if [ -f "$TRY_PATH" ]; then
            cat "$TRY_PATH" >> "$COMBINED_ERR_PATH"
            FOUND_ERR_PATHS="$FOUND_ERR_PATHS '$TRY_PATH'"
        fi
        if [ -f "`command -v outputinspector`" ]; then
            # cd "$BUILD_PATH"
            if [ ! -z "$FOUND_ERR_PATHS" ]; then
                echo "Current Directory: \"`pwd`\""
                # echo "Running outputinspector \"$COMBINED_ERR_PATH\"..."
                # outputinspector "$COMBINED_ERR_PATH" &
                sleep 5
            else
                echo "There are no errors in: $FOUND_ERR_PATHS."
            fi
            customCleanup
        else
            customCleanup
            exit $errorCode  # SKIP the following:
            cat <<END
If you have output inspector, this script would call it so you could read the
output and double-click errors to view the relevant
source code:

  https://github.com/poikilos/outputinspector

END
        fi
    fi
    exit $errorCode
}

if [ -z "$CMAKE_INSTALL_PREFIX" ]; then
    CMAKE_INSTALL_PREFIX="$HOME/.local"
fi
SRC="$HOME/src"
if [ ! -d "$SRC" ]; then
    mkdir -p $SRC || "mkdir -p \"$SRC\" failed."
fi
cd "$SRC" || customDie "cd \"$SRC\" failed in `pwd`."


# See <https://github.com/LMMS/lmms/wiki/Compiling#clone-source-code>
REMOTE_REPO_USER="lmms"
REMOTE_REPO_NAME="lmms"
REPO_URL="https://github.com/$REMOTE_REPO_USER/$REMOTE_REPO_NAME"
LOCAL_REPO_NAME="$REMOTE_REPO_NAME"
LOCAL_REPO="$SRC/$LOCAL_REPO_NAME"
if [ ! -d "$LOCAL_REPO" ]; then
    cd "$SRC" || customDie "cd \"$SRC\" failed in `pwd`."
    git clone --recurse-submodules -b master https://github.com/lmms/lmms || customDie "git clone \"$REPO_URL\" failed in `pwd`."
    # git clone "$REPO_URL" "$LOCAL_REPO" || customDie "git clone \"$REPO_URL\" failed in `pwd`."
    cd "$LOCAL_REPO" || customDie "cd \"$LOCAL_REPO\" failed after clone in `pwd`."
else
    cd "$LOCAL_REPO" || customDie "cd \"$LOCAL_REPO\" failed in `pwd`."
    git pull --all || customDie "git pull failed in `pwd`."
    # TODO: Ensure that we pull the same version as the supermodule.
    # - The above may not bring the submodules up to date with the
    #   supermodule's version of them.
    # git pull --recurse-submodules
    # git submodule update --remote --recursive  # This may update PAST
    #                                            # the supermodule's
    #                                            # version
    #                                            # (not recommended)
fi
echo "Using `pwd`..."
BUILD_PATH="$LOCAL_REPO/build"
if [ ! -d "$BUILD_PATH" ]; then
    mkdir -p "$BUILD_PATH" || "mkdir -p \"$BUILD_PATH\" failed."
fi
cd "$BUILD_PATH" || customDie "cd \"$BUILD_PATH\" failed in `pwd`."
# FORCE_VERSION=$(date "+%Y.%m.%d")  # zero-padded
FORCE_VERSION=$(date "+%Y.%-m.%-d")  # not zero-padded: "%-"
customCleanup
# It still says
# > Debug FP exceptions         : Disabled
# > -----------------------------------------------------------------
# > IMPORTANT:
# > after installing missing packages, remove CMakeCache.txt before
# > running cmake again!
# > -----------------------------------------------------------------
OpenGL_GL_PREFERENCE=GLVND
# VST requires wine, so set WANT_VST to OFF (otherwise it shows error if missing):
cmake "$LOCAL_REPO" -DCMAKE_INSTALL_PREFIX=$CMAKE_INSTALL_PREFIX -DFORCE_VERSION=$FORCE_VERSION -DWANT_VST=OFF -DOpenGL_GL_PREFERENCE=$OpenGL_GL_PREFERENCE || customShutdown "Compiling failed! See errors above"
#-DWANT_QT5=ON  results in:
#CMake Warning:
#  Manually-specified variables were not used by the project:
#
#    WANT_QT5

# make -j4
make -j$(nproc)
make install  # This installs to ~/.local as long as that is set above.
