#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, os.path.dirname(MODULE_DIR))

# import linuxpreinstall.logging2 as logging
# from linuxpreinstall.logging2 import getLogger
from linuxpreinstall import (
    echo0,
)

FLAG_NAME = "api.rc"
REPO_DIR = os.path.realpath(".")
FLAG_PATH = os.path.join(REPO_DIR, FLAG_NAME)
issuesByType = {}
if not os.path.isfile(FLAG_NAME):
    # Can't just use sys.path.insert, since rc needs to be found by scripts
    echo0("You must run {} from the linux-preinstall directory."
          " {} is not here.".format(sys.argv[0], FLAG_NAME))
    sys.exit(1)


def check_sh_quality(path):
    executable = os.access(path, os.X_OK)
    issues = issuesByType.get("sh")
    if issues is None:
        issuesByType["sh"] = []
        issues = issuesByType["sh"]
    if not executable:
        msg = "{}: not marked executable".format(path)
        issues.append(msg)


def check_parent(parent):
    for sub in os.listdir(parent):
        subPath = os.path.join(parent, sub)
        if os.path.isdir(subPath):
            check_parent(subPath)
            continue
        if sub.endswith(".sh"):
            check_sh_quality(subPath)


check_parent(REPO_DIR)
issueCount = 0
for key,issues in issuesByType.items():
    echo0("#{} files:".format(key))
    for issue in issues:
        echo0(issue)
        issueCount += 1
if len(issuesByType.keys()) > 0:
    echo0(
        "There were {} issue(s) in {} files"
        " (Checking any other file types"
        " in this directory tree is not implemented)."
        .format(issueCount, issuesByType.keys()))
else:
    echo0("No files matching the types were found.")
