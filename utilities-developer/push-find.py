#!/usr/bin/env python3
import os
import sys
import shutil
# Importing difflib
import difflib


def diff(file1, file2):
    '''
    Get a list of differences between files.
    '''
    # import difflib
    results = []
    # See
    # <https://www.geeksforgeeks.org/compare-two-files-line-by-line-in-python/>
    with open(file1) as file_1:
        file_1_text = file_1.readlines()

    with open(file2) as file_2:
        file_2_text = file_2.readlines()

    # Find and print the diff:
    for line in difflib.unified_diff(
                file_1_text,
                file_2_text,
                fromfile=file1,
                tofile=file2,
                lineterm='',
            ):
        results.append(line)
    return results


def has_diff(file1, file2):
    return len(diff(file1, file2)) > 0


me = os.path.basename(__file__)
MY_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(MY_DIR)
REPOS_DIR = os.path.dirname(REPO_DIR)

if sys.version_info.major < 3:
    NotADirectoryError = OSError


def shinra_tensei(source_paths, grandparent, subdirectories=None):
    '''
    "Almighty Push" sends the source paths to all subdirectories,
    OVERWRITING them in EVERY REPO from grandma.

    Sequential arguments:
    source_paths -- which files to copy.
    grandparent -- The directory containing multiple repos, each of
        which may contain one or more subdirectories.

    Keyword arguments:
    subdirectories -- A list of subdirectory names (*not* paths) that
        may be in grandparent and that may contain files with the same
        name (os.path.split(source_paths[i])[1]) as any in source_paths
        to be overwritten by them. If None, ALL subdirectories will be
        checked.
    '''
    force = False
    if subdirectories is not None:
        if len(subdirectories) < 1:
            raise ValueError(
                "0 subdirectories where specified."
                " To allow every subdirectory of every repo, specify"
                " subdirectories=None instead."
            )
        force = True
    print("Shinra Tensei!")
    for repo in os.listdir(grandparent):
        repo_path = os.path.join(grandparent, repo)
        if not os.path.isdir(repo_path):
            continue
        if repo.startswith("."):
            continue
        _subdirectories = subdirectories
        if _subdirectories is None:
            # ^ separate variable, otherwise only happens once if None!
            # try:
            _subdirectories = os.listdir(repo_path)
            # except NotADirectoryError:
            #     # "NotADirectoryError: [Errno 20] Not a directory:
            #     #     '/home/owner/git/.directory'"
            force = False
        for scripts_name in _subdirectories:
            scripts_path = os.path.join(repo_path, scripts_name)
            if scripts_name == "__pycache__":
                continue
            if scripts_name.startswith("."):
                if not force:
                    continue
            if not os.path.isdir(scripts_path):
                continue
            # print('* checking "{}"'.format(scripts_path))
            for src_path in source_paths:
                script_name = os.path.basename(src_path)
                dst_path = os.path.join(scripts_path, script_name)
                if os.path.isfile(dst_path):
                    if src_path == dst_path:
                        continue
                    if not has_diff(src_path, dst_path):
                        print('# no diff: "{}" "{}"'.format(src_path, dst_path))
                        continue
                    print('cp "{}" "{}"'.format(src_path, dst_path))
                    shutil.copy(src_path, dst_path)


def main():
    files_here = []
    names = []
    source_dir = os.getcwd()
    # subdirectories = ['utilities', 'utilities-server',
    #                   'utilities-developer', 'scripts']
    # ^ unused since all subs need to be checked (such as any
    #   module directory particular to a repo)
    subdirectories = None
    for sub in os.listdir(source_dir):
        if not sub.startswith("find_"):
            continue
        names += sub
        files_here.append(os.path.join(source_dir, sub))
        print("[{}] collected {}".format(me, sub))
    sub = "push-find.py"
    if not os.path.isfile(sub):
        raise RuntimeError('"{}" is missing.'.format(sub))
    files_here.append(sub)
    print("[{}] collected {}".format(me, sub))
    return shinra_tensei(
        files_here,
        REPOS_DIR,
        subdirectories=subdirectories,
    )


if __name__ == "__main__":
    sys.exit(main())
