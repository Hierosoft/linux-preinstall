#!/usr/bin/env python
"""
Clone a git repository using only the name or the full URL.

USAGE
The current directory name must be the user name.
Otherwise, specify --user then the username.
If the website is not GitHub, specify the base URL after --site,
such as https://gitlab.com

    script_name <repo_name_or_url> [options]

(The first CLI argument that isn't a non-boolean "--" switch and doesn't
have one before it will be used as REPO_NAME or a URL.)

EXAMPLES
    script_name basic_materials --user poikilos --site https://gitlab.com
    # ends up as ~/Downloads/git/poikilos/

    script_name filter --user poikilos --repos_dir ~/git
    # - uses github.com/poikilos
    # - clones to ~/git/poikilos/filter

    script_name filter --site github
    # - uses github.com
    # - clones to ~/Downloads/git/poikilos/filter

    script_name git@github.com:poikilos/filter.git
    # - parses the URL and clones it to the appropriate directory.
"""

from __future__ import print_function
import os
import sys
import argparse
import subprocess
from argparse import ArgumentParser


def check_git_installed():
    """Check if git is installed."""
    if not subprocess.call(['which', 'git'], stdout=subprocess.DEVNULL) == 0:
        print("Error: git is not installed.")
        sys.exit(1)


def construct_url(website, user, repo_name):
    """Construct the URL for cloning the repo."""
    if website:
        return "{}/{}/{}.git".format(website, user, repo_name)
    return ""


def main():
    check_git_installed()

    parser = ArgumentParser(description=__doc__)

    parser.add_argument(
        '--repos_dir',
        help="Set the base directory for repos."
    )
    parser.add_argument(
        '--user',
        help="Set the repo user."
    )
    parser.add_argument(
        '--user_dir',
        help=("Construct the local repo path from "
              "$USER_DIR/$REPO_NAME instead of "
              "$DEFAULT_REPO_DIR/$REMOTE_GIT_USER/$REPO_NAME.")
    )
    parser.add_argument(
        '--site',
        help=("Set the base URL for CUSTOM_URL. If it is a known name "
              "(notabug, gitlab, or github), it will be automatically "
              "converted to a URL.")
    )
    parser.add_argument(
        '--url',
        help=("Set the repo URL directly. This option overrides the "
              "WEBSITE option.")
    )

    parser.add_argument(
        'repo_name_or_url',
        help="The name of the repository or a full URL."
    )

    args = parser.parse_args()

    repo_name_or_url = args.repo_name_or_url
    repos_dir = os.path.expanduser(args.repos_dir) if args.repos_dir else "~/Downloads/git"
    remote_git_user = args.user
    website = args.site
    custom_url = args.url
    user_dir = os.path.expanduser(args.user_dir) if args.user_dir else None

    # Detect if repo_name_or_url is a URL
    parts = None
    if repo_name_or_url.startswith("git@") or repo_name_or_url.startswith("https://"):
        custom_url = repo_name_or_url
        parts = repo_name_or_url.split("/")
        if parts[-1].endswith(".git"):
            parts[-1] = parts[-1][:-4]  # Strip ".git"
        repo_name = parts[-1]
    else:
        repo_name = repo_name_or_url

    # Determine USER_DIR and REMOTE_GIT_USER
    if not remote_git_user:
        remote_git_user = os.path.basename(os.getcwd())

    if parts:
        remote_git_user = parts[-2]  # Get the username from the URL

    if not user_dir:
        user_dir = os.path.join(repos_dir, remote_git_user)

    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    # Construct the clone URL if not provided directly
    if not custom_url:
        custom_url = construct_url(website, remote_git_user, repo_name)

    if not custom_url:
        print("Error: Repository URL could not be determined.")
        sys.exit(1)

    print("* Cloning from: {}".format(custom_url))
    print("* Cloning into directory: {}".format(user_dir))

    # Execute git clone
    subprocess.call(["git", "clone", custom_url, os.path.join(user_dir, repo_name)])


if __name__ == "__main__":
    sys.exit(main())