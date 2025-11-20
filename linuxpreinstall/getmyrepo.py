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

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def which_nearby_cmd(name):
    """Return absolute path to command or None."""
    # 1. Standard lookup in PATH
    path = shutil.which(name)
    if path:
        return os.path.abspath(path)

    # 2. Exact extension lists and order as required
    if sys.platform.startswith("win"):
        extensions = [".bat", ".ps1", ".py", ".pyw"]
    else:
        extensions = ["", ".sh", ".py"]

    for ext in extensions:
        candidate = os.path.join(SCRIPT_DIR, name + ext)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return os.path.abspath(candidate)

    return None


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
        repos_dir = SCRIPT_DIR
        user_dir = SCRIPT_DIR

    # ------------------------------------------------------------------
    # Try each username exactly like the original script
    # ------------------------------------------------------------------
    for username in USERS_TO_TRY:
        cmd = (["getrepo"] + getrepo_args +
               ["--user", username,
                "--repos_dir", repos_dir,
                "--user_dir",  user_dir])
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