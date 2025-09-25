#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
import argparse

if sys.version_info.major < 3:
    FileNotFoundError = IOError

SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(SCRIPTS_DIR)

sys.path.insert(0, REPO_DIR)

from linuxpreinstall.logging2 import getLogger

from linuxpreinstall.moreapt import (
    get_package_files,
    get_packages,
)

logger = getLogger(__name__)


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
            print("Specify one of the package files above (or substring) to list packages from the repo(s).")
            print("ppa-examine <packages file>")
            return 1
        except FileNotFoundError as e:
            print("Error:", e)
            return 2

    # If a package file is specified, read and process it
    try:
        results = get_packages(args.packages_file)
        packages = results.get('packages')
        errors = results.get('errors')
        if not packages:
            logger.warning("No package lines found in {}"
                           .format(repr(args.packages_file)))
            return 0
        names = []
        repos = set()
        for package, repo in packages:
            print(package, " # from", repr(repo), file=sys.stderr)
            names.append(package)
            repos.add(repo)
        print(file=sys.stderr)
        print("# Lists dir: {}".format(results.get('lists_dir')), file=sys.stderr)
        print("# Repos: {}".format(" ".join(repos)), file=sys.stderr)
        print("# Packages:", file=sys.stderr)
        if names:
            print(" ".join(names))
        if errors:
            for error in errors:
                logger.error(error)
        return 0
    except FileNotFoundError as e:
        print("Error:", e)
        return 3


if __name__ == "__main__":
    sys.exit(main())
