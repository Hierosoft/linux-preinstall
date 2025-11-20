#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
thumbnails
----------
Process thumbnails from XDG desktops.

If this file runs directly, the default action is to delete the
thumbnail from ~/.cache/thumbnails (the large or normal directory) so
it will be regenerated.

Usage:
thumbnails <filename1 [, filename2, ...]> [options]

Examples:
  thumbnails some_filename.stl
    # ^ (default action) Delete the cached thumbnail in ~/.cache
  thumbnails *.obj
    # ^ Clear thumbnails for all obj files the current directory.
  thumbnails some_filename.stl --view
    # ^ Open the thumbnail (not file) in the default viewer via xdg-open
    #   only if such a thumbnail already exists.

'''
from __future__ import print_function
import os
import sys
import platform
# import shutil
import subprocess
if sys.version_info.major >= 3:
    # import pathlib
    from urllib.parse import quote
    # ^ quote does too much
    # from pathlib import Path
else:
    from urllib import quote
    # import pathlib2 as pathlib
    # from pathlib2 import Path
    # ^ This backport is not included
    #   (See <https://pypi.org/project/pathlib2/>)
# ^ See https://stackoverflow.com/a/9345102/4541104
import hashlib
BUF_SIZE = 65536

HOME = None
if platform.system() == "Windows":
    HOME = os.environ['USERPROFILE']
else:
    HOME = os.environ['HOME']

if __name__ == "__main__":
    MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, os.path.dirname(MODULE_DIR))

from linuxpreinstall.lplogging import (  # noqa: E402
    echo0,
)

import linuxpreinstall.logging2 as logging  # noqa: E402
from linuxpreinstall.logging2 import getLogger  # noqa: E402


logger = getLogger(__name__)


def usage():
    echo0("thumbnails")
    echo0("----------")
    echo0(__doc__+"\n")


def str_to_hexdigest(value):
    md5Hash = hashlib.md5(value.encode())
    # ^ The following don't produce the same hash as perl Digest::MD5:
    #   encode("utf-8")
    #   encode()  # same as "utf-8"
    return md5Hash.hexdigest()


def to_perl_uri(path):
    '''
    Mimic Perl to match the GNU desktop behavior
    (The %27 isn't encoded by Perl).
    same as:
    perl -MURI::file -MDigest::MD5=md5_hex -e \
    'printf "%s.png\n", md5_hex(URI::file->new(shift))' \
    "$path"
    as per https://unix.stackexchange.com/a/91334/343286
    where $path has spaces and special characters but Perl converts
    the path to a URL before running md5_hex (verified: Perl
    produces the same name as the OS).
    '''
    # return Path(path).as_uri().replace("%27", "'")
    # ^ Python 3 (requires from pathlib import path)
    return "file://"+quote(path).replace("%27", "'")


def file_to_hexdigest(path):
    # See <https://stackoverflow.com/a/22058673/4541104>
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
    return md5.hexdigest()


def get_thumbnails(src_path):
    results = []
    raw_path = src_path
    src_path = os.path.abspath(raw_path)
    # src_path = quote_plus(src_path)
    # ^ This won't work--it encodes slashes. It is for names not paths.
    # dstName = file_to_hexdigest(src_path) + ".png"
    src_path = to_perl_uri(src_path)
    dstName = str_to_hexdigest(src_path) + ".png"
    thumbsPath = os.path.join(HOME, ".cache", "thumbnails")
    thumbSubs = ["large", "normal"]   # there is also "fail/$progname"
    for thumbSub in thumbSubs:
        thumbPath = os.path.join(thumbsPath, thumbSub, dstName)
        if os.path.isfile(thumbPath):
            results.append(thumbPath)
        else:
            logger.warning(
                '* There is no "{}" for "{}".'.format(thumbPath, src_path))
    return results


def main():
    paths = []
    mode = "delete"  # Delete the cached thumbnail.
    for argI in range(1, len(sys.argv)):
        arg = sys.argv[argI]
        if arg.startswith("--"):
            if arg == "--verbose":
                logging.basicConfig(logging.INFO)
            elif arg == "--debug":
                logging.basicConfig(logging.DEBUG)
            elif arg == "--view":
                mode = "view"
            else:
                logger.error('The argument "{}" is invalid.'.format(arg))
                return 2
        elif os.path.isfile(arg):
            paths.append(arg)
        else:
            logger.error('"{}" is not a file.'.format(arg))
            return 3
    if len(paths) < 1:
        usage()
        logger.error('You must specify at least one thumbnail-able file.')
        return 1
    for src_path in paths:
        for thumbPath in get_thumbnails(src_path):
            # print(thumbPath)
            if mode == "view":
                print('xdg-open "{}"'.format(thumbPath))
                subprocess.call(["xdg-open", thumbPath])
                # ^ subprocess.run is only for Python 3.
            elif mode == "delete":
                print('rm "{}"'.format(thumbPath))
                os.remove(thumbPath)


if __name__ == "__main__":
    sys.exit(main())
