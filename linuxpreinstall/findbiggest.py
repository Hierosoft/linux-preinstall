#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
import os
from collections import OrderedDict
import argparse

class DirectorySizeChecker:
    def __init__(self, directory, max_items=10):
        self.directory = directory
        self.max_items = max_items
        self.biggest = OrderedDict()  # To store the biggest files
        self.max_key = None
        self.min_key = None

    def _get_size(self, path):
        """Recursively get the size of a file or directory."""
        if os.path.isdir(path):
            total_size = 0
            for dirpath, _, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
            return total_size
        return os.path.getsize(path)

    def _add_to_collection(self, path, size):
        """Add file to the collection of the biggest files."""
        if len(self.biggest) < self.max_items:
            self.biggest[path] = size
            if self.max_key is None or size > self.biggest[self.max_key]:
                self.max_key = path
            if self.min_key is None or size < self.biggest[self.min_key]:
                self.min_key = path
        else:
            if size > self.biggest[self.min_key]:
                del self.biggest[self.min_key]
                self.biggest[path] = size
                self.min_key = min(self.biggest, key=self.biggest.get)

    def check_sizes(self):
        """Walk through the directory and find the biggest files."""
        for dirpath, _, filenames in os.walk(self.directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                size = self._get_size(filepath)
                self._add_to_collection(filepath, size)

def main():
    parser = argparse.ArgumentParser(description='Find the largest files in a directory.')
    parser.add_argument('directory', metavar='directory', type=str,
                        help='The directory to search for the largest files.')

    args = parser.parse_args()

    checker = DirectorySizeChecker(args.directory, max_items=10)
    checker.check_sizes()

    print("\nTop 10 biggest files in the directory (in MB):")
    for filepath, size in checker.biggest.items():
        print("{:<100} {:>10.2f} MB".format(filepath, size / (1024 * 1024)))

if __name__ == "__main__":
    main()
