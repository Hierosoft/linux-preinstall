from __future__ import print_function
import os
import sys

CAT_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(CAT_DIR)


if __name__ == "__main__":
    sys.path.insert(0, REPO_DIR)


def install_rsnapshot_scripts():
    """Install linux-preinstall's rsnapshot automation scripts.

    Ensure /opt/bin directory exists, then attempt to
    create symbolic links to linux-preinstall's rsnapshot scripts.

    Returns:
        int: Returns 0 if all symlinks are created successfully. Returns 1
            if a PermissionError occurs, or if there is an issue creating
            symlinks.

    Raises:
        Exception: If an unexpected exception occurs during symlink creation.
    """
    scripts_dir = os.path.join(REPO_DIR, "utilities")

    # Ensure the /opt/bin directory exists
    os.makedirs("/opt/bin", exist_ok=True)

    # Define the files to link
    files_to_link = [
        "before_rsnapshot.py",
        "before_rsnapshot.sh",
        "generate_exclude.py",
        "rsnapshot_logged.py",
        "rsnapshot_logged.sh"
    ]

    for filename in files_to_link:
        target = os.path.join(scripts_dir, filename)
        dst = os.path.join("/opt/bin", filename)

        try:
            if os.path.isfile(dst) and not os.path.islink(dst):
                print("Error: {} exists as a regular file.".format(dst),
                      file=sys.stderr)
                return 1

            if os.path.islink(dst):
                existing_target = os.readlink(dst)
                if existing_target != target:
                    print("Error: {} exists but points to {} instead of {}."
                          .format(dst, existing_target, target),
                          file=sys.stderr)
                    return 1

            os.symlink(target, dst)

        except PermissionError:
            print("Permission denied: unable to create symlink at {}."
                  .format(dst), file=sys.stderr)
            return 1

    return 0


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
