"""
Install linux-preinstall's rsnapshot exclude generator and wrappers for
extra logging.

Don't forget:
If you use the recommended rsnapshot.conf and uncomment parts:
- change script from rsnapshot to /opt/bin/rsnapshot_logged.sh
- sudo systemctl daemon-reload
"""
from __future__ import print_function

import os
import sys

if __name__ == "__main__":
    SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, os.path.dirname(SCRIPTS_DIR))

from linuxpreinstall.logging2 import (
    getLogger,
)

from linuxpreinstall.more_rsnapshot import install_rsnapshot_scripts


logger = getLogger(__name__)


def main():
    """Main function that triggers the symlink creation process.

    Returns:
        int: The return value of the create_symlinks function, which is 0
            for success or 1 for failure.
    """
    return install_rsnapshot_scripts()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as ex:
        logger.exception(ex)
    sys.exit(99)
