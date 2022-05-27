#!/usr/bin/env python3
'''
Move files already in the profile directory to the proper
ones on the new operating system.
- The files must already be correctly transferred to the
  new computer.
  - Before example 1, you must have already done something
    (on the old macOS computer) like:
    rsync -rtP ~/ user@192.168.1.98:/home/user
    # ^ where 192.168.1.98 is the IP address of the
        computer with a GNU+Linux operating system
        and user is the name of the user that exists on
        that machine but who has not yet used (or has
        renamed or cleared) profiles for:
        {programs}

-------------------------- Usage --------------------------
Run the command on the destination computer after the
transfer is complete:
  {migrateconfig} <source system> <destination system>

Example 1 (migrate macOS files to Linux):
{migrateconfig} Darwin Linux
'''

from __future__ import print_function
import os
import shutil
import sys
import platform


from linuxpreinstall import (
    profile,
    echo0,
)


mvCmd = "mv -f"
if platform.system() == "Windows":
    mvCmd = "move /y"


def usage():
    echo0(__doc__.format(
        migrateconfig=sys.argv[0],
        programs=subs.keys(),
    ))


subs = {}

subs['firefox'] = {}
# See <https://www.howtogeek.com/255587/how-to-find-your-firefox-
# (The profile is under the following directory.)
# profile-folder-on-windows-mac-and-linux/>:
subs['firefox']['Linux'] = os.path.join(".mozilla", "firefox")
# ^ There is no Profiles directory on Linux.
subs['firefox']['Windows'] = os.path.join("AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
subs['firefox']['Darwin'] = os.path.join("Library", "Application Support", "Firefox", "Profiles")

subs['thunderbird'] = {}
# See <https://www.lifewire.com/thunderbird-profile-directory-1173093>:
# (The profile is under the following directory.)
subs['thunderbird']['Linux'] = ".thunderbird"
# ^ > . . . ~/.thunderbird/<Profile name>.
#   > However, if you use a third party build from Debian or Ubuntu,
#   > those builds store your profile folder in
#   > ~/.mozilla-thunderbird<Profile name>"
#   -lifewire.com
subs['thunderbird']['Windows'] = os.path.join("AppData", "Roaming", "Thunderbird", "Profiles")
subs['thunderbird']['Darwin'] = os.path.join("Library", "Thunderbird", "Profiles")
# ^ ~/Library/Thunderbird/Profiles/c49m8v3i.default from Help,
#   Troubleshooting Information using macOS 10.13


def migrate(fromSystem, toSystem):
    '''
    Sequential arguments:
    fromSystem -- Use a platform.system() result such as "Darwin" to
                  specify macOS.
    '''
    for program, systems in subs.items():
        echo0("* processing {}...".format(program))
        srcSub = systems[fromSystem]
        dstSub = systems[toSystem]
        src = os.path.join(profile, srcSub)
        dst = os.path.join(profile, dstSub)
        if not os.path.exists(src):
            echo0("  * INFO: \"{}\" doesn't exist"
                  " so it will not be migrated.".format(src))
            continue
        if os.path.exists(dst):
            echo0("  * INFO: \"{}\" already exists"
                  " so it will not be migrated.".format(dst))
            continue
        os.makedirs(dst)
        # ^ Ensure that the parent directory containing dst exists, but:
        dstParent = os.path.dirname(dst)
        os.rmdir(dst)
        # ^ Ensure that src can move to dst without interference.
        if "move" in mvCmd.lower():
            print('{} "{}" "{}\\"'.format(mvCmd, src, dstParent))
        else:
            print('{} "{}" "{}"'.format(mvCmd, src, dst))
        shutil.move(src, dst)


def main():
    if len(sys.argv) != 3:
        usage()
        echo0("ERROR: You must specify a source and destination"
              " platform.")
        exit(1)
    migrate(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
