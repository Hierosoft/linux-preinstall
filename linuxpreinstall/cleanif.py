#!/usr/bin/env python
"""
Delete files and directories in delPath if they are in readRoot
recursively, but only delete directories that become empty.

You must specify two folders:
1: a folder with extra files to delete from here if they're in folder 2
2: a folder read as the list of original copies to only keep in itself

Usage:
  cleanif <delete_in_here> <if_in_here>

Example:
  cleanif dir_with_extra_copies_of_faraway_folder faraway_folder

"""
import os
import sys
# good = "/run/media/owner/BLACK16/"
# oops = "/run/media/owner/JGustafsonExt/"

from linuxpreinstall import prerr


def usage():
    prerr(__doc__)


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
    # delIf(oops, good)
    if len(sys.argv) != 3:
        usage()
        prerr("ERROR: You must specify one dir with extra files"
              " & one to be read for the original copies to keep.")
        exit(1)
    delif(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
