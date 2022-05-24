#!/usr/bin/env python
'''
ggrep
by Jake Gustafson

This program allows you to search using grep then get a geany command to go to a specific line.
- It automatically is recursive, but you can prevent that by specifying a file (that exists) as any parameter.
- It automatically includes only certain files as shown in the output, but you can change the file type using exactly one --include parameter.
- Though it has more output than grep, only results go to standard output (other output goes to stderr).

Differences from grep:
- The output is a geany command for each match rather than bare output.
- Binary files are ignored.
- Basically no special grep options are implemented (-n/--line-number is automatic, -r/--recursive is automatic)
- stderr output differs significantly.

You can install it such as via:
  python3 -m pip install --user linux-preinstall


Then you can use it any time.
For example, if you run:
    ggrep contains_vec3

You can exclude the content and get the line number commands cleanly such as via:
    ggrep contains_vec3 | cut -f1 -d\#


The output (if you don't use "| cut -f1 -d\#") is:

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

When you enter the command, Geany would go to the exact line.

Options
-------
--verbose            Show verbose output.
--extra              Show extra verbose output.
--no-ignore          Do not read .gitignore (If not specified, ggrep will not only ignore .git directories but also read .gitignore files recursively and ignore files and directories specified in the files).
--include-all        Include all file types (For the default grep behavior, you must specify this and --no-ignore but binary files are still ignored).
'''
from __future__ import print_function
import sys
import os
import re
from linuxpreinstall import (
    prerr as error,
    debug,
    extra,
    set_verbose,
)

_include_args = [
    "*.py",
    "*.lua",
    "*.cpp",
    "*.h",
    "*.js",
    "*.sh",
    "*.yml",
    "*.yaml",
    "*.json",
    "*.htm",
    "*.html",
    "*.php",
    "*.inc",
    "*.tmpl",
    "*.po",
    "*.pot",
    "*.twig",
    "*.ini",
    "*.txt",
]

def usage():
    print(__doc__)
    print("Default types included: {}".format(_include_args))
    print("")


def _wild_increment(haystack_c, needle_c):
    if needle_c == "*":
        return 0
    if needle_c == "?":
        return 1
    if needle_c == haystack_c:
        return 1
    return -1


def is_like(haystack, needle, allow_blank=False, quiet=False):
    '''
    It is a filename pattern not regex, so the only wildcards are '*'
    and '?'.

    Sequential arguments:
    needle -- a pattern such as "*.png"
    allow_blank -- Instead of raising an exception on a blank needle,
        return False and show a warning (unless quiet).
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
    if len(needle) == 0:
        if not allow_blank:
            raise ValueError(
                'The needle can\'t be blank or it would match all.'
                ' Set to "*" to match all explicitly.'
            )
        else:
            if not quiet:
                error("The needle is blank so the match will be False.")
        return False
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
    extra("is_like matches={} req_count={}".format(matches, req_count))
    return matches == req_count


def is_like_any(haystack, needles, allow_blank=False, quiet=False):
    for needle in needles:
        if is_like(haystack, needle, allow_blank=allow_blank,
                   quiet=quiet):
            return True
    return False


def grep(pattern, path, more_args=None, include=None, recursive=True,
         quiet=True, ignore=None, ignore_root=None, gitignore=True,
         show_args_warnings=True, allow_non_regex_pattern=True):
    '''
    Keyword arguments:
    include -- Specify a single string or a list of strings that filter
        which files to include. It is a filename pattern not regex (See
        is_like documentation for details).
    recursive -- Recursively search subdirectories (ignored if path
        is a file).
    quiet -- Only return lines, do not print them.
    ignore -- Ignore a list of files (automatically changed to content
        of .gitignore if present and path is a directory and gitignore
        is True).
    ignore_base -- This is required when using ignore since .gitignore
        may have paths starting with "/" and they must be a path
        relative to the gitignore file.
    gitignore -- Set to True to read .gitignore files recursively and
        to ignore files and directories specified in those files.
    show_args_warnings -- Show a warning for each command switch in
        more_args that is not implemented. The value is True for only
        one call. It will be automatically be changed to False before
        another call.
    allow_non_regex_pattern -- Allow the pattern to be in string even if
        pattern is a substring rather than regex.
    '''

    if more_args is not None:
        for arg in more_args:
            if arg == "--include-all":
                raise ValueError("--include-all should set include to None")
            else:
                if show_args_warnings:
                    show_args_warnings = False
                    error("* Warning: {} is not implemented in ggrep."
                          "".format(arg))
    results = []
    if include is None:
        include = ["*"]
    elif isinstance(include, str):
        include = [include]
    if isinstance(ignore, str):
        ignore = [ignore]
    if ignore is not None:
        if not isinstance(ignore_root, str):
            raise ValueError("ignore requires ignore_root")
    sub = os.path.split(path)[1]
    if os.path.isdir(path):
        if sub == ".git":
            error('* ignored "{}"'.format(path))
            return results

    if ignore is not None:
        for rawIgnore in ignore:
            ignore_s = rawIgnore
            checkPath = path
            absolute = False
            if ignore_s.startswith("/"):
                absolute = True
                # ignore_s = [1:]
                # ^ keep "/" since checkPath will start with "/" after
                #   ignore_root is removed in the case of a match.
                checkPath = path
                if checkPath.startswith(ignore_root):
                    checkPath = checkPath[len(ignore_root):]
                    # ^ Now checkPath starts with "/" like ignore_s
            if ignore_s.endswith("/"):
                ignore_s = ignore_s[:-1]
                if absolute:
                    if os.path.isdir(path) and is_like(checkPath, ignore_s):
                        error("* ignored {} due to {}".format(
                            path,
                            os.path.join(ignore_root, ".gitignore"),
                        ))
                        return results
                else:
                    if os.path.isdir(path) and is_like(sub, ignore_s):
                        error("* ignored {} due to .gitignore".format(path))
                        return results
            else:
                if absolute:
                    if os.path.isfile(path) and is_like(checkPath, ignore_s):
                        error("* ignored {} due to .gitignore".format(path))
                        return results
                else:
                    if os.path.isfile(path) and is_like(sub, ignore_s):
                        error("* ignored {} due to .gitignore".format(path))
                        return results
            extra("- {} ({}) doesn't match {}".format(checkPath, path, ignore_s))
    if os.path.isfile(path):
        # debug('* checking "{}"'.format(path))
        if not is_like_any(sub, include):
            return results
        else:
            with open(path, 'r') as ins:
                lineN = 0
                try:
                    extra('* Checking "{}"'.format(path))
                    for rawL in ins:
                        lineN += 1
                        line = rawL.rstrip("\n\r")
                        if (re.search(pattern, line)
                                or (allow_non_regex_pattern
                                    and (pattern in line))):
                            result = "{}:{}:{}".format(
                                path,
                                lineN,
                                line,
                            )
                            results.append(result)
                            if not quiet:
                                print(result)
                        else:
                            extra('  * pattern {} is not in "{}"'
                                  ''.format(pattern, line))
                except UnicodeDecodeError as ex:
                    # 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
                    error('* ignored binary file "{}" due to: {}'.format(path, str(ex)))
                    return results

            return results
    if (len(path) != 0) and (not os.path.isdir(path)):
        # Dangling symlink in this case probably, so return to avoid:
        # "FileNotFoundError: [Errno 2] No such file or directory: "
        # return results
        pass
    tryIgnore = os.path.join(path, ".gitignore")
    if gitignore and os.path.isfile(tryIgnore):
        debug('* reading "{}"'.format(tryIgnore))
        ignore = []
        ignore_root = path
        with open(tryIgnore, 'r') as ins:
            for rawL in ins:
                line = rawL.strip()
                if len(line) < 1:
                    continue
                if line.startswith("#"):
                    continue
                ignore.append(line)
    listPath = path
    if listPath == "":
        listPath = "."
    subs = None
    try:
        subs = os.listdir(listPath)
    except FileNotFoundError:
        error('* missing or inaccessible: "{}"'.format(listPath))
        return results
    for sub in subs:
        # The path is guaranteed *not* to be a file by now.
        subPath = os.path.join(path, sub)
        if path == "":
            subPath = sub
        if recursive or not os.path.isdir():
            results += grep(
                pattern,
                subPath,
                more_args=more_args,
                include=include,
                recursive=recursive,
                quiet=quiet,
                ignore=ignore,
                ignore_root=ignore_root,
                show_args_warnings=show_args_warnings,
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
    global _include_args
    me = "ggrep"
    prev_var = ""
    _found_include = False
    _recursive_arg = None
    _more_args = []
    # ^ defaults
    _n_arg = None
    _include_all = False
    gitignore = True
    pattern = None
    path = None

    for argI in range(1, len(sys.argv)):
        arg = sys.argv[argI]
        if arg == "--help":
            usage()
            return 0
        elif arg == "--include":
            pass
        elif arg == "-r":
            error("* -r (recursive) is already the default.")
        elif arg == "-n":
            _n_arg = "-n"
        elif arg == "--no-ignore":
            gitignore = False
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
                _include_args = None
                _found_include = True
                _include_all = True
            elif arg == "--verbose":
                set_verbose(True)
            elif arg == "--extra":
                set_verbose(2)
            elif prev_var == "--include":
                if _include_all:
                    raise ValueError(
                        "Error: '--include' isn't compatible with"
                        " '--include-all'."
                    )

                if not _found_include:
                    _include_args = []

                _found_include = True
                # grep can accept more than one --include, so force the
                # old one and the new one:
                _include_args.append("--include")
                _include_args.append(arg)
            elif path is None:
                if arg.startswith("-"):
                    if not os.path.exists(arg):
                        raise ValueError(
                            "{} is neither an implemented {} option"
                            " nor a file.".format(arg, me)
                        )
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
    if _include_args is not None:
        includeCount = len(_include_args)
        error("* _include_args count: {}".format(includeCount))
    else:
        error("* _include_args: {}".format(_include_args))

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
        error("  (using ggrep default types since not specified)")
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
    results = grep(pattern, path, more_args=_new_args,
                   include=_include_args, gitignore=gitignore)
    for line in results:
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
        print("geany {} -l {}  # < {}".format(quoted(_file), _line_n, line[colon2+1:]))

    error()
    error("({} match(es))".format(len(results)))
    error()
    error("* to reduce output horizontally, hide line content via:")
    space = ""
    i = 0
    sys.stderr.write("  ")
    for arg in sys.argv:
        if i == 0:
            sys.stderr.write(os.path.split(arg)[1])
        else:
            sys.stderr.write(space+quoted(arg))
        i += 1
        space = " "
    error(" | cut -f1 -d\#")

    if not _include_all:
        error("* to show all file types"
              " (revert to default grep behavior), use:")
        sys.stderr.write("  ")
        # sys.stderr.write("  `basename $0`")
        # ^ Placing >&2 before or after doesn't seem to matter.
        # sys.stderr.write(" ")
        # sys.stderr.write("$@")
        i = 0
        for arg in sys.argv:
            if i == 0:
                sys.stderr.write(os.path.split(arg)[1])
            else:
                sys.stderr.write(" "+arg)
            i += 1
        # ^ TODO: Place quotes around the param if necessary.
        error(" --include-all")
        error("  # and add --no-ignore to search in"
              " .git directories and in files listed in"
              " .gitignore files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
