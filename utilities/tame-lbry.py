#!/usr/bin/env python
import os
import re
import shutil
import psutil

procnames = ["lbry-app", "lbrynet"]
counts = {}
print("* closing...")
for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() in procnames:
        if counts.get(proc.name()) is None:
            counts[proc.name()] = 1
        else:
            counts[proc.name()] += 1
        proc.kill()

for k,v in counts.items():
    print("({}) {}".format(v, k)) 
print("(Finished OK)")
