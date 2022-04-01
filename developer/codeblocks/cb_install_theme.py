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
profile = None
AppData = None
LocalAppData = None
myAppData = None

if platform.system() == "Windows":
    profile = os.environ['USERPROFILE']
    AppData = os.environ['APPDATA']
    LocalAppData = os.environ['LOCALAPPDATA']
    myAppData = os.path.join(AppData, "CodeBlocks")
else:
    profile = os.environ['HOME']
    if platform.system() == "Darwin":
        Library = os.path.join(profile, "Library")
        AppData = os.path.join(Library, "Application Support")
        LocalAppData = os.path.join(Library, "Application Support")
        # myAppData = os.path.join(LocalAppData, "codeblocks")
        # cbConf = os.path.join(myAppData, "default.conf")
    else:
        AppData = os.path.join(profile, ".config")
        LocalAppData = os.path.join(profile, ".config")
    myAppData = os.path.join(AppData, "codeblocks")

cbConf = os.path.join(myAppData, "default.conf")

yzhong52 = os.path.join(myDir, "yzhong52", "colour_themes.conf")
sangams = os.path.join(myDir, "sangams", "theme.conf")

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
    print("Error: This script isn't implemented so you have to use"
          " the cb_share_config GUI.")
    sys.exit(1)


if __name__ == "__main__":
    main()
