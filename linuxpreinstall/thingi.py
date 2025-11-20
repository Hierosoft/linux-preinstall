#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
thingi
------
Gather and organize files from a zip file(s)

Usage:
  unthing <file1.zip [file2.zip ...]>

Example:
  unthing *.zip

If this script runs directly (as main):

Decompress specified zip file(s) as a single directory (Only create a
subdirectory if there is more files/directories than 1 in the root of
the zip).
'''
from __future__ import print_function
import os
import sys
from zipfile import ZipFile
import tempfile
import shutil
import shlex

if __name__ == "__main__":
    MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, os.path.dirname(MODULE_PATH))

from linuxpreinstall.lplogging import (  # noqa: E402
    echo0,
)

import linuxpreinstall.logging2 as logging

from linuxpreinstall.logging2 import (
    getLogger,
)

logger = getLogger(__name__)


def usage():
    echo0("unthing")
    echo0("-------")
    echo0(__doc__+"\n")


def unzip_unmess(src_path, dst_path):
    '''
    Unzip the file to dst_path, and only create a subdirectory under
    dst_path if there is more than one file or directory in the zip
    file.
    '''
    # See also SpooledTemporaryFile for in-memory operations
    #   (uses storage only if necessary)
    # with open(tmp.name, 'w') as f:
    code = 1
    oldName = None
    with tempfile.TemporaryDirectory() as tmp:
        tmpPath = tmp
        with ZipFile(src_path, 'r') as zipObj:
            echo0('* extracting to temporary folder "{}"'.format(tmpPath))
            zipObj.extractall(path=tmpPath)
            # ^ ZipFile.extractall args:
            #   path: destination path (None for working directory)
            #   members: list of members (None to extract all)
            #   pwd: zip password if any
            code = 0

        srcPath = tmpPath
        subs = list(os.listdir(tmpPath))
        if len(subs) < 1:
            raise IOError('There were no files nor directories in "{}"'
                          ''.format(src_path))
        elif len(subs) == 1:
            dstName = subs[0]
            srcPath = os.path.join(tmpPath, subs[0])
            logger.debug('* moving the sub "{}"'.format(srcPath))
        else:
            # Move the whole thing.
            dstName = os.path.splitext(os.path.split(src_path)[1])[0]
            logger.debug(
                '* moving the whole "{}" as "{}"'
                ' (The name may be processed further--see mv below)'
                .format(srcPath, dstName))
        uI = dstName.find("_")
        oldName = dstName
        if uI > -1:
            if dstName[:uI].isdigit():
                logger.debug(
                    'removing "{}" from "{}"'
                    .format(dstName[:uI],  dstName))
                dstName = dstName[uI+1:]
            else:
                logger.debug(
                    'isdigit({}): no'
                    .format(shlex.join([dstName[:uI], ])))
        else:
            logger.debug('"_" in {}: no'.format(shlex.join([dstName, ])))
        dstName = dstName.strip(" _").strip()
        # ^ strip again in case of unusual/unicode whitespace characters
        if dstName != oldName:
            echo0('* changed "{}" to "{}"'.format(oldName, dstName))

        echo0("* got {}".format(subs))

        dstSubPath = os.path.join(dst_path, dstName)

        if not os.path.exists(dstSubPath):
            # os.rename(srcPath, dstSubPath)
            # ^ raises 'OSError: [Errno 18] Invalid cross-device link:'
            shutil.move(srcPath, dstSubPath)
            print('mv "{}" "{}"'.format(srcPath, dstSubPath))
            # echo0('* extracted as "{}"'.format(dstSubPath))
        else:
            # shutil.move copies into it if it exists!
            logger.error(
                'Error: "{}" already exists,'
                ' so extracted files will be ignored.'
                .format(dstSubPath))
            code = 1
    srcName = os.path.split(src_path)[1]
    foundReadme = None
    dstReadme = "readme.md"
    tryReadmeName = os.path.splitext(srcName)[0] + ".md"
    tryReadmes = [
        tryReadmeName,
        os.path.join(os.path.dirname(src_path), tryReadmeName),
    ]
    for tryReadme in tryReadmes:
        if os.path.isfile(tryReadme):
            foundReadme = tryReadme
    if foundReadme is not None:
        trySubs = [
            os.path.join("files", "Poikilos"),
            os.path.join("files", "poikilos"),
        ]
        # ^ [0] will be created if None exist.
        nonIdealSubs = ["files"]
        trySubs += nonIdealSubs
        dstDocsPath = None
        dstDocs = None
        for trySub in trySubs:
            trySubPath = os.path.join(dstSubPath, trySub)
            if os.path.isdir(trySubPath):
                dstDocs = trySub
                dstDocsPath = trySubPath
                break
        if (dstDocsPath is None) or (dstDocs in nonIdealSubs):
            trySubPath = os.path.join(dstSubPath, trySubs[0])
            os.makedirs(trySubPath)
            print('mkdir -p "{}"'.format(trySubPath))
            dstDocsPath = trySubPath
        '''
        if dstDocsPath is None:
            echo('* there is no "{}" in the destination "{}"'
                 ' so "{}" will be moved to the destination itself'
                 ' (as "{}").'
                 ''.format(trySubs, dstSubPath, foundReadme, dstReadme))
            dstDocsPath = dstSubPath
        '''
        dstReadmePath = os.path.join(dstDocsPath, dstReadme)
        shutil.move(foundReadme, dstReadmePath)
        print('mv "{}" "{}"'.format(foundReadme, dstReadmePath))
    else:
        logger.warning(
            '* there is no "{}" here to move.'.format(tryReadmeName))

    return code


def main():
    paths = []
    # TODO: Keyword argument: in_place=True
    # in_place (bool): Use the location of the file as the destination
    #     directory.
    for argI in range(1, len(sys.argv)):
        arg = sys.argv[argI]
        if arg.startswith("--"):
            if arg == "--verbose":
                logging.basicConfig(level=logging.INFO)
            elif arg == "--debug":
                logging.basicConfig(level=logging.DEBUG)
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
        logger.error("You must specify at least one zip file.")
        return 1
    for path in paths:
        dst_path = os.getcwd()
        echo0('os.path.realpath(path): "{}"'.format(os.path.realpath(path)))
        echo0('os.getcwd(): "{}"'.format(os.getcwd()))
        echo0('os.path.join(os.getcwd(), path): "{}"'
              .format(os.path.join(os.getcwd(), path)))
        if os.path.realpath(path) != os.path.join(os.getcwd(), path):
            dst_path = os.path.dirname(path)
        code = unzip_unmess(path, dst_path)
        if code != 0:
            return code


if __name__ == "__main__":
    sys.exit(main())
