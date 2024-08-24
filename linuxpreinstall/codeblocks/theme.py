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
import os
import sys

if __name__ == "__main__":
    SUBMODULE_DIR = os.path.dirname(os.path.realpath(__file__))
    MODULE_DIR = os.path.dirname(os.path.dirname(SUBMODULE_DIR))
    sys.path.insert(0, os.path.dirname(MODULE_DIR))

from linuxpreinstall import (
    myAppData,
    echo0,
)

from linuxpreinstall.logging2 import (
    getLogger,
)

logger = getLogger(__name__)

myDir = os.path.dirname(os.path.abspath(__file__))

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
    echo0(__doc__)
    echo0("")


def main():
    destConf = cbConf
    if len(sys.argv) < 2:
        logger.error("You must specify a source file.")
        return 1
    srcConf = sys.argv[1]
    if not os.path.isfile(srcConf):
        usage()
        logger.error("\"{}\" is not present.".format(srcConf))
        return 1
    srcConf = os.path.abspath(srcConf)
    echo0("* chose \"{}\"".format(srcConf))
    if len(sys.argv) > 2:
        destConf = sys.argv[2]
    if not os.path.isfile(destConf):
        usage()
        logger.error("{} is not present.".format(cbConf))
        if destConf == cbConf:
            echo0("Open and close Code::Blocks to"
                  " generate an initial configuration.")
        return 1
    else:
        destConf = os.path.abspath(destConf)
        echo0("* targeting {}".format(destConf))

    usage()
    raise NotImplementedError(
        "This script isn't implemented so you have to use"
        " the cb_share_config GUI."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
