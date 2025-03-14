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
    script_name basic_materials --user Poikilos --site https://gitlab.com
    # ends up as ~/Downloads/git/Poikilos/

    script_name filter --user Poikilos --repos_dir ~/git
    # - uses github.com/Poikilos
    # - clones to ~/git/Poikilos/filter

    script_name filter --site github
    # - uses github.com
    # - clones to ~/Downloads/git/Poikilos/filter

    script_name git@github.com:Poikilos/filter.git
    # - parses the URL and clones it to the appropriate directory.
"""

from __future__ import print_function
import os
import sys
import argparse
import subprocess
from argparse import ArgumentParser

SITES = {
    'site': None,
    'github': "https://github.com",
    'gitlab': "https://gitlab.com",
    'codeberg': "https://codeberg.org",
    'notabug': "https://notabug.org",
}


def check_git_installed():
    """Check if git is installed."""
    if not subprocess.call(['which', 'git'], stdout=subprocess.DEVNULL) == 0:
        print("Error: git is not installed.")
        sys.exit(1)


def construct_url(website, user, repo_name):
    """Construct the URL for cloning the repo."""
    if website:
        base_url = SITES.get(website)
        if not base_url:
            base_url = website
        return "{}/{}/{}.git".format(base_url, user, repo_name)
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
        help=("Construct the local repo path from"
              " $USER_DIR/$REPO_NAME instead of"
              " $DEFAULT_REPO_DIR/$REMOTE_GIT_USER/$REPO_NAME.")
    )
    parser.add_argument(
        '--site',
        help=("Set the base URL for CUSTOM_URL. If it is a known name"
              " (notabug, codeberg, gitlab, github), it will be automatically"
              " converted to a URL.")
    )
    parser.add_argument(
        '--github',
        action='store_true',
        help=("Set the base URL to github.com")
    )
    parser.add_argument(
        '--gitlab',
        action='store_true',
        help=("Set the base URL to gitlab.com")
    )
    parser.add_argument(
        '--notabug',
        action='store_true',
        help=("Set the base URL to notabug.org")
    )
    parser.add_argument(
        '--codeberg',
        action='store_true',
        help=("Set the base URL to codeberg.org")
    )
    parser.add_argument(
        '--url',
        help=("Set the repo URL directly. This option overrides the"
              " WEBSITE option.")
    )

    parser.add_argument(
        'repo_name_or_url',
        help="The name of the repository or a full URL."
    )

    args = parser.parse_args()

    repo_name_or_url = args.repo_name_or_url

    repos_dir = args.repos_dir if args.repos_dir else "~/Downloads/git"
    repos_dir = os.path.expanduser(repos_dir)

    remote_git_user = args.user
    website = None
    count = 0

    got_sites = []
    for key in list(SITES.keys()):
        if getattr(args, key):
            count += 1
            if key == 'site':
                website = getattr(args, key)
            else:
                # Others are boolean, so use key as value.
                website = key
            got_sites.append(website)
    if len(got_sites) > 1:
        print(
            "Error: You can only choose one of the mutually exclusive"
            " arguments %s or --url, but got %s"
            % (list(SITES.keys()), got_sites),
            file=sys.stderr,
        )
        return 1
    elif len(got_sites) > 0 and args.url:
        print(
            "Error: You can only choose one of the mutually exclusive"
            " arguments %s or --url, but got %s and --url"
            % (list(SITES.keys()), got_sites),
            file=sys.stderr,
        )
        return 1

    custom_url = args.url
    user_dir = os.path.expanduser(args.user_dir) if args.user_dir else None

    # Detect if repo_name_or_url is a URL
    parts = None
    if (repo_name_or_url.startswith("git@")
            or repo_name_or_url.startswith("https://")):
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
        parser.print_help()
        print("\nError: Repository URL could not be determined."
              " Specify --url or a base url (above) containing {}/{}"
              .format(remote_git_user, repo_name))
        sys.exit(1)

    print("* Cloning from: {}".format(custom_url))
    print("* Cloning into directory: {}".format(user_dir))

    # Execute git clone
    return_code = subprocess.call(
        ["git", "clone", custom_url, os.path.join(user_dir, repo_name)])
    return return_code


if __name__ == "__main__":
    sys.exit(main())
