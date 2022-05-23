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

from linuxpreinstall.ggrep import (
    is_like_any,
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

identifier_keys = [
    "Exec",
    "TryExec",
    "GenericName",
    "Name",
    # "Comment",
    # "Icon",
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
        # error()
        errorf("* Checking for \"{}\"...not a full path"
               "".format(BIN_PATH))
        TRY_CMD = which(BIN_PATH)
        if TRY_CMD is not None:
            error(". Unless you specify:")
            error("  {} \"{}\"".format(me, TRY_CMD))
            error("  # or whichever is the correct {} to get the"
                  " correct icon, otherwise the first matching the"
                  " detected path {} will"
                  " be displayed as standard output."
                  "".format(BIN_PATH, TRY_CMD))
            # exit 2
        else:
            error(" and command is not in the environment's PATH"
                  " either.".format(BIN_PATH, TRY_CMD))
            #       " (which {}: {})."
            # exit 3
        # error()

    result = ""
    error("* [{}] looking for a shortcut to \"{}\"..."
          "".format(me, BIN_PATH))
    exact_results = []
    fuzzy_results = []
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
                    error('  * inaccessible file: {} from symlink {}'
                          ''.format(got, subPath))
                continue
            found = None
            exact = False
            with open(subPath, 'r') as ins:
                for rawL in ins:
                    line = rawL.strip()
                    name = ""
                    value = ""
                    execSub = ""
                    if line.startswith("#"):
                        if not line.startswith("#!"):
                            # Some desktop files have a shebang which
                            # runs the executable.
                            continue
                        value = line
                    else:
                        signI = line.find("=")
                        if signI > -1:
                            name = line[:signI]
                            value = line[signI+1:]
                            if name not in identifier_keys:
                                continue
                            if os.path.sep in value:
                                execSub = os.path.split(value)[1]
                        else:
                            value = ""
                            continue
                    execParts = value.split(" ")
                    launchCmd = ""
                    if len(execParts) > 0:
                        if os.path.split(execParts[0])[1] == "flatpak":
                            # Example: "Exec=/usr/bin/flatpak run
                            # --branch=stable --arch=x86_64
                            # --command=gimp-2.10 --file-forwarding
                            # org.gimp.GIMP @@u %U @@"
                            for cmdI in range(1, len(execParts)):
                                arg = execParts[cmdI]
                                launchPre = "--command="
                                if arg.startswith(launchPre):
                                    launchCmd = arg[len(launchPre):]
                    if BIN_PATH == execSub:
                        found = line
                        error('* matched name "{}"'.format(found))
                        exact = True
                        break
                    elif BIN_PATH == launchCmd:
                        found = line
                        error('* {} matches launch argument in "{}"'
                              ''.format(BIN_PATH, launchCmd))
                        exact = True
                        break
                    elif BIN_PATH in launchCmd.split("-"):
                        # elif is_like_any(BIN_PATH,
                        #                  launchCmd.split("-"),
                        #                  allow_blank=True,
                        #                  quiet=True):
                        found = line
                        error('* {} matches a part of a command in "{}"'
                              ''.format(BIN_PATH, launchCmd))
                        exact = True
                        break
                    elif is_like_any(BIN_PATH, execSub.split("-"),
                                     allow_blank=True, quiet=True):
                        found = line
                        error('* {} is_like "{}"'
                              ''.format(BIN_PATH, execSub))
                        exact = True
                        break
                    elif BIN_PATH == value:
                        found = line
                        error('* matched path "{}"'.format(found))
                        exact = True
                        break
                    elif BIN_PATH in execSub:
                        found = line
                        error('* matched part of "{}"'.format(found))
                        break
                    # else
                    #     error("NOT {}: {}"
                    #           "".format(subPath, line))
            if found is not None:
                if exact:
                    exact_results.append(subPath)
                else:
                    fuzzy_results.append(subPath)
    results = exact_results + fuzzy_results
    result = ""
    for subPath in results:
        sub = os.path.split(subPath)[1]
        # if found is not None:
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
