#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import shutil
import subprocess
import sys

# ------------------------------------------------- settings -------------------------------------------------
USERS_TO_TRY = ["Hierosoft", "Poikilos"]
FORCE_GIT_DIR = os.path.expanduser(os.path.join("~", "git"))
# Set to None or empty string to clone into the same dir as this script
# ----------------------------------------------------------------------------------------------------------------

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(MODULE_DIR)
SCRIPT_DIRS = (
    os.path.join(REPO_DIR, "utilities-developer"),
    os.path.join(REPO_DIR, "utilities-server"),
    os.path.join(REPO_DIR, "utilities"),
)


if __name__ == "__main__":
    # Allow running this script directly
    #   (Edit path to find the module in the repo).
    sys.path.insert(0, REPO_DIR)

from linuxpreinstall.lpplatform import which_nearby_cmd
from linuxpreinstall.getrepo import main as getrepo_main


def main():
    # ------------------------------------------------------------------
    # Exact argument handling from the original script
    # ------------------------------------------------------------------
    if len(sys.argv) < 2:
        print("You must specify a repo name.")
        return 1

    repo_name = sys.argv[1]
    getrepo_args = sys.argv[1:]          # everything including repo name

    # ------------------------------------------------------------------
    # Check for git
    # ------------------------------------------------------------------
    if not which_nearby_cmd("git"):
        print("Error: git is not installed.")
        return 1

    # ------------------------------------------------------------------
    # Determine target directory (exactly like original)
    # ------------------------------------------------------------------
    if FORCE_GIT_DIR:
        repos_dir = os.path.abspath(FORCE_GIT_DIR)
        user_dir  = repos_dir
        if not os.path.isdir(repos_dir):
            try:
                os.makedirs(repos_dir)
            except OSError:
                print("Error: cannot create {0}".format(repos_dir),
                      file=sys.stderr)
                return 1
    else:
        repos_dir = os.path.dirname(REPO_DIR)
        user_dir = repos_dir

    for username in USERS_TO_TRY:
        cmd = (["getrepo"] + getrepo_args +
               ["--user", username,
                "--repos_dir", repos_dir,
                "--user_dir",  user_dir])
        sys.argv[:] = cmd
        code = getrepo_main()
        if code == 0:
            print("getrepo returned success.")
            return 0

    return code


def getrepo_cmd(username):
    # Resolve getrepo path only when we actually need to run it
    getrepo_path = which_nearby_cmd("getrepo")
    if not getrepo_path:
        print("Error: getrepo not found.", file=sys.stderr)
        return 1
    cmd[0] = getrepo_path
    py_cmd = []
    if sys.platform.startswith("win"):
        py_cmd = ["py", "-3"]
        if not shutil.which(py_cmd[0]):
            py_cmd = ["python3"]
        if not shutil.which(py_cmd[0]):
            py_cmd = ["python"]
    cmd = py_cmd + cmd

    print("Trying {0}...".format(username))
    print('calling: {}'.format(cmd))
    code = subprocess.call(cmd)

    if code == 0:
        print("getrepo returned success.")
        return 0

    return code   # last exit code (non-zero)


if __name__ == "__main__":
    sys.exit(main())