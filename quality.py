#!/usr/bin/env python
import os
import sys

FLAG_NAME = "api.rc"
REPO_DIR = os.path.realpath(".")
FLAG_PATH = os.path.join(REPO_DIR, "api.rc")
issuesByType = {}
if not os.path.isfile(FLAG_NAME):
    print("You must run {} from the linux-preinstall directory."
          " {} is not here.".format(sys.argv[0], FLAG_NAME))
    exit(1)

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
    print("#{} files:".format(key))
    for issue in issues:
        print(issue)
        issueCount += 1
if len(issuesByType.keys()) > 0:
    print("There were {} issue(s) in {} files (Checking any other file types in this directory tree is not implemented)."
          "".format(issueCount, issuesByType.keys()))
else:
    print("No files matching the types were found.")
