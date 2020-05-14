#!/usr/bin/env python3
"""
Check the size of subdirectories (not files) in a given directory.
"""
from __future__ import print_function
from __future__ import division

import os
import sys
units = ["bytes", "kb", "mb", "gb"]
default_un = "mb"

def bytes_to(size_bytes, unit):
    unit_upper = unit.upper()
    if unit_upper == "BYTES":
        return size_bytes
    elif unit_upper == "KB":
        return size_bytes / 1024.0
    elif unit_upper == "MB":
        return size_bytes / 1024.0 / 1024.0
    elif unit_upper == "GB":
        return size_bytes / 1024.0 / 1024.0 / 1024.0
    elif unit_upper == "TB":
        return size_bytes / 1024.0 / 1024.0 / 1024.0 / 1024.0
    else:
        raise ValueError("{} is not a valid unit. Try: {}"
                         "".format(unit, units))


def get_size(start_path='.', unit="bytes"):
    """
    See <https://stackoverflow.com/questions/1392413/calculating-a-
    directorys-size-using-python>.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for sub in filenames:
            sub_path = os.path.join(dirpath, sub)
            # skip if it is symbolic link
            if not os.path.islink(sub_path):
                total_size += bytes_to(os.path.getsize(sub_path), unit)
    return total_size

def usage():
    print(__doc__)
    print("USAGE")
    print("-----")
    me = os.path.split(sys.argv[0])[-1]
    print("")
    print("{} <directory> [options]".format(me))
    print("")
    print("OPTIONS:")
    print("")
    opt_fmt = "{:<14}     {}"
    print(opt_fmt.format("--help", "Show this screen."))
    print(opt_fmt.format("--sort",
                                 "Sort the results (ascending)."))
    print(opt_fmt.format("--unit <unit>",
                                 "Show sizes in: "+str(units)))
    print(opt_fmt.format("", "(default: {})".format(default_un)))
    print("")

def main():
    root_path = "."
    prev_arg = None
    enable_sort = False
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        parts = arg.split("=")
        if arg.startswith("--") and (len(parts) > 1):
            prev_arg = parts[0]
            arg = parts[1]
        if prev_arg == "--unit":
            unit = arg
        elif arg == "--sort":
            enable_sort = True
        elif arg == "--help":
            usage()
            exit(0)
        else:
            root_path = sys.argv[1]
    total_as_unit = 0.0
    unit = default_un.upper()
    stats = []
    if enable_sort:
        print("sorting...")
    for sub in os.listdir(root_path):
        sub_path = os.path.join(root_path, sub)
        if os.path.isdir(sub_path) and not sub.startswith("."):
            sub_size = get_size(sub_path, unit=unit)
            total_as_unit += sub_size
            if not enable_sort:
                print("{}: {} {}".format(sub_path, sub_size, unit))
            else:
                stats.append({"size": sub_size, "path": sub_path})
    if enable_sort:
        sorted_stats = sorted(stats, key=lambda k: k['size'])
        for stat in sorted_stats:
            print("{}: {} {}".format(stat["path"], stat["size"], unit))
    print("{}: {} {}".format("TOTAL",total_as_unit, unit))


if __name__ == "__main__":
    main()
