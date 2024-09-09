#!/usr/bin/env python3

import os
import sys
from gi.repository import Gio

if sys.version_info.major < 3:
    from linuxpreinstall.logging2 import getLogger
else:
    from logging import getLogger

logger = getLogger(__name__)

HOME = os.path.expanduser("~")
AVATAR_PATH = os.path.join(HOME, ".config", "linux-preinstall", "user.png")

def pin_app_to_favorites(desktop_file_path, index=None):
    """
    Pins the application to Cinnamon favorites if it is not already present.
    Optionally, pins it at a specified index.

    :param desktop_file_path: Path to the .desktop file to be pinned.
    :param index: Optional index at which to pin the application.
    """
    # Check if the .desktop file exists
    if not os.path.isfile(desktop_file_path):
        print(f"Warning: Missing {desktop_file_path}, can't pin")
        return

    # Extract the full filename of the .desktop file
    app_name = os.path.basename(desktop_file_path)

    # Retrieve the current list of favorite apps
    settings = Gio.Settings.new("org.cinnamon")
    current_favorites = settings.get_strv("favorite-apps")

    # Preliminary removal if index is provided and the app is already in the list
    if index is not None and app_name in current_favorites:
        current_favorites.remove(app_name)

    # Check if the app is already in the list (post-removal check)
    if app_name in current_favorites:
        print(f"{app_name} is already in the favorites list.")
    else:
        if index is not None:
            # Insert at the specified index
            current_favorites.insert(index, app_name)
        else:
            # Append the new app to the list
            current_favorites.append(app_name)

        # Set the new list as the favorite apps
        settings.set_strv("favorite-apps", current_favorites)
        print(f"Pinned '{app_name}' to favorites.")


def create_logout_desktop_file():
    """
    Creates a .desktop file to log out from Cinnamon and pins it to the favorites.

    The .desktop file is saved in the ~/.local/share/applications directory.
    """
    # Get the current user's username and home directory
    username = os.getenv("USER", "user")

    # Define the desktop file path and icon path using os.path.join
    desktop_dir = os.path.join(HOME, ".local", "share", "applications")
    desktop_file_path = os.path.join(desktop_dir, "logout.desktop")

    name = "Logout ({})".format(username)

    # Ensure the target directory exists
    os.makedirs(desktop_dir, exist_ok=True)

    # Content of the .desktop file
    desktop_file_content = (
        "[Desktop Entry]\n"
        "Version=1.0\n"
        "Type=Application\n"
        "Name={}\n"
        "Exec=cinnamon-session-quit --logout\n"
        "Icon={}\n"
        "Terminal=false\n"
    ).format(name, AVATAR_PATH)

    # Write the content to the file
    with open(desktop_file_path, "w") as desktop_file:
        desktop_file.write(desktop_file_content)

    # Make the file executable
    os.chmod(desktop_file_path, 0o755)

    print("Desktop file created at:", desktop_file_path)

    # Pin the created desktop file to Cinnamon favorites at index 0
    pin_app_to_favorites(desktop_file_path, index=0)


def main():
    """
    Main function to create the logout desktop file and pin it to Cinnamon favorites.
    """
    if not os.path.isfile(AVATAR_PATH):
        print("Error: Create {} first.".format(AVATAR_PATH))
        return 1
    # try:
    create_logout_desktop_file()
    # except Exception as ex:
    #     logger.exception(ex)
    #     return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
