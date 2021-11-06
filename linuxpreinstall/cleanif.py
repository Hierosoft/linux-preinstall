#!/usr/bin/env python
import os
good = "/run/media/owner/BLACK16/"
oops = "/run/media/owner/JGustafsonExt/"


def delIf(delPath, readPath, readRoot=None):
    """Delete files and directories in delPath if they are in readRoot
    recursively, but only delete directories that become empty."""

    if readRoot is None:
        readRoot = readPath
    else:
        if readPath == readRoot:
            raise RuntimeError("readPath should not be readRoot: {}"
                               "".format(readRoot))
        if not readPath.startswith(readRoot):
            raise RuntimeError("readPath must start with readRoot.")
    for sub in os.listdir(readPath):
        if sub == ".":
            continue
        elif sub == "..":
            continue
        subPath = os.path.join(readPath, sub)
        delSubPath = os.path.join(delPath, sub)
        if os.path.isdir(subPath):
            if os.path.isdir(delSubPath):
                delIf(delSubPath, subPath, readRoot=readRoot)
                os.rmdir(delSubPath)
                # print("rmdir " + delSubPath)
                # print("")
        elif os.path.isfile(subPath):
            if os.path.isfile(delSubPath):
                try:
                    os.remove(delSubPath)
                except PermissionError:
                    print("# PermissionError:")
                    print("rm " + delSubPath)

def main():
    delIf(oops, good)
