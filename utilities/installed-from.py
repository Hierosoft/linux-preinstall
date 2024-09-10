#!/usr/bin/env python3
"""
This script lists all packages from a specified Ubuntu repository or all the
available repositories on the system. It can also filter for installed packages.

If you receive an import error, you may need to install python-apt first with e.g.
  sudo apt install python-apt

but this is often not necessary.

based on https://askubuntu.com/a/1355071/766334
"""
from __future__ import division
import apt
import argparse
import subprocess
import sys


def count_installed_packages():
    """Count all installed Debian packages.

    Returns:
        int: The number of installed packages.
    """
    try:
        # Run dpkg-query command to list all installed packages
        result = subprocess.run(
            ['dpkg-query', '-f', '${Package}\n', '-W'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Split the output by lines and count them
        match_count = len(result.stdout.splitlines())
        return match_count
    except subprocess.CalledProcessError as e:
        # Handle possible errors during the subprocess call
        print("An error occurred while counting installed packages: {}".format(e))
        return 0


def count_deb_packages_from_cache(installed=False):
    """Count all installed Debian packages using the apt cache.

    Returns:
        int: The number of installed packages.
    """
    cache = apt.Cache()
    if installed:
        installed_count = sum(1 for pkg in cache if pkg.is_installed)
    else:
        installed_count = sum(1 for pkg in cache)
    return installed_count


def count_cached_packages():
    """Count all installed Debian packages by reading the dpkg status file.

    This should match the count from tools like apt-cache by reading
    directly from the same package database used by APT.

    Returns:
        int: The number of installed packages.
    """
    try:
        # Use grep to count lines starting with "Package:" in the dpkg status file
        result = subprocess.run(
            ['grep', '-c', '^Package:', '/var/lib/dpkg/status'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Convert the output to an integer count
        package_count = int(result.stdout.strip())
        return package_count
    except subprocess.CalledProcessError as e:
        print("An error occurred while counting installed packages: {}".format(e))
        return 0


def describe_package(package):
    return ("shortname={}, name={}, fullname={}"
            .format(package.shortname, package.name, package.fullname))


def show_packages_from(repo_site, show_sites=False, installed=False):
    """
    Args:
        repo_site (str): The site such as obtained from show_sites.
            Example: "extras.ubuntu.com"
            Set to None to list no packages such as when
            show_sites=True to list sites only (not packages).
        show_sites (bool, optional): List all of the sites that are
            present on the system (Any of these can then later be used
            for the repo_site argument). Defaults to False.
        installed (bool, optional): Only list installed packages
            (or only sites with installed packages if show_sites).
            Defaults to False.
    """

    count = 0
    cache = apt.Cache()
    match_count = 0
    sites = set()
    # total = count_installed_packages()  # Warning: gets fewer than Cache()
    # total = count_cached_packages()  # gets fewer than Cache()
    print("Counting packages...", file=sys.stderr)
    total = count_deb_packages_from_cache(installed=False)  # uses Cache()
    print("Processing packages...", file=sys.stderr)
    for package in cache:
        count += 1  # count even if "installed" & not packages.is_installed
        # so progress doesn't update so slowly
        if total:
            ratio = count / total
            percentage = "{:.2%} ({}/{})".format(ratio, count, total)  # percentage formatter
            sys.stderr.write("\r"+percentage)
        if installed and not package.is_installed:
            continue
        if not package.candidate:
            # print("\nINFO: package.candidate is None"
            #       " for dir(package)={}"
            #       .format(dir(package)), file=sys.stderr)
            # ^ 'architecture', 'candidate', 'commit', 'essential', 'fullname', 'get_changelog', 'has_config_files', 'id', 'installed', 'installed_files', 'is_auto_installed', 'is_auto_removable', 'is_inst_broken', 'is_installed', 'is_now_broken', 'is_upgradable', 'mark_auto', 'mark_delete', 'mark_install', 'mark_keep', 'mark_upgrade', 'marked_delete', 'marked_downgrade', 'marked_install', 'marked_keep', 'marked_reinstall', 'marked_upgrade', 'name', 'shortname', 'versions'
            print("\nINFO: package.candidate is None (no remote origin?)"
                  " for {}"
                  .format(describe_package(package)),
                  file=sys.stderr)
            continue
        if show_sites:
            if not package.candidate.origins[0].site:
                print("\nNo site for {}".format(describe_package(package)),
                      file=sys.stderr)
            elif package.candidate.origins[0].site not in sites:
                prefix = ""
                stream = sys.stdout
                if repo_site:
                    prefix = "checking package(s) in site: "
                    stream = sys.stderr
                print("\n"+prefix+"{}"
                      .format(package.candidate.origins[0].site), file=stream)
                sites.add(package.candidate.origins[0].site)
        if (
            cache[package.name].is_installed
            and package.candidate.origins[0].site == repo_site
        ):
            package_origin = package.candidate.origins[0]
            print(
                package.name,
                # See https://apt-team.pages.debian.net/python-apt/library/apt.package.html#apt.package.Origin
                # for further details on the meanings of the below
                package_origin.origin,  # The Origin, as set in the Release file
                package_origin.archive,  # The archive (eg. Ubuntu release name)
                package_origin.component,  # The component (eg. main/universe)
                package_origin.site,  # The hostname of the site.
                # package_origin.label,  # The Label, as set in the Release file
                # package_origin.trusted,  # Origin trusted (Release file signed by key in apt keyring)
            )
            match_count += 1
    print()
    print(total, "packages counted")
    print(count, "packages processed")
    if repo_site:
        print(match_count, "packages match")
    return 0


def list_apt_sites(installed=False):
    """List all available repository sites on the system.
    This is slower than other methods, so typically set
    installed to True for some useful output specific to this
    code.

    Returns:
        int: 0 if successful, 1 if there was an error.
    """
    return show_packages_from(None, show_sites=True, installed=installed)


def parse_arguments():
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="List repos from which packages are installed, etc.")
    parser.add_argument("repo_site", nargs='?', help="The repository site to list packages from, such as 'extras.ubuntu.com'.")
    parser.add_argument("--list-sites", action="store_true", help="List all available repository sites.")
    parser.add_argument("--installed", action="store_true", help="Only list installed packages (or repos from which packages were installed if also --list-sites).")
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.list_sites:
        if args.installed:
            print("Listing sites only.", file=sys.stderr)
        else:
            print("Listing sites only, also limited to those from which packages are installed.", file=sys.stderr)
        list_apt_sites(installed=args.installed)
        return 0
    if not args.repo_site:
        print("Error: Expected repo site such as 'extras.ubuntu.com', or --list-sites", file=sys.stderr)
        return 1
    return show_packages_from(args.repo_site, installed=args.installed)


if __name__ == "__main__":
    sys.exit(main())
