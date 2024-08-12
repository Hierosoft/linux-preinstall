"""
Install linux-preinstall's rsnapshot exclude generator and wrappers for
extra logging.

Don't forget:
If you use the recommended rsnapshot.conf and uncomment parts:
- change script from rsnapshot to /opt/bin/rsnapshot_logged.sh
- sudo systemctl daemon-reload
"""
from __future__ import print_function
import sys


from linuxpreinstall.more_rsnapshot import install_rsnapshot_scripts


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
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
    sys.exit(99)
