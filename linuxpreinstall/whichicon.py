#!/usr/bin/env python
'''
-------------------------------- USAGE --------------------------------

Given a binary name or path, this script outputs the first matching
desktop file to standard output (all other messages including successive
matches go to stderr).

The script also returns success (zero) only if it finds a matching
desktop file.

Install:
pip install https://github.com/poikilos/linux-preinstall/archive/refs/heads/master.zip

Examples:
whichicon openscad
# The output could be something like: /usr/share/applications/openscad.desktop
# To get a variable:
OPENSCAD_PATH="\`whichicon openscad\`"
'''
from __future__ import print_function
import os
import sys
import platform

from linuxpreinstall import (
    profile,
    AppData,
    which,
    endsWithAny,
)


def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def errorf(arg):
    sys.stderr.write(arg)
    sys.stderr.flush()


def usage():
    print(__doc__)
    # ^ If you're reading this using a text editor/browser, note that you must
    #   not include the backslashes in the example(s).


me = sys.argv[0]

icon_paths = [
    "/usr/local/share/applications",
    "/usr/share/applications",
    os.path.join(profile, ".local/share/applications"),
    "/var/lib/flatpak/exports/share/applications",
]

icon_dot_extensions = [".desktop"]

if platform.system() == "Windows":
    icon_dot_extensions = [".lnk", ".bat"]
    icon_paths = [
        os.path.join(AppData, "Microsoft", "Windows", "Start Menu"),
        os.path.join(profile, "Desktop"),
        r"C:\ProgramData\Microsoft\Windows\Start Menu",
    ]


def main():
    if len(sys.argv) < 2:
        usage()
        error("Error: You must specify a path or a binary in the path.")
        return 1

    BIN_PATH = sys.argv[1]
    if not os.path.isfile(BIN_PATH):
        error()
        errorf("Warning: The path \"{}\" does not exist"
               "".format(BIN_PATH))
        TRY_CMD = which(BIN_PATH)
        if os.path.isfile(TRY_CMD):
            error(". Unless you specify:")
            error("  {} \"{}\"".format(me, TRY_CMD))
            error("  # or whichever is the correct {} to get the"
                  " correct icon, otherwise the first matching the"
                  " detected path {} will"
                  " be displayed as standard output."
                  "".format(BIN_PATH, TRY_CMD))
            error()
            # exit 2
        else:
            error(".")
            error("Warning: It is not in the environment's PATH either"
                  " (which {}: {})."
                  "".format(BIN_PATH, TRY_CMD))
            error()
            # exit 3

    result = ""
    error("* [{}] looking for a shortcut to \"{}\"..."
          "".format(me, BIN_PATH))
    for SC_PATH in icon_paths:
        if not os.path.isdir(SC_PATH):
            # error("{} does not exist.".format(SC_PATH))
            continue
        # error("* checking in \"{}\"...".format(SC_PATH))
        for sub in os.listdir(SC_PATH):
            subPath = os.path.join(SC_PATH, sub)
            if os.path.isdir(subPath):
                continue
            got = None
            gotRel = None
            if os.path.islink(subPath):
                got = os.readlink(subPath)
            if got is not None:
                if got.startswith("./") or got.startswith("../"):
                    gotRel = got
                    got = os.path.abspath(os.path.join(SC_PATH, gotRel))
                    # error("  * relative symlink resolved to {}"
                    #       "".format(got))
            if (got is not None) and (not os.path.isfile(got)):
                if got == "":
                    error("  * bad symlink {}"
                          " points to inaccessible file {}"
                          "".format(subPath, got))
                else:
                    error("  * inaccessible file: {} from symlink {}".format(got, subPath))
                continue
            found = None
            with open(subPath, 'r') as ins:
                for rawL in ins:
                    line = rawL.strip()
                    if BIN_PATH in line:
                        found = line
                        break
                    # else
                    #     error("NOT {}: {}"
                    #           "".format(subPath, line))
            if found is not None:
                if not endsWithAny(sub, icon_dot_extensions, CS=False):
                    error("  * skipping non-shortcut \"{}\""
                          "".format(subPath))
                    continue
                if sub == "bamf-2.index":
                    error("  * skipping non-shortcut \"{}\""
                          "".format(subPath))
                    continue
                if sub == "mimeinfo.cache":
                    error("  * skipping non-shortcut \"{}\""
                          "".format(subPath))
                    continue
                if result != "":
                    error("  * skipping \"{}\""
                          " since already got a result!"
                          "".format(subPath))
                    continue
                print(subPath)
                result = subPath
    if result != "":
        return 0
    else:
        # error "  * no result was found (got \"$result\")"
        error("  * no desktop file contained \"{}\"".format(BIN_PATH))
        return 1


if __name__ == "__main__":
    main()
