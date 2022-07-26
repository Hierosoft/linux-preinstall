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
import json


verbosity = 0
for argI in range(1, len(sys.argv)):
    arg = sys.argv[argI]
    if arg.startswith("--"):
        if arg == "--verbosity":
            verbosity = 1
        elif arg == "--debug":
            verbosity = 2

if __name__ == "__main__":
    myDir = os.path.dirname(os.path.abspath(__file__))
    repoDir = os.path.dirname(myDir)
    if verbosity > 1:
        print("looking for module in repoDir last: {}".format(repoDir),
              file=sys.stderr)
    sys.path.append(repoDir)
    # There is more code for the __name__ case at the bottom.


from linuxpreinstall import (
    profile,
    AppData,
    which,
    endsWithAny,
    get_verbosity,
    echo0,  # formerly prerr as error
    write0,  # formerly errorf
    echo1,  # formerly debug
)

tryRepo = os.path.join(profile, "git", "pycodetool")
tryModule = os.path.join(tryRepo, "pycodetool")

if os.path.isdir(tryModule):
    sys.path.insert(0, tryRepo)

from pycodetool.ggrep import (
    is_like_any,
    any_contains,
)


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


def which_icon(BIN_PATH):
    if not os.path.isfile(BIN_PATH):
        # echo0()
        write0("* Checking for \"{}\"...not a full path"
               "".format(BIN_PATH))
        TRY_CMD = which(BIN_PATH)
        if TRY_CMD is not None:
            echo0(". Unless you specify:")
            echo0("  {} \"{}\"".format(me, TRY_CMD))
            echo0("  # or whichever is the correct {} to get the"
                  " correct icon, otherwise the first matching the"
                  " detected path {} will"
                  " be displayed as standard output."
                  "".format(BIN_PATH, TRY_CMD))
            # exit 2
        else:
            # concatenates onto errorf above:
            echo0(" and command \"{}\" is not in the environment's PATH"
                  " either.".format(TRY_CMD))
            #       " (which {}: {})."
            # exit 3
        # echo0()

    result = ""
    echo0("* [{}] looking for a shortcut to \"{}\"..."
          "".format(me, BIN_PATH))
    exact_results = []
    fuzzy_results = []
    echo1("BIN_PATH: {}".format(BIN_PATH))
    for SC_PATH in icon_paths:
        if not os.path.isdir(SC_PATH):
            # echo0("{} does not exist.".format(SC_PATH))
            continue
        # echo0("* checking in \"{}\"...".format(SC_PATH))
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
                    # echo0("  * relative symlink resolved to {}"
                    #       "".format(got))
            if (got is not None) and (not os.path.isfile(got)):
                if got == "":
                    echo0("  * bad symlink {}"
                          " points to inaccessible file {}"
                          "".format(subPath, got))
                else:
                    echo0('  * inaccessible file: {} from symlink {}'
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
                        name = "#!"
                        value = line[2:]
                        tmpExecParts = value.split(" ")
                        execParts = []
                        for execI in range(len(tmpExecParts)):
                            xPart = tmpExecParts[execI]
                            if "/" in xPart:
                                xPart = os.path.basename(xPart)
                            if xPart in ["python", "python2", "python3"]:
                                continue
                            execParts.append(xPart)
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
                    check_all_parts = False
                    if name in ["Exec", "TryExec"]:
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
                    elif (name == "Name") or name.startswith("Name["):
                        check_all_parts = True
                    elif name == "#!":
                        pass
                    else:
                        echo1("  * skipping ")
                        continue
                    echo1('  * checking for {} in {} or in part of {} or {}'
                          ''.format(BIN_PATH, value, json.dumps(launchCmd),
                                    json.dumps(execSub)))
                    if BIN_PATH == execSub:
                        found = line
                        echo0('    * matched name "{}"'.format(found))
                        exact = True
                        break
                    elif check_all_parts and any_contains(execParts, BIN_PATH,
                                                          case_sensitive=False):
                        found = line
                        exact = BIN_PATH in execParts
                        break
                    elif BIN_PATH == launchCmd:
                        found = line
                        echo0('    * {} matches launch argument in {}'
                              ''.format(BIN_PATH, json.dumps(launchCmd)))
                        exact = True
                        break
                    elif any_contains(launchCmd.split("-"), BIN_PATH,
                                      allow_blank=True, case_sensitive=False):
                        # elif is_like_any(BIN_PATH,
                        #                  launchCmd.split("-"),
                        #                  allow_blank=True,
                        #                  quiet=True):
                        found = line
                        echo0('    * any part of {} contains {}'
                              ''.format(json.dumps(launchCmd), BIN_PATH))
                        exact = BIN_PATH in launchCmd.split("-")
                        break
                    elif BIN_PATH in execSub.split("-"):
                        found = line
                        echo0('    * {} is in part of {}'
                              ''.format(BIN_PATH, json.dumps(execSub)))
                        exact = True
                        break
                    elif is_like_any(BIN_PATH, execSub.split("-"),
                                     allow_blank=True, quiet=True):
                        found = line
                        echo0('    * {} is_like "{}"'
                              ''.format(BIN_PATH, execSub))
                        exact = True
                        break
                    elif BIN_PATH == value:
                        found = line
                        echo0('    * matched path "{}"'.format(found))
                        exact = True
                        break
                    elif BIN_PATH in execSub:
                        found = line
                        echo0('    * matched part of "{}"'.format(found))
                        break
                    # else
                    #     echo0("NOT {}: {}"
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
            echo0("  * skipping non-shortcut \"{}\""
                  "".format(subPath))
            continue
        if sub == "bamf-2.index":
            echo0("  * skipping non-shortcut \"{}\""
                  "".format(subPath))
            continue
        if sub == "mimeinfo.cache":
            echo0("  * skipping non-shortcut \"{}\""
                  "".format(subPath))
            continue
        if result != "":
            echo0("  * skipping \"{}\""
                  " since already got a result!"
                  "".format(subPath))
            continue
        print(subPath)
        result = subPath
    return result


def main():
    if len(sys.argv) < 2:
        usage()
        echo0("Error: You must specify a path or a binary in the path.")
        return 1

    BIN_PATH = sys.argv[1]
    result = which_icon(BIN_PATH)
    if result != "":
        return 0
    else:
        # error "  * no result was found (got \"$result\")"
        echo0("  * no desktop file contained \"{}\"".format(BIN_PATH))


if __name__ == "__main__":
    main()
