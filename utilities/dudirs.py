#!/usr/bin/env python3
"""
Only checks the size of subdirectories (not files) in a given directory.
See https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
"""
from __future__ import print_function
from __future__ import division

import os
import sys

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for sub in filenames:
            sub_path = os.path.join(dirpath, sub)
            # skip if it is symbolic link
            if not os.path.islink(sub_path):
                total_size += os.path.getsize(sub_path)

    return total_size

def main():
    root_path = "."
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
    total_mb = 0.0
    for sub in os.listdir(root_path):
        sub_path = os.path.join(root_path, sub)
        if os.path.isdir(sub_path) and not sub.startswith("."):
            sub_size = get_size(sub_path)
            total_mb += sub_size/1024.0/1024.0
            print("{}: {}".format(sub_path, sub_size))
    print("{}: {}".format("TOTAL", "{} M".format(total_mb)))

if __name__ == "__main__":
    main()
