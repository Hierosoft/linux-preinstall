#!/usr/bin/env python3
import os
import sys
import magic
m = None

def find_mime(mt, parent="", partial=True, show=True,
        hide_root=None, hide_root_as=None, show_dot_hidden=True):
    '''
    Find files by MIME Type recursively.

    Sequential arguents:
    mt -- Find this MIME Type
    partial -- If true, allow partial matches, such as if mt is image,
        find all files where the MIME Type contains "image"
    parent -- Specify the starting directory. If "", the
        directory will be used as root and will never be shown in the
        output. If it starts with "." (including "..") or is a relative
        path, the root directory will be shown starting with that (The
        absolute path will not be calculated).
    hide_root -- This is generated automatically (See parent). *
    hide_root_as -- This is generated automatically (See parent). *
    show_dot_hidden -- Check directories and files starting with "." *
    show -- * Params marked with * only apply when this is True. If
        True, display each file to standard output (The format will be
        similar to the GNU "find" command.
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


def main():
    if len(sys.argv) < 2:
        raise ValueError('You must specify a full/partial mime type'
                         'such as "jpeg" or "image".')
    mt = sys.argv[1]
    results = find_mime(mt)

if __name__ == "__main__":
    main()
