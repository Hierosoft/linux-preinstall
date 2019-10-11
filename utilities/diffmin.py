#!/usr/bin/env python
from __future__ import print_function
import sys

# see <https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python>
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if len(sys.argv) < 3:
    eprint("You must specify two files.")
    exit(1)

# NOTE: sys.argv[0] is this script.
fName = sys.argv[1]
docDict = {}
count = 0
with open(fName, 'r') as f:
    for lineOriginal in f:
	if not lineOriginal: break
	line = lineOriginal.strip()
	docDict[line] = True
	count += 1
eprint("- read " + str(count) + " line(s)")

f2Name = sys.argv[2]

count = 0
newCount = 0
with open(f2Name, 'r') as f:
    eprint("Reading " + f2Name + "...")
    for lineOriginal in f:
	line = lineOriginal.strip()
	if docDict.get(line) is None:
	    print(lineOriginal.rstrip())
	    newCount += 1
	count += 1
eprint("- read " + str(count) + " line(s)")
eprint("- " + str(newCount) + " new line(s).")

