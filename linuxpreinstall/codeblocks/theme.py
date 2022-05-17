#!/usr/bin/env python3
"""
Transfer only the parts you want (such as colors from one codeblocks
XML config file to another).

See
<https://yuchen52.medium.com/change-editor-theme-for-code-blocks-windows-linux-mac-92e9c15cbca4>
(for installing
<https://gist.github.com/yzhong52/6852140faa233408de67/raw/b8c19b115859afa9a6831ffd59f1d2e81985ccca/colour_themes.conf>
manually).

"""
import platform
import os
import sys

myDir = os.path.dirname(os.path.abspath(__file__))

cbConf = None

from linuxpreinstall import(
    profile,
    AppData,
    LocalAppData,
    myAppData,
)

cbConf = os.path.join(myAppData, "default.conf")

yzhong52 = os.path.join(myDir, "yzhong52", "colour_themes.conf")
sangams = os.path.join(myDir, "sangams", "theme.conf")
missing_files = []

if not os.path.isfile(yzhong52):
    missing_files.append(yzhong52)

if not os.path.isfile(sangams):
    missing_files.append(sangams)

if len(missing_files) > 0:
    raise FileNotFoundError(
        "The linuxpreinstall module isn't installed correctly. The"
        " missing data files should be included: {}"
        "".format(missing_files)
    )


def usage():
    print(__doc__)
    print("")


def main():
    destConf = cbConf
    if len(sys.argv) < 2:
        print("You must specify a source file.")
        sys.exit(1)
    srcConf = sys.argv[1]
    if not os.path.isfile(srcConf):
        usage()
        print("Error: \"{}\" is not present.".format(srcConf))
        sys.exit(1)
    srcConf = os.path.abspath(srcConf)
    print("* chose \"{}\"".format(srcConf))
    if len(sys.argv) > 2:
        destConf = sys.argv[2]
    if not os.path.isfile(destConf):
        usage()
        print("Error: {} is not present.")
        if destConf == cbConf:
            print("Open and close Code::Blocks to"
                  " generate an initial configuration."
                  "".format(cbConf))
        sys.exit(1)
    else:
        destConf = os.path.abspath(destConf)
        print("* targeting {}"
              "".format(destConf))

    usage()
    raise NotImplementedError(
        "Error: This script isn't implemented so you have to use"
        " the cb_share_config GUI."
    )


if __name__ == "__main__":
    main()
