# -*- coding: utf-8 -*-
import os
import shlex
import sys

if not hasattr(shlex, "join"):
    # NOTE: shlex.join requires Python 3.8,
    #   so polyfill that.
    def shlex_join(parts):
        if isinstance(parts, tuple):
            parts = list(parts)  # allow item assignment
        for i in range(len(parts)):
            if " " in parts[i]:
                parts[i] = parts[i].replace("'", "\\'")
                parts[i] = "'{}'".format(parts[i])
        return " ".join(parts)

    shlex.join = shlex_join
# else:
#     from shlex import join as shlex_join


from collections import OrderedDict

from linuxpreinstall.lplogging import (
    human_readable,
)

from linuxpreinstall.lplogging import (
    echo0,
)

from linuxpreinstall.bash import compare_files


class DupSet():
    """A duplicate comparison state.

    Attributes:
        names (set[str]): A set of names that has been found so far.
        dup_paths (dict[set[str]]): Key is parent, and set contains duplicate relative paths.
    """
    def __init__(self):
        self._mode = None
        self._last_memory_s = None
        self._last_memory_count = 0
        self.names = OrderedDict()
        self.sizes = {}
        self.dup_paths = {}
        self.memory_count = 0
        self.dup_count = 0
        self.dup_size = 0

    def print_summary(self, prefix="# "):
        echo0(prefix+'memory use: {}'
              .format(human_readable(self.memory_count)))
        echo0(prefix+'duplicate count: {}'
              .format(self.dup_count))
        if self.dup_size:
            echo0(prefix+'duplicate data total: {}'
                  .format(human_readable(self.dup_size)))

    def check(self, parent, follow_symlinks=False, match_fn=None,
              prefix="# "):
        """Resursively check parent for filenames
        and output relative paths of duplicate files as standard output.

        Args:
            match_fn (function): Function to compare two files given
                two path strings. Defaults to
                from linux_preinstall.bash import compare_files.
            prefix (str): Prefix to place before STDERR lines
                (just as a visual aid--only real duplicates go to
                STDOUT).
        """
        if not match_fn:
            match_fn = compare_files
        self.dup_paths[parent] = set()
        self._check(parent, "",
                    follow_symlinks=follow_symlinks,
                    match_fn=match_fn,
                    prefix=prefix)

    def _check(self, root, rel, follow_symlinks=False, match_fn=None,
               prefix=None):
        # ^ pass *all* args to recursion (but some will be new)!
        if self._mode and (self._mode != "content"):
            raise RuntimeError(
                "\"content\" mode can't be run on a \"{}\" mode DupSet."
                .format(self._mode)
            )
        self._mode = "content"
        # Folders:
        if rel:
            parent = os.path.join(root, rel)
        else:
            # avoid adding extra trailing slash
            parent = root
        for sub in os.listdir(parent):
            sub_path = os.path.join(parent, sub)
            if not follow_symlinks and os.path.islink(sub_path):
                continue
            if os.path.isfile(sub_path):
                continue
            # join doesn't add extra slash if *1st* is blank, so:
            self._check(root, os.path.join(rel, sub),
                        follow_symlinks=follow_symlinks,
                        match_fn=match_fn,
                        prefix=prefix)
        # Files (shallow last, so less organized ones are listed dups):
        for sub in os.listdir(parent):
            sub_path = os.path.join(parent, sub)
            if not follow_symlinks and os.path.islink(sub_path):
                continue
            if os.path.isdir(sub_path):
                continue
            size = os.stat(sub_path).st_size
            # if sub in self.names:
            if size in self.sizes:
                for base in self.sizes[size]:
                    if match_fn(sub_path, base):
                        rel_sub = os.path.join(rel, sub)
                        self.dup_paths[root].add(rel_sub)
                        self.dup_count += 1
                        self.dup_size += size
                        self.memory_count += sys.getsizeof(rel_sub)
                        print(shlex.join([sub_path, base]))
                        break
                self.sizes[size].append(sub_path)  # *after* check all
                self.memory_count += sys.getsizeof(sub_path)
                # found duplicate
                # rel_sub = os.path.join(rel, sub)
                # self.dup_paths[root].add(rel_sub)
                # self.dup_count += 1
                # self.memory_count += sys.getsizeof(rel_sub)
                # echo0(prefix+'memory use: {}'.format(human_readable(self.memory_count)))
            else:
                # There is no file of this size yet, so it can't be a
                #   match (so add it so other files of the same size
                #   will be compared to it).
                self.sizes[size] = []
                self.sizes[size].append(sub_path)
                self.memory_count += sys.getsizeof(sub_path)
                # self.names[sub] = sub_path
                # self.memory_count += sys.getsizeof(sub)

            memory_s = human_readable(self.memory_count, places=1)
            # if memory_s != self._last_memory_s:
            if self.memory_count - self._last_memory_count > 1000000:
                echo0(prefix+'memory use: {}'.format(memory_s))
                self._last_memory_s = memory_s
                self._last_memory_count = self.memory_count


    def check_names(self, parent, follow_symlinks=False, prefix="# "):
        """Resursively check parent for *filenames*
        and output relative paths of files with same *filenames* as
        standard output.
        """

        self.dup_paths[parent] = set()
        self._check_names(parent, "",
                    follow_symlinks=follow_symlinks,
                    prefix=prefix)

    def _check_names(self, root, rel, follow_symlinks=False, prefix=None):
        # ^ pass *all* args to recursion (but some will be new)!
        if self._mode and (self._mode != "name"):
            raise RuntimeError(
                "\"name\" mode can't be run on a \"{}\" mode DupSet."
                .format(self._mode)
            )
        self._mode = "name"

        # Folders:
        if rel:
            parent = os.path.join(root, rel)
        else:
            # avoid adding extra trailing slash
            parent = root
        for sub in os.listdir(parent):
            sub_path = os.path.join(parent, sub)
            if not follow_symlinks and os.path.islink(sub_path):
                continue
            if os.path.isfile(sub_path):
                continue
            # join doesn't add extra slash if *1st* is blank, so:
            self._check_names(root, os.path.join(rel, sub),
                              follow_symlinks=follow_symlinks,
                              prefix=prefix)
        # Files (shallow last, so less organized ones are listed dups):
        for sub in os.listdir(parent):
            sub_path = os.path.join(parent, sub)
            if not follow_symlinks and os.path.islink(sub_path):
                continue
            if os.path.isdir(sub_path):
                continue
            if sub in self.names:
                # found duplicate
                # rel_sub = os.path.join(rel, sub)
                # self.dup_paths[root].add(rel_sub)
                self.dup_count += 1
                # self.memory_count += sys.getsizeof(rel_sub)
                # echo0(prefix+'memory use: {}'.format(human_readable(self.memory_count)))
                print(shlex.join([sub_path, self.names[sub]]))
            else:
                self.names[sub] = sub_path
                self.memory_count += sys.getsizeof(sub)

            memory_s = human_readable(self.memory_count, places=1)
            # if memory_s != self._last_memory_s:
            if self.memory_count - self._last_memory_count > 1000000:
                echo0(prefix+'memory use: {}'.format(memory_s))
                self._last_memory_s = memory_s
                self._last_memory_count = self.memory_count
