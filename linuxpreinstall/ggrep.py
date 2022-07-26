#!/usr/bin/env python
'''
ggrep
by Jake Gustafson

This program allows you to search using grep then get a geany command
to go to a specific line.
- It automatically is recursive, but you can prevent that by specifying
  a file (that exists) as any parameter.
- It automatically includes only certain files as shown in the output,
  but you can change the file type using exactly one --include
  parameter.
- Though it has more output than grep, only results go to standard
  output (other output goes to stderr).

Differences from grep:
- The output is a geany command for each match rather than bare output.
- Binary files are ignored.
- Basically no special grep options are implemented (-n/--line-number is
  automatic, -r/--recursive is automatic)
- stderr output differs significantly.

You can install it such as via:
  python3 -m pip install --user linux-preinstall


Then you can use it any time.
For example, if you run:
    ggrep contains_vec3

You can exclude the content and get the line number commands cleanly
    such as via:
    ggrep contains_vec3 | cut -f1 -d\\#


The output (if you don't use "| cut -f1 -d\\#") is:

* ggrep is passing along extra arguments to grep:  contains_vec3
grep -r contains_vec3 -n
results:

geany pyglops.py -l 606 # < pyglops.py:606:def hitbox_contains_vec3(o,\
 pos):
geany kivyglops.py -l 1848 # < kivyglops.py:1848:\
self.glops[bumper_index].properties['hitbox']\
.contains_vec3(get_vec3_from_point(self.glops[bumpable_index]._t_ins)):
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
--debug              Show extra verbose output.
--no-ignore          Do not read .gitignore (If not specified, ggrep
                     will not only ignore .git directories but also
                     read .gitignore files recursively and ignore files
                     and directories specified in the files).
--include-all        Include all file types (For the default grep
                     behavior, you must specify this and --no-ignore
                     but binary files are still ignored).
'''
from __future__ import print_function
import sys
import os
import re
import json
import platform

from linuxpreinstall import (
    echo0,  # formerly prerr as error
    echo1,  # formerly debug
    echo2,  # formerly extra
    echo3,
    set_verbosity,
)

default_includes = [
    "*.py",
    "*.lua",
    "*.c",
    "*.cxx",
    "*.cpp",
    "*.h",
    "*.hpp",
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
    "*.desktop",
]

GREP_DOC = '''
Usage: grep [OPTION]... PATTERNS [FILE]...
Search for PATTERNS in each FILE.
Example: grep -i 'hello world' menu.h main.c
PATTERNS can contain multiple patterns separated by newlines.

Pattern selection and interpretation:
  -E, --extended-regexp     PATTERNS are extended regular expressions
  -F, --fixed-strings       PATTERNS are strings
  -G, --basic-regexp        PATTERNS are basic regular expressions
  -P, --perl-regexp         PATTERNS are Perl regular expressions
  -e, --regexp=PATTERNS     use PATTERNS for matching
  -f, --file=FILE           take PATTERNS from FILE
  -i, --ignore-case         ignore case distinctions in patterns and data
      --no-ignore-case      do not ignore case distinctions (default)
  -w, --word-regexp         match only whole words
  -x, --line-regexp         match only whole lines
  -z, --null-data           a data line ends in 0 byte, not newline

Miscellaneous:
  -s, --no-messages         suppress error messages
  -v, --invert-match        select non-matching lines
  -V, --version             display version information and exit
      --help                display this help text and exit

Output control:
  -m, --max-count=NUM       stop after NUM selected lines
  -b, --byte-offset         print the byte offset with output lines
  -n, --line-number         print line number with output lines
      --line-buffered       flush output on every line
  -H, --with-filename       print file name with output lines
  -h, --no-filename         suppress the file name prefix on output
      --label=LABEL         use LABEL as the standard input file name prefix
  -o, --only-matching       show only nonempty parts of lines that match
  -q, --quiet, --silent     suppress all normal output
      --binary-files=TYPE   assume that binary files are TYPE;
                            TYPE is 'binary', 'text', or 'without-match'
  -a, --text                equivalent to --binary-files=text
  -I                        equivalent to --binary-files=without-match
  -d, --directories=ACTION  how to handle directories;
                            ACTION is 'read', 'recurse', or 'skip'
  -D, --devices=ACTION      how to handle devices, FIFOs and sockets;
                            ACTION is 'read' or 'skip'
  -r, --recursive           like --directories=recurse
  -R, --dereference-recursive
                            likewise, but follow all symlinks
      --include=GLOB        search only files that match GLOB (a file pattern)
      --exclude=GLOB        skip files that match GLOB
      --exclude-from=FILE   skip files that match any file pattern from FILE
      --exclude-dir=GLOB    skip directories that match GLOB
  -L, --files-without-match print only names of FILEs with no selected lines
  -l, --files-with-matches  print only names of FILEs with selected lines
  -c, --count               print only a count of selected lines per FILE
  -T, --initial-tab         make tabs line up (if needed)
  -Z, --null                print 0 byte after FILE name

Context control:
  -B, --before-context=NUM  print NUM lines of leading context
  -A, --after-context=NUM   print NUM lines of trailing context
  -C, --context=NUM         print NUM lines of output context
  -NUM                      same as --context=NUM
      --group-separator=SEP use SEP as a group separator
      --no-group-separator  use empty string as a group separator
      --color[=WHEN],
      --colour[=WHEN]       use markers to highlight the matching strings;
                            WHEN is 'always', 'never', or 'auto'
  -U, --binary              do not strip CR characters at EOL (MSDOS/Windows)

When FILE is '-', read standard input.  With no FILE, read '.' if
recursive, '-' otherwise.  With fewer than two FILEs, assume -h.
Exit status is 0 if any line is selected, 1 otherwise;
if any error occurs and -q is not given, the exit status is 2.

Report bugs to: bug-grep@gnu.org
GNU grep home page: <http://www.gnu.org/software/grep/>
General help using GNU software: <https://www.gnu.org/gethelp/>
'''
GREP_ARGS = []
GREP_WHENS = ["always", "never", "auto"]
GREP_TYPES = ['binary', 'text', 'without-match']
GREP_DIR_ACTIONS = ['read', 'recurse', 'skip']
GREP_DEV_ACTIONS = ['read', 'skip']
for word in GREP_DOC.split():
    if word.startswith("-"):
        if word.endswith(","):
            word = word[:-1]
        signI = word.find("=")
        if word.endswith("[=WHEN]"):
            signI -= 1
            for grep_when in GREP_WHENS:
                GREP_ARGS.append(word[:signI]+"="+grep_when)
        elif signI > -1:
            if word[signI+1:] == "TYPE":
                for grep_type in GREP_TYPES:
                    GREP_ARGS.append(word[:signI]+"="+grep_type)
            elif word[:signI] == "--directories":
                for grep_dir_action in GREP_DIR_ACTIONS:
                    GREP_ARGS.append(word[:signI]+"="+grep_dir_action)
            elif word[:signI] == "--devices":
                for grep_dev_action in GREP_DEV_ACTIONS:
                    GREP_ARGS.append(word[:signI]+"="+grep_dev_action)
            else:
                GREP_ARGS.append(word[:signI+1])
                # ^ include the sign so it can be used as a startswith param
        else:
            GREP_ARGS.append(word)

class DontStopIteration(Exception):
    '''
    End the recursive generator early without return (which is the
    same as StopIteration) but allow iteration to continue.
    '''
    pass


def is_grep_arg(arg):
    for word in GREP_ARGS:
        if word.endswith("="):
            if arg.startswith(word):
                return True
        else:
            if arg == word:
                return True
    return False

def usage():
    print(__doc__)
    print("Default types included: {}".format(default_includes))
    print("")


def _wild_increment(haystack_c, needle_c):
    if needle_c == "*":
        return 0
    if needle_c == "?":
        return 1
    if needle_c == haystack_c:
        return 1
    return -1

# region same as nopackage


def contains(haystack, needle, allow_blank=False, quiet=False):
    '''
    Check if the substring "needle" is in haystack. The behavior differs
    from the Python "in" command according to the arguments described
    below.

    Sequential arguments:
    haystack -- a string to look in
    needle -- a string for which to look
    allow_blank -- Instead of raising an exception on a blank needle,
        return False and show a warning (unless quiet).
    quiet -- Do not report errors to stderr.

    Raises:
    ValueError -- If allow_blank is not True, a blank needle will raise
        a ValueError, otherwise there will simply be a False return.
    TypeError -- If no other error occurs, the "in" command will raise
        "TypeError: argument of type 'NoneType' is not iterable" if
        haystack is None (or haystack and needle are None), or
        "TypeError: 'in <string>' requires string as left operand, not
        NoneType" it needle is None.
    '''
    if len(needle) == 0:
        if not allow_blank:
            raise ValueError(
                'The needle can\'t be blank or it would match all.'
                ' Set to "*" to match all explicitly.'
            )
        else:
            if not quiet:
                echo0("The needle is blank so the match will be False.")
        return False
    return needle in haystack


def any_contains(haystacks, needle, allow_blank=False, quiet=False,
                 case_sensitive=True):
    '''
    Check whether any haystack contains the needle.
    For documentation of keyword arguments, see the "contains" function.

    Returns:
    bool -- The needle is in any haystack.
    '''
    if not case_sensitive:
        needle = needle.lower()
    for rawH in haystacks:
        haystack = rawH
        if not case_sensitive:
            haystack = rawH.lower()
        # Passing case_sensitive isn't necessary since lower()
        # is already one in that case above:
        if contains(haystack, needle, allow_blank=allow_blank, quiet=quiet):
            echo1("is_in_any: {} is in {}".format(needle, haystack))
            return True
    return False


def contains_any(haystack, needles, allow_blank=False, quiet=False,
                 case_sensitive=True):
    '''
    Check whether the haystack contains any of the needles.
    For documentation of keyword arguments, see the "contains" function.

    Returns:
    bool -- Any needle is in the haystack.
    '''
    if not case_sensitive:
        needle = haystack.lower()
    for rawN in needles:
        needle = rawN
        if not case_sensitive:
            needle = rawN.lower()
        # Passing case_sensitive isn't necessary since lower()
        # is already one in that case above:
        if contains(haystack, needle, allow_blank=allow_blank, quiet=quiet):
            echo3("is_in_any: {} is in {}".format(needle, haystack))
            return True
    return False


# endregion same as nopackage

def is_abs_path(path):
    if platform.system() == "Windows":
        if (len(path) > 1):
            if str.isalpha(path[0]) and (path[1] == ":"):
                return True
        if path.startswith("//"):
            return True
    else:
        if path.startswith("/"):
            return True
    return False


def is_like(haystack, needle, allow_blank=False, quiet=False,
            haystack_start=None, needle_start=None, indent=2):
    '''
    Check if haystack is like needle (See needle and other arguments for
    details).

    Sequential arguments:
    haystack -- a string in which to find the needle.
    needle -- It is a filename pattern such as "*.png" not regex, so the
        only wildcards are '*' and '?'.

    Keyword arguments:
    allow_blank -- Instead of raising an exception on a blank needle,
        return False and show a warning (unless quiet).
    quiet -- Do not report errors to stderr.
    haystack_start -- Start at this character index in haystack.
    needle_start -- Start at this character index in needle.
    indent -- Set the visual indent level for debug output, expressed as
        a number of spaces. The default is 2 since some higher level
        debugging will normally be taking place and calling this
        method.
    '''
    tab = " " * indent
    if haystack_start is None:
        haystack_start = 0
    if needle_start is None:
        needle_start = 0
    haystack = haystack[haystack_start:]
    needle = needle[needle_start:]
    echo3(tab+"in is_like({}, {})"
          "".format(json.dumps(haystack), json.dumps(needle)))
    if needle_start == 0:
        double_star_i = needle.find("**")
        if "***" in needle:
            raise ValueError("*** is an invalid .gitignore wildcard.")
        if needle == "**":
            raise ValueError("** would match every directory!")
        if (double_star_i > 0):
            # and (double_star_i < len(needle) - 2):
            # It is allowed to be at the end.
            echo3(tab+"* splitting needle {} at **"
                  "".format(json.dumps(needle)))
            left_needle = needle[:double_star_i] + "*"
            right_needle = needle[double_star_i+2:]
            echo3(tab+"* testing left_needle={}"
                  "".format(json.dumps(left_needle)))
            if is_like(haystack, left_needle,
                       allow_blank=allow_blank, quiet=quiet,
                       indent=indent+2):
                right_haystack = haystack[len(left_needle)-1:]
                # ^ -1 to skip '*'
                # ^ -2 to skip '*/' but that's not all that needs to be
                #   skipped, the whole matching directory needs to be
                #   skipped, so:
                next_slash_i = right_haystack.find("/")
                if next_slash_i > -1:
                    right_haystack = right_haystack[next_slash_i:]
                elif right_needle == "":
                    echo3(tab+"  * there is no right side,"
                          " so it matches")
                    # ** can match any folder, so the return is True
                    # since:
                    # - There is nothing to match after **, so any
                    #   folder (leaf only though) matches.
                    # - The remainder of haystack has no slash, so it is
                    #   a leaf.
                    return True
                echo3(tab+"* testing right_haystack={}, right_needle={}"
                      "".format(json.dumps(right_haystack),
                                json.dumps(right_needle)))
                if (right_needle == ""):
                    if (right_haystack == ""):
                        return True
                    else:
                        echo3(tab+"* WARNING: right_haystack")
                return is_like(right_haystack, right_needle,
                               allow_blank=True, quiet=quiet,
                               indent=indent+2)
            else:
                echo3(tab+"  * False")
                # It is already false, so return
                # (prevent issue 22: "More than one '*' in a row").
                return False
        if needle.startswith("**/"):
            needle = needle[1:]
            # It is effectively the same, and is only different when
            # a subfolder is specified (See
            # <https://git-scm.com/docs/gitignore#:~:
            # text=Two%20consecutive%20asterisks%20(%22%20**%20%22,
            # means%20match%20in%20all%20directories.>.
            # That circumstance is tested in test_ggrep.py.
        elif needle.startswith("!"):
            raise ValueError(
                "The value should not start with '!'."
                " The higher-level logic should check for inverse"
                " results and handle them differently."
            )
    req_count = 0
    prev_c = None
    for i in range(0, len(needle)):
        # ^ 0 since needle = needle[needle_start:]
        c = needle[i]
        if c == "*":
            if prev_c == "*":
                raise ValueError(
                    "More than one '*' in a row in needle isn't allowed"
                    " (needle={}). Outer logic should handle special"
                    " syntax if that is allowed."
                    "".format(json.dumps(needle))
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
                echo0(
                    tab
                    + "The needle is blank so the match will be False."
                )
        return False
    if req_count == 0:
        # req_count may be 0 even if has one character: "*"
        return True
    hI = 0  # 0 since haystack = haystack[haystack_start:]
    nI = 0  # 0 since needle = needle[needle_start:]
    matches = 0
    while hI < len(haystack):
        if nI >= len(needle):
            # If still in haystack, there are more things to match so
            # there aren't enough needle characters/wildcards.
            return False
        inc = _wild_increment(haystack[hI], needle[nI])
        if inc == 0:
            # *
            if (nI+1) == len(needle):
                # The needle ends with *, so the matching is complete.
                return True
            match_indices = []
            next_needle_c = needle[nI+1]
            echo3(tab+"* checking for each possible continuation of"
                  " needle[needle.find('*')+1]"
                  " in haystack {}[{}:] -> {}"
                  .format(haystack, hI, haystack[hI:]))
            for try_h_i in range(hI, len(haystack)):
                if haystack[try_h_i] == next_needle_c:
                    echo3(tab+"  * is_like({}[{}:] -> {}, {}[{}+1:]"
                          " -> {})"
                          "".format(haystack, try_h_i,
                                    haystack[try_h_i:],
                                    needle, nI, needle[nI+1:]))
                    if is_like(haystack, needle,
                               allow_blank=allow_blank,
                               quiet=quiet, haystack_start=try_h_i,
                               needle_start=nI+1,
                               indent=indent+2):
                        echo3(tab+"    * True")
                        # The rest may match from ANY starting point of
                        # the character after *, such as:
                        # abababc is like *ababc (should be True)
                        # - If next_needle_c were used, that wouldn't
                        #   return True as it should.
                        # - To return True, the recursion will occur
                        #   twice:
                        #   - (abababc, ababc) -> False
                        #   - (ababc, ababc) -> True
                        #   - or:
                        #     - (abababc, a*c) -> False
                        #     - (ababc, a*c) -> True
                        return True
                    else:
                        echo3(tab+"    * False")

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
    echo3(tab+"is_like matches={} req_count={}"
          "".format(matches, req_count))
    return matches == req_count


def is_like_any(haystack, needles, allow_blank=False, quiet=False):
    for needle in needles:
        if is_like(haystack, needle, allow_blank=allow_blank,
                   quiet=quiet):
            return True
    return False


def ggrep(pattern, path, more_args=None, include=None, recursive=True,
          quiet=True, ignore=None, ignore_root=None, gitignore=True,
          show_args_warnings=True, allow_non_regex_pattern=True,
          trace_ignore_files={}, follow_symlinks=True,
          followed_symlink_targets=[]):
    '''
    Find a pattern within files in a given path (or one file if path is
    a file) and yield the next for each.

    Sequential arguments:
    pattern -- a regular expression or plain text substring

    Keyword arguments:
    allow_non_regex_pattern -- Allow the pattern to be in string even if
        pattern is a substring rather than regex.
    '''

    results = []
    try:
        for sub in filter_tree(path, more_args=more_args,
                               include=include, recursive=recursive,
                               quiet=quiet, ignore=ignore,
                               ignore_root=ignore_root,
                               gitignore=gitignore,
                               show_args_warnings=show_args_warnings,
                               trace_ignore_files=trace_ignore_files,
                               follow_symlinks=follow_symlinks,
                               followed_symlink_targets=followed_symlink_targets):
            # subPath = os.path.join(path, sub)
            # if path == "":
            #     subPath = sub
            # if not os.path.isfile(subPath):
            if not os.path.isfile(os.path.realpath(sub)):
                # echo3('- not a file: "{}"'.format(sub))
                continue
            else:
                pass
                # echo3("- examining file: {}".format(sub))
            with open(sub, 'r') as ins:
                lineN = 0
                try:
                    echo3('* Checking "{}"'.format(sub))
                    for rawL in ins:
                        lineN += 1
                        line = rawL.rstrip("\n\r")
                        if (re.search(pattern, line)
                                or (allow_non_regex_pattern
                                    and (pattern in line))):
                            result = "{}:{}:{}".format(
                                sub,
                                lineN,
                                line,
                            )
                            results.append(result)
                            if not quiet:
                                print(result)
                        else:
                            pass
                            # echo3('  * pattern "{}" is not in line'
                            #       ' "{}"'.format(pattern, line))
                except UnicodeDecodeError as ex:
                    # 'utf-8' codec can't decode byte 0x89 in position
                    #  0: invalid start byte
                    echo0('* ignored binary file "{}" due to: {}'
                          ''.format(sub, str(ex)))
                    # return results
                    continue
    except DontStopIteration as ex:
        raise RuntimeError(
            "The specified path itself was filtered"
            " (This should never happen): {}".format(str(ex))
        )
        pass
        # results.append(sub)
    # for result in results:
    #     print(result)
    return results

TRIVIAL_EXCLUSION_INCLUDES = "is not in includes"
TRIVIAL_INCLUSION_IN_INCLUDES = "is in includes"
TRIVIAL_EXCEPTION_FLAGS = [
    TRIVIAL_EXCLUSION_INCLUDES,
    TRIVIAL_INCLUSION_IN_INCLUDES,
]

def filter_tree(path, more_args=None, include=None, recursive=True,
                quiet=True, ignore=None, ignore_root=None, gitignore=True,
                show_args_warnings=True,
                trace_ignore_files={}, follow_symlinks=True,
                followed_symlink_targets=[], root=None):
    '''
    Find the entire subtree of files and directories in a given path and
    yield the next for each.

    Sequential arguments:
    path -- Search this file or directory (limited by arguments
        described below). If "", the current directory will be searched
        but excluded from the beginning of each result.

    Keyword arguments:
    include -- Specify a single string or a list of strings that filter
        which files to include. It is a filename pattern not regex (See
        is_like documentation for details). It does not affect which
        directories are yielded (only ignore does).
    recursive -- Recursively search subdirectories (ignored if path is a
        file).
    quiet -- Only return lines, do not print them.
    ignore -- Ignore a list of files (automatically changed to content
        of .gitignore if present and path is a directory and gitignore
        is True).
    ignore_root -- This is required when using ignore since .gitignore
        may have paths starting with "/" and they must be a path
        relative to the gitignore file.
    gitignore -- Set to True to read .gitignore files recursively and to
        ignore files and directories specified in those files.
    show_args_warnings -- Show a warning for each command switch in
        more_args that is not implemented. The value is True for only
        one call. It will be automatically be changed to False before
        another call.
    trace_ignore_files -- Like ignore, this is generated automatically.
        If you set ignore manually, you should also initialize
        trace_ignore_files manually, but it will be updated
        automatically in the same way as ignore (See ignore
        documentation). Set the key to the ignore and the value to the
        file so that an invalid pattern can be traced back to a file
        for error reporting purposes.
    follow_symlinks -- Follow symlinked directories.
    followed_symlink_targets -- This is automatically generated. Any
        symlink target that was followed already won't be followed
        again, even if relative and recursive.
    root -- Set the root directory upon which to add sub (only used for
        tracking, and automatically set).
    '''
    # echo2('filter_tree("{}")'.format(path))
    if root is None:
        root = path
    if more_args is not None:
        for arg in more_args:
            if arg == "--include-all":
                raise ValueError(
                    "--include-all should set include to None, not be"
                    " sent to ggrep."
                )
            else:
                if show_args_warnings:
                    show_args_warnings = False
                    echo0("* Warning: {} is not implemented in filter_subs."
                          "".format(arg))
    if include is None:
        include = ["*"]
    elif isinstance(include, str):
        include = [include]
    if isinstance(ignore, str):
        ignore = [ignore]
    ig_path = ".gitignore"
    if ignore is not None:
        if not isinstance(ignore_root, str):
            raise ValueError("ignore requires ignore_root")
        else:
            ig_path = os.path.join(ignore_root, ".gitignore")
    sub = os.path.split(path)[1]
    # Do not ignore if "" even if .git, so let sub  ""--isdir("")==False
    if os.path.isdir(path):
        if sub == ".git":
            raise DontStopIteration('* ignored "{}"'.format(path))

    if ignore is not None:
        before_ignore = []
        other_ignore = []
        for rawIgnore in ignore:
            if rawIgnore.startswith("!"):
                before_ignore.append(rawIgnore)
            else:
                other_ignore.append(rawIgnore)
        ignore = before_ignore + other_ignore
        # ^ Inverse operations must happen *first* so that lookahead
        #   is done, otherwise a loose ignore may match first and
        #   result in an early return (which means ignore)!
        for rawIgnore in ignore:
            ignore_s = rawIgnore
            checkPath = path
            absolute = False
            verb = "ignored"
            if ignore_s.startswith("!"):
                verb = "kept"
                # For this to work, inverse strings must be processed
                # first!
                ignore_s = ignore_s[1:]
            if ignore_s.startswith("/"):
                absolute = True
                # ignore_s = [1:]
                # ^ keep "/" since checkPath will start with "/" after
                #   ignore_root is removed in the case of a match.
                checkPath = path
                if checkPath.startswith(ignore_root):
                    checkPath = checkPath[len(ignore_root):]
                    # ^ Now checkPath starts with "/" like ignore_s
            try:
                if ignore_s.endswith("/"):
                    ignore_s = ignore_s[:-1]
                    if absolute:
                        if (os.path.isdir(path)
                                and is_like(checkPath, ignore_s)):
                            msg = ("* {} {} due to {}".format(
                                verb,
                                path,
                                ig_path,
                            ))
                            if verb == "ignored":
                                raise DontStopIteration(msg)
                            else:
                                echo0(msg)
                                # If inverse and matches, keep it. Stop
                                # checking it against ignore strings.
                                break
                    else:
                        if (os.path.isdir(path) and is_like(sub, ignore_s)):
                            msg = ("* {} {} due to {}"
                                   "".format(verb, path, ig_path))
                            if verb == "ignored":
                                raise DontStopIteration(msg)
                            else:
                                echo0(msg)
                                # If inverse and matches, keep it. Stop
                                # checking it against ignore strings.
                                break
                else:
                    if absolute:
                        if (os.path.isfile(os.path.realpath(path))
                                and is_like(checkPath, ignore_s)):
                            msg = ("* {} {} due to {}"
                                   "".format(verb, path, ig_path))
                            if verb == "ignored":
                                raise DontStopIteration(msg)
                            else:
                                echo0(msg)
                                # If inverse and matches, keep it. Stop
                                # checking it against ignore strings.
                                break
                    else:
                        if (os.path.isfile(os.path.realpath(path))
                                and is_like(sub, ignore_s)):
                            # ^ ALWAYS use realpath since could be ""
                            msg = ("* {} {} due to {}"
                                   "".format(verb, path, ig_path))
                            if verb == "ignored":
                                raise DontStopIteration(msg)
                            else:
                                echo0(msg)
                                # If inverse and matches, keep it. Stop
                                # checking it against ignore strings.
                                break
            except ValueError as ex:
                igs = ignore_s
                rig = rawIgnore
                echo0(
                    'trace_ignore_files[{}] = {}  # effectively {}'
                    ''.format(json.dumps(rawIgnore),
                              json.dumps(trace_ignore_files.get(rig)),
                              json.dumps(igs))
                )
                raise ex
            if path != checkPath:
                echo2("- {} ({}) not {} by filter: {}"
                      "".format(checkPath, path, verb, ignore_s))
            else:
                echo2("- {} not {} by filter: {}"
                      "".format(path, verb, ignore_s))
    if os.path.isfile(os.path.realpath(path)):
        # ^ ALWAYS do realpath since could be ""
        # echo1('* checking "{}"'.format(path))
        if not is_like_any(sub, include):
            # ^ default is ["*"]
            raise DontStopIteration(
                "* {} {}".format(sub, TRIVIAL_EXCLUSION_INCLUDES)
            )
        else:
            yield path
            raise DontStopIteration(
                "{} {}".format(path, TRIVIAL_INCLUSION_IN_INCLUDES)
            )
        # ^ Either way, do not continue below if it is a file.
    else:
        yield path

    if (len(path) != 0) and (not os.path.isdir(path)):
        # ^ If not checking len 0, use os.path.abspath(path)
        #   to convert "" to a path.
        # Dangling symlink in this case probably, so return to avoid:
        # "FileNotFoundError: [Errno 2] No such file or directory: "
        # raise DontStopIteration(
        #     '* The directory "{}" could not be opened'.format(path)
        # )  # return
        pass
    # Even though tryIgnore occurs last, it will happen before any file
    # in the directory, since path that is dir is in the *same* depth
    # as the file at that depth and therefore such a .gitignore should
    # *not* affect any file at that level.
    tryIgnore = os.path.join(path, ".gitignore")
    if gitignore and os.path.isfile(tryIgnore):
        echo1('* reading "{}"'.format(tryIgnore))
        ignore = []
        trace_ignore_files = {}
        ignore_root = path
        with open(tryIgnore, 'r') as ins:
            for rawL in ins:
                line = rawL.strip()
                if len(line) < 1:
                    continue
                if line.startswith("#"):
                    continue
                ignore.append(line)
                trace_ignore_files[line] = tryIgnore
    listPath = path
    if listPath == "":
        listPath = "."
    subs = None
    try:
        subs = os.listdir(listPath)
    except FileNotFoundError as ex:
        msg = ('* missing or inaccessible: "{}" ({})'
               ''.format(listPath, ex))
        raise DontStopIteration(msg)
    except NotADirectoryError as ex:
        msg = ('* missing or inaccessible'
               ' (neither a file nor a directory): "{}" ({})'
               ''.format(listPath, ex))
        raise DontStopIteration(msg)
    # echo1("- searching {} sub(s) in {}"
    #       "".format(len(subs), json.dumps(path)))

    for sub in subs:
        # The parent path is guaranteed *not* to be a file by now.
        subPath = os.path.join(path, sub)
        if path == "":
            subPath = sub
        if recursive or not os.path.isdir(subPath):
            # echo2("  searching {}".format(subPath))
            # Always avoid recursive symlinks:
            if os.path.islink(subPath):
                target = os.readlink(subPath)
                if not follow_symlinks:
                    echo0("* follow_symlinks=False, skipping {} -> {}"
                          "".format(subPath, target))
                    continue
                # if os.path.abspath(target) != target:
                if not is_abs_path(target):
                    # The path must be constructed manually because:
                    '''
                    cd ~/Videos
                    cd without-intro
                    ln -s .. Videos
                    cd ..
                    python3
                    os.path.abspath(os.readlink("without-intro/Videos"))
                    # The result is ~ but should be Videos, so:
                    '''
                    targetPath = os.path.join(path, target)
                    targetPath = os.path.abspath(targetPath)
                    absPath = os.path.abspath(path)
                    if absPath == targetPath:
                        continue
                    targetPathSlash = targetPath
                    if not targetPathSlash.endswith(os.path.sep):
                        targetPathSlash += os.path.sep
                    if absPath.startswith(targetPathSlash):
                        echo0("* not following recursive (out-of-scope)"
                              " link {} -> {}"
                              "".format(subPath, targetPath))
                        # Don't go backwards to expand the search such
                        # as: "/opt/something" startswith "/opt/"
                        continue
                if target in followed_symlink_targets:
                    echo0("* already followed {} -> {}"
                          "".format(subPath, target))
                    continue
                followed_symlink_targets.append(target)
                echo2('* only following symlink to "{}" once'
                      ''.format(target))
            try:
                # Without `yield from`, the call never really happens
                # (since this is a generator)!
                yield from filter_tree(
                    subPath,
                    more_args=more_args,
                    include=include,
                    recursive=recursive,
                    quiet=quiet,
                    ignore=ignore,
                    ignore_root=ignore_root,
                    show_args_warnings=show_args_warnings,
                    trace_ignore_files=trace_ignore_files,
                    follow_symlinks=follow_symlinks,
                    followed_symlink_targets=followed_symlink_targets,
                    root=root,
                )
                # ^ filter the files too
                # ^ don't yield here, even if directory, since filtering
                #   must occur (yield path before this loop instead)
            except DontStopIteration as ex:
                if not contains_any(str(ex), TRIVIAL_EXCEPTION_FLAGS):
                    echo0("  "+str(ex))
                    # ^ Show the message explaining why the file or
                    #   directory was ignored, without interfering with
                    #   stdout.
                pass
        else:
            pass
            # echo2('  - skipping {} since isdir (recursive={})'
            #       ''.format(subPath, recursive))

    # Don't return: It is the Pythonic StopIteration and stops
    # recursion within a generator!

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
    include_args = default_includes.copy()
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
    # path = None
    paths = []

    for argI in range(1, len(sys.argv)):
        arg = sys.argv[argI]
        if arg == "--help":
            usage()
            return 0
        elif arg == "--include":
            pass
            # prev_var will be checked, so there is nothing to do yet.
        elif arg == "-r":
            echo0("* -r (recursive) is already the default.")
        elif arg == "-n":
            _n_arg = "-n"
        elif arg == "--no-ignore":
            gitignore = False
        elif arg == "--recursive":
            _recursive_arg = True
            # echo0("* -r (recursive) is already the default.")
        elif pattern is None:
            pattern = arg
        else:
            if os.path.isfile(arg):
                # _recursive_arg = False
                # echo0('* turning off recursive mode'
                #       ' (default in ggrep) since "{}" is a file'
                #       ''.format(arg))
                # ^ -r is never used anyway (ggrep is always recursive
                #   unless a file is detected in paths)
                paths.append(arg)
                '''
                if path is not None:
                    raise ValueError(
                        'Having more than one file parameter is not'
                        ' implemented. "{}" was already before "{}"'
                        ''.format(path, arg)
                    )
                path = arg
                '''
            elif arg == "--include-all":
                if _found_include:
                    raise ValueError(
                        "Error: '--include-all' isn't compatible with"
                        " '--include'."
                    )

                echo0("* removing the default '--include'"
                      " option so all are included.")
                include_args = None
                _found_include = True
                _include_all = True
            elif arg == "--verbose":
                set_verbosity(1)
            elif arg == "--debug":
                set_verbosity(2)
            elif prev_var == "--include":
                if _include_all:
                    raise ValueError(
                        "Error: '--include' isn't compatible with"
                        " '--include-all'."
                    )

                if not _found_include:
                    include_args = []

                _found_include = True
                # grep can accept more than one --include, so force the
                # old one and the new one:
                include_args.append("--include")
                include_args.append(arg)
            elif os.path.isdir(arg):  # elif path is None:
                paths.append(arg)
                '''
                if arg.startswith("-"):
                    if not os.path.exists(arg):
                        raise ValueError(
                            "{} is neither an implemented {} option"
                            " nor a file.".format(arg, me)
                        )
                path = arg
                '''
            elif not is_grep_arg(arg):
                echo0(GREP_DOC)
                raise ValueError(
                    ("{} is not a valid argument."
                     " See above (from `grep --help` of grep 3.6)"
                     " for arguments that ggrep will either"
                     " try to process like grep"
                     " or ignore and show a warning"
                     " if not implemented.".format(arg))
                )
            else:
                _more_args.append(arg)

        if arg == "-n":
            echo0("* -n is already the default (required for"
                  " the functionality of {}).".format(me))
            prev_var = ""
        else:
            prev_var = arg

    if len(paths) == 0:
        paths.append("")  # Use the current directory but don't show it.

    if prev_var == "--include":
        raise ValueError(
            "Error: You must specify a filename pattern after"
            " --include such as \"*.lua\""
            "(including quotes if using asterisk(s)!) ."
        )

    count = len(_more_args)
    echo0("* _more_args count: {}".format(count))
    if include_args is not None:
        includeCount = len(include_args)
        echo0("* include_args count: {}".format(includeCount))
    else:
        echo0("* include_args: {}".format(include_args))

    if _n_arg is None:
        _n_arg = "-n"
        # The line number (obtained via -n) is required for this script's
        # main purpose.

    if _recursive_arg is None:
        _recursive_arg = True

    echo0("* _more_args: {}".format(_more_args))
    echo0("* include_args: {}".format(include_args))
    _new_args = _more_args

    if not _found_include:
        echo0("  (using ggrep default types since not specified)")
    else:
        echo0("* _found_include: {}".format(_found_include))

    sys.stderr.write("grep")
    for value in _new_args:
        if " " in value:
            sys.stderr.write(' "{}"'.format(value))
        else:
            sys.stderr.write(" {}".format(value))
        sys.stderr.flush()
    num = 0
    total_count = 0
    for path in paths:
        num += 1
        echo0()
        echo0()
        if len(paths) > 1:
            echo0('results set {} of {} (looking for "{}" in "{}"):'
                  ''.format(num, len(paths), pattern, path))
        else:
            echo0('results (looking for "{}" in "{}"):'
                  ''.format(pattern, path))
        echo0()
        current_inc = include_args
        if os.path.isfile(path):
            current_inc = None
            # ^ don't filter an explicitly-set file!
        results = ggrep(pattern, path, more_args=_new_args,
                        include=current_inc, gitignore=gitignore)
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
            print("geany {} -l {}  # < {}"
                  "".format(quoted(_file), _line_n, line[colon2+1:]))

        echo0()
        echo0("({} match(es))".format(len(results)))
        total_count += len(results)

    if len(paths) > 0:
        echo0()
        echo0("({} match(es) total)".format(total_count))
    echo0()
    echo0("* to reduce output horizontally, hide line content via:")
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
    echo0(" | cut -f1 -d\\#")  # The actual command requires 1 backslash

    if not _include_all:
        echo0("* to show all file types"
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
        echo0(" --include-all")
        echo0("  # and add --no-ignore to search in"
              " .git directories and in files listed in"
              " .gitignore files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
