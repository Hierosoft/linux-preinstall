#!/usr/bin/env python
'''Replace extension of all files in the current directory with a new
extension if the file has the old extension (not case sensitive).
'''
import os
import sys
import shutil

def usage():
    print("  {} <old_extension> <new_extension>".format(sys.argv[0]))

if len(sys.argv) < 3:
    print("You must specify an old and new extension.")
    usage()
    exit(1)

old_ext = sys.argv[1]
new_ext = sys.argv[2]

folder_path = "."
for sub in os.listdir(folder_path):
    sub_path = os.path.join(folder_path, sub)
    if os.path.isfile(sub_path) and (sub[:1] != "."):
	if sub[-(len(old_ext)+1):] == ("." + old_ext):  # +1 for dot
	    # print(sub[:-(len(old_ext)+1)] + "." + new_ext)
	    shutil.move(sub, sub[:-(len(old_ext)+1)] + "." + new_ext)
