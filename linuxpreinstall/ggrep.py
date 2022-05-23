#!/usr/bin/env python
'''
ggrep
by Jake Gustafson

This program allows you to search using grep then get a geany command to go to a specific line.
- It automatically is recursive, but you can prevent that by specifying a file (that exists) as any parameter.
- It automatically includes *.py files, but you can change the file type using exactly one --include parameter.

You can install it such as via:
  cd linux-preinstall
  sudo ln -s `pwd`/utilities/ggrep /usr/local/bin/ggrep


Then you can use it any time.
For example, if you run:
    ggrep contains_vec3

You can exclude the content and get the line number commands cleanly such as via:
    ggrep contains_vec3 | cut -f1 -d:


The output (if you don't use "| cut -f1 -d:") is:

* ggrep is passing along extra arguments to grep:  contains_vec3
grep -r contains_vec3 -n
results:

geany pyglops.py -l 606 # < pyglops.py:606:def hitbox_contains_vec3(o, pos):
geany kivyglops.py -l 1848 # < kivyglops.py:1848:                                               self.glops[bumper_index].properties['hitbox'].contains_vec3(get_vec3_from_point(self.glops[bumpable_index]._t_ins)):
# END of output


Then you can simply paste (There is no need to copy and paste using
hotkeys. Simply utilize the auto-copy feature of linux: In a GUI
terminal window, select (left click and drag) the command in the part
above, then middle click to get):
  geany pyglops.py -l 606


When you press enter, Geany will go to the exact line.
'''
from __future__ import print_function
import sys
import os
import re
from linuxpreinstall import (
    prerr as error,
    debug,
)

def usage():
    print(__doc__)


def _wild_increment(haystack_c, needle_c):
    if needle_c == "*":
        return 0
    if needle_c == "?":
        return 1
    if needle_c == haystack_c:
        return 1
    return -1


def is_like(haystack, needle):
    '''
    It is a filename pattern not regex, so the only wildcards are '*'
    and '?'.

    Sequential arguments:
    needle -- a pattern such as "*.png"
    '''
    req_count = 0
    prev_c = None
    for c in needle:
        if c == "*":
            if prev_c == "*":
                raise ValueError(
                    "More than one '*' in a row isn't allowed."
                )
            prev_c = c
            continue
        req_count += 1
        prev_c = c
    if req_count == 0:
        return True
    hI = 0
    nI = 0
    matches = 0
    while hI < len(haystack):
        if nI >= len(needle):
            # If still in haystack, there are more things to match so
            # there aren't enough needle characters/wildcards.
            return False
        inc = _wild_increment(haystack[hI], needle[nI])
        if inc == 0:
            # *
            if nI == (len(needle)-1):
                # The needle ends with *, so the matching is complete.
                return True
            next_needle_c = needle[nI+1]
            if next_needle_c == haystack[hI]:
                nI += 2
                matches += 1  # Only 1 since req_count doesn't have '*'
            hI += 1
        elif inc == 1:
            hI += 1
            nI += 1
            matches += 1
        elif inc == -1:
            return False
    debug("is_like matches={} req_count={}".format(matches, req_count))
    return matches == req_count


def is_like_any(haystack, needles):
    for needle in needles:
        if is_like(haystack, needle):
            return True
    return False


def grep(pattern, path, more_args=None, include=None, recursive=True, quiet=True):
    '''
    Keyword arguments:
    include -- Specify a single string or a list of strings that filter
        which files to include. It is a filename pattern not regex (See
        is_like documentation for details).
    recursive -- Recursively search subdirectories (ignored if path
        is a file).
    quiet -- Only return lines, do not print them.
    '''
    if more_args is not None:
        for arg in more_args:
            if arg == "--include-all":
                raise ValueError("--include-all should set include to None")
            else:
                error("* Warning: {} is not implemented in ggrep."
                      "".format(arg))
    results = []
    if include is None:
        include = ["*"]
    elif isinstance(include, str):
        include = [include]
    sub = os.path.split(path)[1]
    if os.path.isfile(path):
        if not is_like_any(sub, include):
            return results
        else:
            with open(path, 'r') as ins:
                lineN = 0
                for rawL in ins:
                    lineN += 1
                    line = rawL.rstrip("\n\r")
                    if re.search(pattern, line):
                        result = "{}:{}:{}".format(
                            path,
                            lineN,
                            line,
                        )
                        results.append(result)
                        if not quiet:
                            print(result)
            return results

    listPath = path
    if listPath == "":
        listPath = "."
    for sub in os.listdir(listPath):
        # The path is guaranteed to not be a file by now.
        subPath = os.path.join(path, sub)
        if path == "":
            subPath = sub
        if recursive or not os.path.isdir():
            results += grep(
                pattern,
                subPath,
                include=include,
                recursive=recursive,
            )

    return results


def quoted(path):
    '''
    Make the path usable in a CLI.
    '''
    if "'" in path:
        path = '"{}"'.format(path.replace('"', '\\"'))
    elif " " in path:
        path = "'{}'".format(path)
    return path


# TODO: Ignore the .git directory.
def main():
    me = "ggrep"
    prev_var = ""
    _found_include = False
    _recursive_arg = None
    _more_args = []
    _include_args = [
        "*.py",
        "*.lua",
        "*.cpp",
        "*.h",
        "*.js",
        "*.sh",
    ]
    # ^ defaults
    _n_arg = None
    _include_all = False
    pattern = None
    path = None

    for argI in range(1, len(sys.argv)):
        arg = sys.argv[argI]
        if arg == "--include":
            pass
        elif arg == "-r":
            error("* -r (recursive) is already the default.")
        elif arg == "-n":
            _n_arg = "-n"
        elif arg == "--recursive":
            _recursive_arg = True
            # error("* -r (recursive) is already the default.")
        elif pattern is None:
            pattern = arg
        else:
            if os.path.isfile(arg):
                _recursive_arg = False
                error('* turning off recursive mode (default in ggrep)'
                      ' since "{}" is a file'.format(arg))
            elif arg == "--include-all":
                if _found_include:
                    raise ValueError(
                        "Error: '--include-all' isn't compatible with"
                        " '--include'."
                    )

                error("* removing the default '--include' option so all are included.")
                _include_args=()
                _found_include = True
                _include_all = True
            elif prev_var == "--include":
                if _include_all:
                    raise ValueError(
                        "Error: '--include' isn't compatible with"
                        " '--include-all'."
                    )

                if not _found_include:
                    _include_args=()

                _found_include = True
                # grep can accept more than one --include, so force the
                # old one and the new one:
                _include_args.append("--include")
                _include_args.append(arg)
            elif path is None:
                path = arg
            else:
                _more_args.append(arg)



        if arg == "-n":
            error("* -n is already the default (required for"
                  " the functionality of {}).".format(me))
            prev_var = ""
        else:
            prev_var = arg

    if path is None:
        path = ""

    if prev_var == "--include":
        raise ValueError(
            "Error: You must specify a filename pattern after"
            " --include such as \"*.lua\""
            "(including quotes if using asterisk(s)!) ."
        )

    count = len(_more_args)
    error("* _more_args count: {}".format(count))
    includeCount = len(_include_args)
    error("* _include_args count: {}".format(includeCount))

    if _n_arg is None:
        _n_arg = "-n"
        # The line number (obtained via -n) is required for this script's
        # main purpose.

    if _recursive_arg is None:
        _recursive_arg = True

    error("* _more_args: {}".format(_more_args))
    error("* _include_args: {}".format(_include_args))
    _new_args = _more_args

    if not _found_include:
        error("  (use --include-all for all files, the default grep behavior)")
    else:
        error("* _found_include: {}".format(_found_include))

    sys.stderr.write("grep")
    for value in _new_args:
        if " " in value:
            sys.stderr.write(' "{}"'.format(value))
        else:
            sys.stderr.write(" {}".format(value))
        sys.stderr.flush()
    error()
    error()
    error('results (looking for "{}" in "{}"):'.format(pattern, path))
    error()
    for line in grep(pattern, path, more_args=_new_args, include=_include_args):
        colon1 = line.find(":")
        colon2 = line.find(":", colon1+1)
        if colon2 <= colon1:
            raise RuntimeError(
                "The grep result must have the line for {}"
                " to work but doesn't have 2 colons: {}"
                "".format(me, line)
            )
        _line_n = line[colon1+1:colon2]
        _file = line[:colon1]
        print("geany {} -l {}".format(quoted(_file), _line_n))

    error()
    error()
    error("* to reduce output horizontally, hide line content via:")
    space = ""
    for arg in sys.argv:
        sys.stderr.write(space+quoted(arg))
        space = " "
    error(" | cut -f1 -d\#")

    if not _include_all:
        error("* to show all file types (revert to default grep behavior), use:")
        # sys.stderr.write("  `basename $0`")
        # ^ Placing >&2 before or after doesn't seem to matter.
        # sys.stderr.write(" ")
        # sys.stderr.write("$@")
        for arg in sys.argv:
            sys.stderr.write(" "+arg)
        # ^ TODO: Place quotes around the param if necessary.
        error(" --include-all")
    return 0


if __name__ == "__main__":
    sys.exit(main())
