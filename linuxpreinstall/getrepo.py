#!/usr/bin/env python3
'''
getrepo
-------
Get or pull a repo.

This is submodule of linuxpreinstall hosted at
<https://github.com/Poikilos/linux-preinstall>.
This submodule is also present in
<https://github.com/Poikilos/marlininfo>
in preload_tft_sdcard.py (since they are trivial and should make
the script depend on linuxpreinstall).

'''

import os
import sys
import platform
import subprocess


if platform.system() == "Windows":
    HOME = os.environ['USERPROFILE']
    USER = os.environ['USERNAME']
else:
    HOME = os.environ['HOME']
    USER = os.environ['USER']


def echo0(*args):
    print(*args, file=sys.stderr)

def get_or_pull(repo_url, repo_dir):
    '''
    Returns:
    0 for success.

    Raises:
    subprocess.CalledProcessError -- if the process returns nonzero
    '''
    if not os.path.isdir(repo_dir):
        echo0('[get_or_pull] cloning into "{}"...'.format(repo_dir))
        cmd = "git clone '{}' '{}'".format(repo_url, repo_dir)
    else:
        os.chdir(repo_dir)
        echo0('[get_or_pull] running `git pull` in "{}"...'.format(repo_dir))
        cmd = "git pull"
    proc = subprocess.run(
        cmd,
        shell=True,
        # check=True,  # raises exception on non-zero
        # capture_output=True,
    )
    code = proc.returncode
    return code


def repo_flag_sub(path):
    '''
    Get the file that indicates the path is probably not an sdcard.

    Returns:
    The bad subdirectory (name not path).
    '''
    oops_sub = None
    for sub in os.listdir(path):
        sub_path = os.path.join(path, sub)
        if not os.path.isfile(sub_path):
            continue
        if "setup" in sub.lower():
            oops_sub = sub
            break
        if sub.lower() == ".gitignore":
            oops_sub = sub
            break
        if sub.lower() == "readme.md":
            oops_sub = sub
            break
    return oops_sub
