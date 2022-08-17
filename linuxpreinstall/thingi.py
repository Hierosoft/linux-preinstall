#!/usr/bin/env python3
import os
import sys
from zipfile import ZipFile
import tempfile
import shutil


def echo0(*args, **kwargs):  # formerly prerr
    print(*args, file=sys.stderr, **kwargs)
    return True

verbosity = 0
verbosities = [True, False, 0, 1, 2]

def set_verbosity(level):
    global verbosity
    if level not in verbosities:
        raise ValueError("level must be one of {}".format(verbosities))
    verbosity = level


def unzip_unmess(src_path, dst_path):
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

        movePath = tmpPath
        subs = list(os.listdir(tmpPath))
        if len(subs) < 1:
            raise IOError('There were no files nor directories in "{}"'
                          ''.format(src_path))
        elif len(subs) == 1:
            moveName = subs[0]
            movePath = os.path.join(tmpPath, moveName)
        else:
            # Move the whole thing.
            moveName = os.path.splitext(src_path)[0]
        uI = moveName.find("_")
        oldName = moveName
        if uI > -1:
            if moveName[:uI].isdigit():
                moveName = moveName[uI+1:]
        moveName = moveName.strip(" _").strip()
        # ^ strip again in case of unusual/unicode whitespace characters
        if moveName != oldName:
            echo0('* changed "{}" to "{}"'.format(oldName, moveName))


        echo0("* got {}".format(subs))

        dstSubPath = os.path.join(dst_path, moveName)

        if not os.path.exists(dstSubPath):
            # os.rename(movePath, dstSubPath)
            # ^ raises 'OSError: [Errno 18] Invalid cross-device link:'
            shutil.move(movePath, dstSubPath)
            print('mv "{}" "{}"'.format(movePath, dstSubPath))
            echo0('* wrote "{}"'.format(dstSubPath))
        else:
            # shutil.move copies into it if it exists!
            echo0('Error: "{}" already exists,'
                  ' so extracted files will be ignored.'
                  ''.format(dstSubPath))
            code = 1
    srcName = os.path.split(src_path)[1]
    tryReadme = os.path.splitext(srcName)[0] + ".md"
    dstReadme = "readme.md"
    if os.path.isfile(tryReadme):
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
                 ''.format(trySubs, dstSubPath, tryReadme, dstReadme))
            dstDocsPath = dstSubPath
        '''
        dstReadmePath = os.path.join(dstDocsPath, dstReadme)
        shutil.move(tryReadme, dstReadmePath)
        print('mv "{}" "{}"'.format(tryReadme, dstReadmePath))
    else:
        echo0('* there is no "{}" here to move.'.format(tryReadme))

    return code

def main():
    paths = []
    for argI in range(1, len(sys.argv)):
        arg = sys.argv[argI]
        if arg.startswith("--"):
            if arg == "--verbose":
                set_verbosity(1)
            elif arg == "--debug":
                set_verbosity(2)
            else:
                echo0('The argument "{}" is invalid.'.format(arg))
                return 2
        elif os.path.isfile(arg):
            paths.append(arg)
        else:
            echo0('Error: "{}" is not a file.'.format(arg))
            return 3
    if len(paths) < 1:
        echo0("Error: You must specify at least one zip file.")
        return 1
    for path in paths:
        code = unzip_unmess(path, os.getcwd())
        if code != 0:
            return code

if __name__ == "__main__":
    sys.exit(main())
