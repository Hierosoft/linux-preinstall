#!/usr/bin/env python3
import os
import shutil
import sys
import platform


profile = None
mvCmd = "mv -f"
if platform.system() == "Windows":
    profile = os.environ['USERPROFILE']
    mvCmd = "move /y"
else:
    profile = os.environ['HOME']


def error(msg):
    sys.stderr.write("{}\n".format(msg))


def usage():
    error("Move files already in the profile directory to the proper")
    error("ones on the new operating system.")
    error("- The files must already be correctly transferred to the")
    error("  new computer.")
    error("  - Before example 1, you must have already done something")
    error("    (on the old macOS computer) like:")
    error("    rsync -rtP ~/ user@192.168.1.98:/home/user")
    error("    # ^ where 192.168.1.98 is the IP address of the")
    error("        computer with a GNU+Linux operating system")
    error("        and user is the name of the user that exists on")
    error("        that machine but who has not yet used (or has")
    error("        renamed or cleared) profiles for:")
    error("        {}".format(subs.keys()))
    error("")
    error("-------------------------- Usage --------------------------")
    error("Run the command on the destination computer after the")
    error("transfer is complete:")
    error('  {} <source system> <destination system>'
          ''.format(sys.argv[0]))
    error("")
    error("Example 1 (migrate macOS files to Linux):")
    error('{} Darwin Linux'
          ''.format(sys.argv[0]))


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
        error("* processing {}...".format(program))
        srcSub = systems[fromSystem]
        dstSub = systems[toSystem]
        src = os.path.join(profile, srcSub)
        dst = os.path.join(profile, dstSub)
        if not os.path.exists(src):
            error("  * INFO: \"{}\" doesn't exist"
                  " so it will not be migrated.".format(src))
            continue
        if os.path.exists(dst):
            error("  * INFO: \"{}\" already exists"
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
        error("ERROR: You must specify a source and destination"
              " platform.")
        exit(1)


if __name__ == "__main__":
    main()
