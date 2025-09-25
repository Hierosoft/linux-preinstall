#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
findmime
--------
Specify a full/partial MIME type such as "jpeg" or "image"
and list all matching files recursively.

Usage:
findmime.py <full or partial MIME type>

Example:
findmime.py jpeg
"""
import os
import sys
import magic
m = None


def find_mime(mt, parent="", partial=True, show=True,
              hide_root=None, hide_root_as=None, show_dot_hidden=True):
    '''Find files by MIME Type recursively.

    Args:
        mt (str): Find this MIME Type
        partial (Optional[bool]): If true, allow partial matches, such
            as if mt is image, find all files where the MIME Type
            contains "image"
        parent (Optional[str]): Specify the starting directory. If "",
            the directory will be used as root and will never be shown
            in the output. If it starts with "." (including "..") or is
            a relative path, the root directory will be shown starting
            with that (The absolute path will not be calculated).
        hide_root (Optional[str]): Do not set this, generally: This is
            generated automatically (See parent).
        hide_root_as (Optional[bool]): Do not set this, generally: This
            is generated automatically (See parent).
        show (Optional[bool]): "*" Params marked with "*" only apply
            when this is True. If True, display each file to standard
            output (The format will be similar to the GNU "find"
            command.
        show_dot_hidden (Optional[bool]): Check directories and files
            starting with "."
    '''
    results = []
    global m
    if m is None:
        m = magic.open(magic.MAGIC_MIME)
        m.load()
    if parent == "":
        parent = os.path.abspath(".")
        hide_root = parent + os.path.sep
        hide_root_as = ""
    for sub in os.listdir(parent):
        subPath = os.path.join(parent, sub)
        if not show_dot_hidden:
            if sub.startswith("."):
                continue
        if os.path.isdir(subPath):
            results += find_mime(
                mt, parent=subPath, partial=partial, show=show,
                hide_root=hide_root, hide_root_as=hide_root_as,
                show_dot_hidden=show_dot_hidden,
            )
            continue
        gotMT = m.file(subPath)
        if mt.lower() in gotMT.lower():
            results.append(subPath)
            if show:
                print(subPath)
    return results


def usage():
    print(__doc__, file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        usage()
        print("Error: You must specify a full or partial mimetype.",
              file=sys.stderr)
    mt = sys.argv[1]
    _ = find_mime(mt)
    # ^ _ for disposable value by convention (show=True by default, so
    #   output was already shown).
    return 0


if __name__ == "__main__":
    sys.exit(main())
