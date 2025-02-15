#!/usr/bin/env python
from __future__ import print_function
import sys
import os
import argparse

if sys.version_info.major < 3:
    FileNotFoundError = IOError

SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(SCRIPTS_DIR)

sys.path.insert(0, REPO_DIR)

from linuxpreinstall.moreapt import (
    get_package_files,
    get_packages,
)


def main():
    parser = argparse.ArgumentParser(description="Examine package lists.")
    parser.add_argument(
        "packages_file", nargs="?", help="The package file to examine."
    )

    args = parser.parse_args()

    # If no package file is specified, list files in /var/lib/apt/lists
    if not args.packages_file:
        try:
            files = get_package_files()
            for f in files:
                print(f)
            print("Specify one of the package files above to list packages from the repo.")
            print("ppa-examine <packages file>")
            return 1
        except FileNotFoundError as e:
            print("Error:", e)
            return 2

    # If a package file is specified, read and process it
    try:
        packages = get_packages(args.packages_file)
        for package in packages:
            print(package)
        return 0
    except FileNotFoundError as e:
        print("Error:", e)
        return 3

if __name__ == "__main__":
    sys.exit(main())
