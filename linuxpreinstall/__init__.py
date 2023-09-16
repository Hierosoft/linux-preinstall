#!/usr/bin/env python3

from __future__ import print_function
import os
import sys
import subprocess
import platform
from csv import reader
import json

HOME = None
if platform.system() == "Windows":
    HOME = os.environ['USERPROFILE']
else:
    HOME = os.environ['HOME']

PROFILES, USER_DIR_NAME = os.path.split(HOME)
# ^ Also done by generate_exclude.py

# region hierosoft.morelogging relicensed by author for linux-preinstall

to_log_level = {
    3: 10,
    2: 20,
    1: 30,
    0: 40,
}

verbosity_levels = [False, True, 0, 1, 2, 3]

verbosity = 0
for argI in range(1, len(sys.argv)):
    arg = sys.argv[argI]
    if arg.startswith("--"):
        if arg == "--verbose":
            verbosity = 1
        elif arg == "--debug":
            verbosity = 2

def pformat(value, quote_if_like_str=True):
    """This is mostly like pformat from pprint except always on one line.

    Numbers are left as numbers even if quote_if_like_str is True, to
    avoid adding extra quotes. Use set pformat_preferred_quote to set
    the preferred quote.

    Args:
        value: any value that can convert to str. Values in
            an iterable will be processed resursively first.
        quote_if_like_str (Optional[bool]): Do not use this option, or
            your pformat calls will be incompatible with
            pprint.pformat--This option is only for recursion. Add
            quotes (not done recursively, since if iterable but not
            is_str_like, the last step which is converting from iterable
            to string adds quotes to all string values).

    Returns:
        str: string where only strings are quote_if_like_str (without
            leading b or u).
    """
    original_value = value
    enclosures = None
    if not is_str_like(value):
        # ^ unicode isn't normal in Python 3 so check typename not isinstance
        iterated = False
        try:
            parts = []
            enclosures = ("[", "]")
            if isinstance(enclosures, tuple):
                enclosures = ("(", ")")
            if hasattr(value, 'items'):
                if isinstance(value, OrderedDict):
                    parts = OrderedDict()
                else:
                    parts = {}
                for key, item in value.items():
                    parts[key] = pformat(item, quote_if_like_str=False)
                return parts
            for i, item in enumerate(value):
                iterated = True
                parts.append(pformat(item, quote_if_like_str=False))
                # Use append not '=' since tuple is not assignable
            if isinstance(value, tuple):
                value = tuple(parts)
            else:
                value = parts
        except TypeError:
            if iterated:
                raise
            # else it is not iterable, so do not try to fix elements
    if not quote_if_like_str:
        try:
            _ = len(value)
        except TypeError:
            # It is not str-like. To avoid adding quotes to non-str-like
            #   (number, bool, etc.) leave it as is
            #   (otherwise it will get quotes on list to str).
            return value
    value = str(value)
    # big_enclosures = ["OrderedDict(", ")"]
    if is_enclosed(value, "b'", "'") or is_enclosed(value, "u'", "'"):
        if quote_if_like_str:
            return value[1:]  # Only remove b or u not b'' etc.
        else:
            return value[2:-1]
    elif is_str_like(original_value):
        if quote_if_like_str:
            if pformat_preferred_quote is None:
                if '"' in value:
                    return "'%s'" % value.replace("'", "\\'")
                else:
                    return '"%s"' % value.replace('"', '\\"')
            else:
                # This is universal but isn't as nice since it will
                #   force escaped quotes. The case above is adaptive.
                quo = pformat_preferred_quote
                return '%s%s%s' % (quo, value.replace(quo, '\\'+quo), quo)
    # elif isinstance(value, OrderedDict)
    return value


def write0(arg):
    sys.stderr.write(arg)
    sys.stderr.flush()
    return True


def write1(arg):
    if verbosity < 1:
        return False
    sys.stderr.write(arg)
    sys.stderr.flush()
    return True


def write2(arg):
    if verbosity < 2:
        return False
    sys.stderr.write(arg)
    sys.stderr.flush()
    return True


def write3(arg):
    if verbosity < 3:
        return False
    sys.stderr.write(arg)
    sys.stderr.flush()
    return True


def echo0(*args, **kwargs):  # formerly prerr
    print(*args, file=sys.stderr, **kwargs)
    return True


def echo1(*args, **kwargs):  # formerly debug
    if verbosity < 1:
        return False
    print(*args, file=sys.stderr, **kwargs)
    return True


def echo2(*args, **kwargs):  # formerly extra
    if verbosity < 2:
        return False
    print(*args, file=sys.stderr, **kwargs)
    return True


def echo3(*args, **kwargs):
    if verbosity < 3:
        return False
    print(*args, file=sys.stderr, **kwargs)
    return True


def get_verbosity():
    return verbosity


def set_verbosity(verbosity_level):
    global verbosity
    if verbosity_level not in verbosity_levels:
        vMsg = verbosity_levels
        if isinstance(vMsg, str):
            vMsg = '"{}"'.format(vMsg)
        raise ValueError(
            "verbosity_levels must be one of {} not {}."
            "".format(verbosity_levels, vMsg)
        )
    verbosity = verbosity_level

# endregion hierosoft.morelogging relicensed by author for linux-preinstall

# region from hierosoft and relicensed by author for linux-preinstall

def run_and_get_lists(cmd_parts, collect_stderr=True):
    '''
    Returns:
    a tuple of (out, err, returncode) where out and err are each a list
    of 0 or more lines.
    '''
    # See <https://stackabuse.com/executing-shell-commands-with-python>:
    # called = subprocess.run(list_installed_parts,
    #                         stdout=subprocess.PIPE, text=True)
    # , input="Hello from the other side"
    # echo0(called.stdout)
    outs = []
    errs = []
    # See <https://stackoverflow.com/a/7468726/4541104>
    # "This approach is preferable to the accepted answer as it allows
    # one to read through the output as the sub process produces it."
    # -Hoons Jul 21 '16 at 23:19
    if collect_stderr:
        sp = subprocess.Popen(cmd_parts, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    else:
        sp = subprocess.Popen(cmd_parts, stdout=subprocess.PIPE)

    if sp.stdout is not None:
        for rawL in sp.stdout:
            line = rawL.decode()
            # TODO: is .decode('UTF-8') ever necessary?
            outs.append(line.rstrip("\n\r"))
    if sp.stderr is not None:
        for rawL in sp.stderr:
            line = rawL.decode()
            while True:
                bI = line.find("\b")
                if bI < 0:
                    break
                elif bI == 0:
                    print("WARNING: Removing a backspace from the"
                          " start of \"{}\".".format(line))
                line = line[:bI-1] + line[bI+1:]
                # -1 to execute the backspace not just remove it
            errs.append(line.rstrip("\n\r"))
    # MUST finish to get returncode
    # (See <https://stackoverflow.com/a/16770371>):
    more_out, more_err = sp.communicate()
    if len(more_out.strip()) > 0:
        echo0("[run_and_get_lists] got extra stdout: {}".format(more_out))
    if len(more_err.strip()) > 0:
        echo0("[run_and_get_lists] got extra stderr: {}".format(more_err))

    # See <https://stackoverflow.com/a/7468725/4541104>:
    # out, err = subprocess.Popen(
    #     ['ls','-l'],
    #     stdout=subprocess.PIPE,
    # ).communicate()

    # out, err = sp.communicate()
    # (See <https://stackoverflow.com/questions/10683184/
    # piping-popen-stderr-and-stdout/10683323>)
    # if out is not None:
    #     for rawL in out.splitlines():
    #         line = rawL.decode()
    #         outs.append(line.rstrip("\n\r"))
    # if err is not None:
    #     for rawL in err.splitlines():
    #         line = rawL.decode()
    #         errs.append(line.rstrip("\n\r"))

    return outs, errs, sp.returncode

def is_exe(path):
    # Jay, & Mar77i. (2017, November 10). Path-Test if executable exists in
    #     Python? [Answer]. Stack Overflow.
    #     https://stackoverflow.com/questions/377017/
    #     test-if-executable-exists-in-python
    return os.path.isfile(path) and os.access(path, os.X_OK)


WIN_EXECUTABLE_DOT_EXTS = [".exe", ".ps1", ".bat", ".com"]


def which(program_name, more_paths=[]):
    '''Get the full path to a given executable.

    If a full path is provided,
    return it if executable. Otherwise, if there isn't an executable one
    the PATH, return None, or return one that exists but isn't
    executable (using program_name as the preferred path if it is a full
    path even if not executable).

    Args:
        program_name (str): This can leave off the potential file extensions
            and on Windows each known file extension will be checked (for the
            complete list that will be checked, see the
            WIN_EXECUTABLE_DOT_EXTS constant in the module's
            __init__.py.
        more_paths (Iterable[str]): Paths other than those in system PATH
            that should also be checked.

    Returns:
        str: The full path to the executable or None.
    '''
    # from https://github.com/poikilos/DigitalMusicMC
    prefix = "[which] "
    preferred_path = None
    filenames = [program_name]
    if platform.system() == "Windows":
        if os.path.splitext(program_name)[1] == "":
            for dot_ext in WIN_EXECUTABLE_DOT_EXTS:
                filenames.append(program_name+dot_ext)
    for filename in filenames:
        if os.path.split(filename)[0] and is_exe(filename):
            return filename
        elif os.path.isfile(filename):
            preferred_path = filename

        paths_str = os.environ.get('PATH')
        if paths_str is None:
            echo0("Warning: There is no PATH variable, so returning {}"
                  "".format(filename))
            return filename

        paths = paths_str.split(os.path.pathsep)
        fallback_path = None
        for path in (paths + more_paths):
            echo1(prefix+"looking in {}".format(path))
            try_path = os.path.join(path, filename)
            if is_exe(try_path):
                return try_path
            elif os.path.isfile(try_path):
                echo0(prefix+'Warning: "{}" exists'
                      ' but is not executable.'.format(try_path))
                fallback_path = try_path
            else:
                echo1(prefix+"There is no {}".format(try_path))
        result = None
        if preferred_path is not None:
            echo0(prefix+'Warning: "{}" will be returned'
                  ' since given as filename="{}" but is not executable.'
                  ''.format(preferred_path, filename))
            result = fallback_path
        elif fallback_path is not None:
            echo0(prefix+'Warning: "{}" will be returned'
                  ' but is not executable.'.format(fallback_path))
            result = fallback_path
    return result


# endregion from hierosoft and relicensed by author for linux-preinstall



# region hierosoft.ggrep relicensed by author for linux-preinstall


def _wild_increment(haystack_c, needle_c):
    if needle_c == "*":
        return 0
    if needle_c == "?":
        return 1
    if needle_c == haystack_c:
        return 1
    return -1


def contains(haystack, needle, allow_blank=False, quiet=False):
    '''Check if the substring "needle" is in haystack.

    The behavior differs from the Python "in" command according to the
    arguments described below.

    Args:
        haystack (str): a string to look in
        needle (str): a string for which to look
        allow_blank (bool): Instead of raising an exception on a blank
            needle, return False and show a warning (unless quiet).
        quiet (bool): Do not report errors to stderr.

    Raises:
        ValueError: If allow_blank is not True, a blank needle will
            raise a ValueError, otherwise there will simply be a False
            return.
        TypeError: If no other error occurs, the "in" command will raise
            "TypeError: argument of type 'NoneType' is not iterable" if
            haystack is None (or haystack and needle are None), or
            "TypeError: 'in <string>' requires string as left operand,
            not NoneType" it needle is None.
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


def is_like(haystack, needle, allow_blank=False, quiet=False,
            haystack_start=None, needle_start=None, indent=2):
    '''Compare to needle using wildcard notation not regex.

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

# endregion hierosoft.ggrep relicensed by author for linux-preinstall


def endsWithAny(haystack, needles, CS=True):
    '''
    Haystack ends with any of the needles.

    Keyword arguments:
    CS -- Do case-sensitive comparison.
    '''
    if not CS:
        haystack = haystack.lower()
        for rawN in needles:
            needle = rawN.lower()
            if haystack.endswith(needle):
                return True
        return False
    for needle in needles:
        if haystack.endswith(needle):
            return True
    return False


profile = None
AppData = None
LocalAppData = None
myAppData = None

if platform.system() == "Windows":
    profile = os.environ['USERPROFILE']
    AppData = os.environ['APPDATA']
    LocalAppData = os.environ['LOCALAPPDATA']
    myAppData = os.path.join(AppData, "CodeBlocks")
else:
    profile = os.environ['HOME']
    if platform.system() == "Darwin":
        Library = os.path.join(profile, "Library")
        AppData = os.path.join(Library, "Application Support")
        LocalAppData = os.path.join(Library, "Application Support")
        # myAppData = os.path.join(LocalAppData, "codeblocks")
        # cbConf = os.path.join(myAppData, "default.conf")
    else:
        AppData = os.path.join(profile, ".config")
        LocalAppData = os.path.join(profile, ".config")
    myAppData = os.path.join(AppData, "codeblocks")


digits = "1234567890"  # or use s.isdigit()
digit_or_dot = digits + "."

osrelease = None
data_path = os.path.dirname(__file__)

packages_name = "package_names.csv"
alt_names = {}  # Initialized in _init_packagenames, used in add_pkg
# ^ Nested: use alt_names['Debian']['10'] occurs if there is a space
#   in the column header, otherwise it is alt_names['Debian']['10']

refresh_parts = None
install_parts = None
# uninstall_parts = None  # See remove_parts
remove_parts = None
list_installed_parts = None
pkg_search_parts = None
upgrade_parts = None
package_type = None
install_bin = None
packageInfos = None




def set_verbosity(v):
    global verbosity
    # NOTE: True in [0, 1] is also True!
    verbosity_levels = [True, False, 0, 1, 2]
    if v in verbosity_levels:
        verbosity = v
    else:
        raise ValueError("Verbose must be any of {} but the value was"
                         " {}.".format(verbosity_levels, v))


class InstallManager:
    def __init__(self, os_name, desired_os_version):
        '''
        The os_name and version will be combined if possible, otherwise
        the column in package_names.csv with the highest version will be
        used.

        Sequential arguments:
        os_name -- such as "Debian"
        desired_os_version -- such as "10"
        '''
        self._ported_packages = []
        self._os_name = os_name
        self._desired_version = desired_os_version

    def get_the_dev_group_name():
        # TODO: dnf grouplist | grep Development | grep -v "D Development"
        raise NotImplementedError("")

    def port_package_id(self, package_id):
        '''
        Translate the package id to the one for the desired os_name
        using "package_names.csv".

        Append install instructions using files such as
        linux-preinstall/meta/post_install_instructions/
        by_fedora_packagename/geany-plugin-spellcheck.txt

        Returns
        a tuple of name and type, such as
        ("org.codeblocks.codeblocks", "flatpak")
        '''

        raise NotImplementedError("port_package_id")

    def install_ported_package(self, package_id):
        # If found in the flatpak column, use flatpak such as:
        # flatpak install -y flathub org.codeblocks.codeblocks
        raise NotImplementedError("install_ported_package")


def _init_commands():
    echo1("* _init_commands...")
    global refresh_parts
    global install_parts
    # global uninstall_parts  # See remove_parts
    global remove_parts
    global list_installed_parts
    global pkg_search_parts
    global upgrade_parts
    global package_type
    global install_bin

    if bin_exists("dnf"):
        package_type = "rpm"
        install_bin = "dnf"
    elif bin_exists("yum"):
        package_type = "rpm"
        install_bin = "yum"
    elif bin_exists("apt"):
        package_type = "deb"
        install_bin = "apt"
    elif bin_exists("apt-get"):
        package_type = "deb"
        install_bin = "apt-get"
    elif bin_exists("pacman"):
        package_type = "pkg"
        install_bin = "pacman"
        install_parts = [install_bin, "-Syyu", "--noconfirm"]
        remove_parts = [install_bin, "-R", "--noconfirm"]
        upgrade_parts = [install_bin, "-Syyu", "--noconfirm"]
        # REFRESH_CMD = [install_bin, "-Scc"]
        # refresh_parts = [("#nothing do refresh since using pacman "
        #                   "(pacman -Scc clears cache but that's"
        #                   " rather brutal)...  # ")]
        list_installed_parts = [install_bin, "-Q"]
        # ^ Qe lists packages explicitly installed (see pacman -Q --help)
        pkg_search_parts = [install_bin, "-Ss"]
        echo0("WARNING: GTK3_DEV_PKG is unknown for pacman")

    if package_type == "deb":
        install_parts = [install_bin, "install", "-y"]
        remove_parts = [install_bin, "remove", "-y"]
        upgrade_parts = [install_bin, "upgrade"]
        refresh_parts = [install_bin, "update"]
        list_installed_parts = [install_bin, "list", "--installed"]
        pkg_search_parts = [install_bin, "search"]
    elif package_type == "rpm":
        install_parts = [install_bin, "install", "-y"]

    # if bin_exists("apt"):
    #     refresh_result = subprocess.run(["apt", "refresh"])
    # elif bin_exists("apt-get"):
    #     refresh_result = subprocess.run(["apt-get", "refresh"])
    if refresh_parts is not None:
        if os.geteuid() == 0:
            # refresh_result = subprocess.run(refresh_parts,
            #                                 stdout=sys.stderr.buffer)
            # returncode = refresh_result.returncode
            # "run" returns an object but "call" only returns the code:
            # returncode = subprocess.call(refresh_parts,
            #                              stdout=sys.stderr.buffer)
            returncode = subprocess.call(refresh_parts,
                                         stdout=sys.stderr.fileno())
            # ^ fileno() is Python 2 compatible
            #   https://stackoverflow.com/a/11495784/4541104
            #   (redirect stderr so stdout isn't flooded such as when
            #   using the sortversion command (which uses main from
            #   linuxpreinstall.versioning).
            result_msg = ("FAILED ({} didn't succeed with your privileges)"
                          "".format(refresh_parts))
            if returncode == 0:
                result_msg = "OK"
            echo1("* refreshing package list..." + result_msg)
        else:
            echo1("* linuxpreinstall is not refreshing the package list"
                  " since you are not a superuser.")
    echo1("  * done _init_commands")


def get_installed():
    out = None
    if list_installed_parts is not None:
        out, err, code = run_and_get_lists(list_installed_parts)
        msg_prefix = "[linuxpreinstall] Warning"
        if code != 0:
            msg_prefix = "[linuxpreinstall] Error"
        if len(err) > 0:
            echo0("{} (code {}) running {}:"
                  "".format(msg_prefix, code, " ".join(list_installed_parts)))
            for line in err:
                echo0(line)
        elif code != 0:
            echo0("Error code {}".format(code))
        if code != 0:
            return None
    return out


def find_not_decimal(s, start=None, step=1):
    if s is None:
        raise ValueError("s is None.")
    if len(s) == 0:
        raise ValueError("s is blank.")
    if step not in [-1, 1]:
        raise ValueError("step must be 1 or -1 (rfind_not_decimal)")
    if not isinstance(s, str):
        raise ValueError("s must be a str but is {}".format(s))
    if start is None:
        if step < 0:
            start = -1
        else:
            start = 0
    if start < 0:
        start = len(s) + start  # + since negative
    if step < 0:
        i = start + 1  # +1 since decremented before use
    else:
        i = start - 1  # -1 since incremented before use
    while True:
        i += step
        if step < 0:
            if i < 0:
                break
        else:
            if i >= len(s):
                break
        if s[i] not in digit_or_dot:
            return i
    return -1


def rfind_not_decimal(s, start=None):
    return find_not_decimal(s, start=start, step=-1)


def is_decimal(s):
    if len(s) == 0:
        raise ValueError("s is blank.")
    return rfind_not_decimal(s) < 0


def split_package_parts(s):
    '''
    Split a GNU/Linux-style package name into parts such as

    '''
    parts = s.split("-")

    if parts[:2] == ['libapache2', 'mod']:
        # versionize using the number after libapache2-mod-php
        parts = ['-'.join(parts)]
        # echo0("parts: {}".format(parts))

    name_last_index = rfind_not_decimal(parts[0], -1)
    group_prefixes = ['python', 'php', 'apt', 'ruby']

    if name_last_index < len(parts[0])-1:
        # If the first '-' is preceded by a number, split it further.
        version_i = name_last_index + 1
        new_part0 = parts[0][:version_i]  # The name
        new_part1 = parts[0][version_i:]  # The version
        # if new_part0 in group_prefixes:
        if len(parts[1:]) > 0:
            parts = [new_part0, new_part1, '-'.join(parts[1:])]
            # ^ such as ["php", "8.0", "fpm"]
        else:
            parts = [new_part0, new_part1]
            # ^ such as ["php", "8.0"]
        # else:
        #     parts = [new_part0, new_part1] + parts[1:]
        #     such as ["php", "symphony", "service", "contracts"]
    else:
        if parts[0] in group_prefixes:
            if len(parts) > 1:
                parts = [parts[0], "-".join(parts[1:])]
                # such as:
                #   ["php", "symphony-service-contracts"] or
                #   ["apt", "btrfs-snapshot"]
            # else something like: "php"
        else:
            parts = [s]
            # such as [""] (nothing to split)
    return parts


def find_unquoted(haystack, needle, quotes=['"']):
    in_quote = None
    for i in range(len(haystack)):
        char = haystack[i]
        at_quote = None
        for iq in range(len(quotes)):
            if char == quotes[iq]:
                at_quote = quotes[iq]
                break
        if in_quote is None:
            # not in a quote
            if at_quote is not None:
                # Start a quote.
                in_quote = at_quote
            elif haystack[i:i+len(needle)] == needle:
                # char is not a quote, and the needle is here.
                return i
        elif at_quote is not None:
            # in a quote, but this char is a quote, so
            # end the quote.
            in_quote = None
    return -1


def _init_osrelease():
    echo1("* _init_osrelease...")
    global osrelease
    if osrelease is None:
        osrelease = {}
    osrelease_path = os.path.join("/etc", "os-release")
    # other release files and formats:
    # /etc/centos-release: CentOS Linux release 8.4.2105
    # /etc/debian_version: 11.1
    # /etc/devuan_version: chimaera
    # ^ devuan also has /etc/debian_version
    if os.path.isfile(osrelease_path):
        osrelease = {}
        lineN = 0
        with open(osrelease_path) as ins:
            for rawL in ins:
                lineN += 1
                line = rawL.strip()
                comI = find_unquoted(line, "#")
                if comI > -1:
                    line = line[:comI].strip()
                parts = line.split("=")
                if len(parts) == 2:
                    key = parts[0]
                    v = parts[1]
                    if len(v) >= 2:
                        if (v[0] == '"') and (v[-1] == '"'):
                            v = v[1:-1]
                    osrelease[key] = v
                else:
                    signRawI = rawL.find_unquoted("=")
                    raise SyntaxError("{}:{}:{}: misplaced '='"
                                      "".format(osrelease_path, lineN,
                                                signRawI))
    else:
        echo0("osrelease_path \"{}\" was not found. osrelease:{}"
              "".format(osrelease_path, osrelease))
    echo1("  * done _init_osrelease")


def bin_exists(name):
    paths = os.environ['PATH'].split(os.pathsep)
    for root in paths:
        if os.path.isfile(os.path.join(root, name)):
            return True
    return False


def _init_packagenames():
    echo1("* _init_packagenames...")
    global packageInfos
    if packageInfos is None:
        packageInfos = {}
    listPath = os.path.join(data_path, packages_name)
    if not os.path.isfile(listPath):
        raise FileNotFoundError(listPath)
    # raise NotImplementedError("_init_packagenames")
    rowNum = 0
    with open(listPath, 'r') as read_obj:
        rowNum += 1  # Start counting at 1.
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        if header is not None:
            for row in csv_reader:
                rowNum += 1  # Start after header row, at 2.
                pkgid = None
                o = {}
                for i in range(len(header)):
                    fieldName = header[i]
                    if fieldName == "id":
                        pkgid = row[i].strip()
                        o[fieldName] = pkgid
                        if len(pkgid) < 1:
                            echo0("{}:{}: Error: id is blank"
                                  "".format(listPath, rowNum))
                            continue
                    else:
                        if pkgid is None:
                            raise ValueError("The id column must be"
                                             "first in {}"
                                             "".format(listPath))
                        if o.get('names') is None:
                            o['names'] = {}
                        o['names'][fieldName] = row[i]
                if packageInfos.get(pkgid) is None:
                    packageInfos[pkgid] = o
                else:
                    for k, v in o.items():
                        packageInfos[pkgid][k] = v
                echo1("object[{}]: {}".format(pkgid, o))
    echo1("  * done _init_packagenames")


_init_osrelease()
_init_packagenames()
_init_commands()
