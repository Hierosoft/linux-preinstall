#!/usr/bin/env python3
'''
findbycount
-----------
Get a list of directories with the file count specified.

--parent: You can specify a starting directory, otherwise the current
          directory is used.

--ignore: Specify a directory to ignore
          (can be specified multiple times, but use --ignore again
          before each)

--dogExt: Use only this file extension (include the dot).
          (can be specified multiple times, but use --ignore again
          before each)

--count:  (required) Specify how many of the given file type should be
          in each result directory.

Example:
    findbycount.py --count 92 --count 32
'''
from __future__ import print_function
import sys
import os
__author__ = 'Jake "Poikilos" Gustafson'


def echo0(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    return True


defaults = {}
defaults['counts'] = [90, 92]
defaults['parent'] = os.path.realpath(".")
defaults['dotExts'] = [".jpg"]
defaults['ignores'] = ["__pycache__"]
optionNames = {}
optionNames['counts'] = "count"
optionNames['parent'] = "parent"
optionNames['dotExts'] = "dotExt"
optionNames['ignores'] = "ignore"
lists = ['dotExts', 'ignores', 'counts']
integerOptions = ['counts']


def usage():
    echo0(__doc__)
    echo0("Defaults:")
    for k, v in defaults.items():
        echo0("  {}: {}".format(k, v))
    echo0("")


def findByCount(options):
    '''Show directories that have a certain file count.

    Recursively count files in directories and display any full
    directory path that contains a file count that is in the counts
    list.

    Args:
        options (dict): Can have the following keys:
            - parent: The directory path
            - counts (list): The counts to find
            - dotExts (list, optional): Limit the count to these file
              extensions (case-insensitive).
            - ignores (list, optional): Do not recurse into a directory
              that is in this list of directories. Each must be either a
              name only or a full path (both are case-sensitive).
    '''
    # ^ Any more added must also be passed along for recursion!
    parent = options.get('parent')
    if parent is None:
        raise ValueError("parent must be set.")
    counts = options.get('counts')
    if counts is None:
        raise ValueError("counts must be set.")
    if not isinstance(counts, list):
        raise ValueError("counts must be a list.")
    dotExts = options.get('dotExts')
    if dotExts is not None:
        if not isinstance(dotExts, list):
            raise ValueError("dotExts must None or a list.")
    ignores = options.get('ignores')
    if ignores is not None:
        if not isinstance(ignores, list):
            raise ValueError("ignores must None or a list.")

    count = 0
    '''
    try:
        for sub in os.listdir(parent):
            pass
    except FileNotFoundError as ex:
        echo0("Error: File not found: {}".format(parent))
        return
    '''
    for sub in os.listdir(parent):
        subPath = os.path.join(parent, sub)
        if sub.startswith("."):
            continue
        if os.path.isdir(subPath):
            if ignores is not None:
                if sub in ignores:
                    continue
                if subPath in ignores:
                    continue
            newOptions = {}
            for k, v in options.items():
                newOptions[k] = v
            newOptions['parent'] = subPath
            findByCount(newOptions)
            continue
        if os.path.isfile(subPath):
            if dotExts is None:
                count += 1
                continue
            dotExt = os.path.splitext(sub)[1].lower()
            if dotExt in dotExts:
                count += 1
    if count in counts:
        print(parent)


def expandOptions(name, parts):
    s = ""
    space = ""
    for part in parts:
        s += space + "--{} {}".format(name, part)
        space = " "
    return s


def main():
    options = {}
    options['parent'] = None
    options['counts'] = None
    options['dotExts'] = None
    options['ignores'] = None

    thisKey = None
    for argi in range(len(sys.argv)):
        arg = sys.argv[argi]
        if arg in ["/?", "--help"]:
            usage()
            return 0
        if thisKey is not None:
            if thisKey in integerOptions:
                try:
                    arg = int(arg)
                except ValueError:
                    raise ValueError("{} must be an integer but you"
                                     " specified \"{}\"."
                                     "".format(thisKey, arg))
            if thisKey in lists:
                # echo0("* appending to {}".format(thisKey))
                if options.get(thisKey) is None:
                    options[thisKey] = []
                options[thisKey].append(arg)
            else:
                # echo0("* setting {}".format(thisKey))
                if options.get(thisKey) is not None:
                    raise ValueError("{} was already set."
                                     "".format(thisKey))
                options[thisKey] = arg
            thisKey = None
        elif arg.startswith("--"):
            tmp = arg[2:]
            for k, v in optionNames.items():
                if tmp == v:
                    thisKey = k
                    break
            if thisKey is None:
                raise ValueError(
                    "{} is not an option (not a value in optionNames)"
                    "".format(tmp)
                )
    for k, v in defaults.items():
        if options.get(k) is None:
            options[k] = v
            optionName = optionNames[k]
            if isinstance(v, list):
                print("* using defaults {}"
                      "".format(expandOptions(optionName, v)))
            else:
                print("* using default --{} {}".format(optionName, v))
    print("")
    print("using options:")
    for k, v in options.items():
        print("  {}: {}".format(k, v))
    findByCount(options)
    return 0


if __name__ == "__main__":
    sys.exit(main())
