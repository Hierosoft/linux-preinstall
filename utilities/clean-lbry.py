#!/usr/bin/env python
import os
import re
import shutil
parents = []
parents.append(
    os.path.join(os.environ["HOME"], ".local", "share", "lbry",
                 "lbrynet", "blobfiles")
)
# ^ last used 13 days ago on test user's computer 178 GB). I'm not sure
#   why it was that recent, because the deb package was removed a while
#   back.
parents.append(
    os.path.join(os.environ["HOME"], ".var", "app", "io.lbry.lbry-app",
                 "data", "lbry", "lbrynet", "blobfiles")
)
# ^ IT was last used 4 days ago on test user's computer (46.9 GB), so it
#   is probably the flatpak packaged one.
count = 0
deletedMB = 0
for parent in parents:
    if not os.path.isdir(parent):
        print("Error: \"{}\" is missing.".format(Downloads))
        break
    thisCount = 0
    for sub in os.listdir(parent):
        if sub.startswith("."):
            continue
        subPath = os.path.join(parent, sub)
        deletedMB += os.stat(subPath).st_size/1024/1024
        os.remove(subPath)
        print(subPath)
        thisCount += 1
        print("- {}".format(subPath))
        count += thisCount
print("* deleted {} MB ({} file(s))".format(deletedMB, count))
print("You can close this window.")
