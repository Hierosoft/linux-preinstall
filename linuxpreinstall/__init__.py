#!/usr/bin/env python3

from __future__ import print_function
import os
import sys
import subprocess
import platform
from csv import reader

verbose = False
def is_verbose():
    return verbose


def prerr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def debug(*args, **kwargs):
    if not verbose:
        return
    print(*args, file=sys.stderr, **kwargs)

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


# from https://github.com/poikilos/DigitalMusicMC
# and https://github.com/poikilos/blnk
def which(cmd):
    paths_str = os.environ.get('PATH')
    if paths_str is None:
        debug("Warning: There is no PATH variable, so returning {}"
              "".format(cmd))
        return cmd
    paths = paths_str.split(os.path.pathsep)
    for path in paths:
        debug("looking in {}".format(path))
        tryPath = os.path.join(path, cmd)
        if os.path.isfile(tryPath):
            return tryPath
        else:
            debug("There is no {}".format(tryPath))
    return None


osrelease = None
data_path = os.path.dirname(__file__)

packages_name = "package_names.csv"
alt_names = {}  # Initialized in _init_packagenames, used in add_pkg
# ^ Nested: use alt_names['Debian']['10'] occurs if there is a space
#   in the column header, otherwise it is alt_names['Debian']['10']

refresh_parts = None
install_parts = None
uninstall_parts = None
remove_parts = None
list_installed_parts = None
pkg_search_parts = None
upgrade_parts = None
package_type = None
install_bin = None
packageInfos = None


def set_verbose(v):
    global verbose
    if v is True:
        verbose = True
    elif v is False:
        verbose = False
    else:
        raise ValueError("Verbose must be True or False but {} was"
                         " tried".format(v))




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
    if verbose:
        prerr("* _init_commands...")
    global refresh_parts
    global install_parts
    global uninstall_parts
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
        #REFRESH_CMD = [install_bin, "-Scc"]
        # refresh_parts = ["#nothing do refresh since using pacman (pacman -Scc clears cache but that's rather brutal)...  # "]
        list_installed_parts = [install_bin, "-Q"]  # Qe lists packages explicitly installed (see pacman -Q --help)
        pkg_search_parts = [install_bin, "-Ss"]
        prerr("WARNING: GTK3_DEV_PKG is unknown for pacman")

    if package_type == "deb":
        install_parts = [install_bin, "install", "-y"]
        remove_parts = [install_bin, "remove", "-y"]
        upgrade_parts = [install_bin, "upgrade"]
        refresh_parts = [install_bin, "update"]
        list_installed_parts = [install_bin, "list", "--installed"]
        pkg_search_parts = [install_bin, "search"]
    elif package_type == "rpm":
        install_parts = [install_bin, "install", "-y"]

    #if bin_exists("apt"):
    #    refresh_result = subprocess.run(["apt", "refresh"])
    #elif bin_exists("apt-get"):
    #    refresh_result = subprocess.run(["apt-get", "refresh"])
    if refresh_parts is not None:
        if os.geteuid() == 0:
            # refresh_result = subprocess.run(refresh_parts, stdout=sys.stderr.buffer)
            # returncode = refresh_result.returncode
            # "run" returns an object but "call" only returns the code:
            # returncode = subprocess.call(refresh_parts, stdout=sys.stderr.buffer)
            returncode = subprocess.call(refresh_parts, stdout=sys.stderr.fileno())
            # ^ fileno() is Python 2 compatible
            #   https://stackoverflow.com/a/11495784/4541104
            #   (redirect stderr so stdout isn't flooded such as when
            #   using the sortversion command (which uses main from
            #   linuxpreinstall.versioning).
            result_msg = "FAILED ({} didn't succeed with your privileges)".format(refresh_parts)
            if returncode == 0:
                result_msg = "OK"
            prerr("* refreshing package list..." + result_msg)
        else:
            prerr("* linuxpreinstall is not refreshing the package list since you are not a superuser.")
    if verbose:
        prerr("  * done _init_commands")


def run_and_get_lists(cmd_parts, collect_stderr=True):
    '''
    Returns:
    a tuple of (out, err) where each is a list of 0 or more lines.
    '''
    # See <https://stackabuse.com/executing-shell-commands-with-python>:
    # called = subprocess.run(list_installed_parts, stdout=subprocess.PIPE, text=True)
    # , input="Hello from the other side"
    # prerr(called.stdout)
    outs = []
    errs = []
    # See <https://stackoverflow.com/a/7468726/4541104>
    # "This approach is preferable to the accepted answer as it allows
    # one to read through the output as the sub process produces it."
    # –Hoons Jul 21 '16 at 23:19
    if collect_stderr:
        sp = subprocess.Popen(cmd_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
    # See <https://stackoverflow.com/a/7468725/4541104>:
    # out, err = subprocess.Popen(['ls','-l'], stdout=subprocess.PIPE).communicate()

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

    return outs, errs


def get_installed():
    out = None

    if list_installed_parts is not None:
        out, err = run_and_get_lists(list_installed_parts)
        if len(err) > 0:
            prerr("Error running {}:"
                  "".format(" ".join(list_installed_parts)))
            for line in err:
                prerr(line)
            return None
    return out


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
    if verbose:
        prerr("* _init_osrelease...")
    global osrelease
    if osrelease is None:
        osrelease = {}
    osrelease_path = os.path.join("/etc", "os-release")
    # other release files and formats:
    # /etc/centos-release: CentOS Linux release 8.4.2105
    # /etc/debian_version: 11.1
    # /etc/devuan_version: chimera
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
        prerr("osrelease_path \"{}\" was not found. osrelease:{}"
              "".format(osrelease_path, osrelease))
    if verbose:
        prerr("  * done _init_osrelease")


def bin_exists(name):
    paths = os.environ['PATH'].split(os.pathsep)
    for root in paths:
        if os.path.isfile(os.path.join(root, name)):
            return True
    return False


def _init_packagenames():
    if verbose:
        prerr("* _init_packagenames...")
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
                            prerr("{}:{}: Error: id is blank"
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
                if verbose:
                    prerr("object[{}]: {}".format(pkgid, o))
    if verbose:
        prerr("  * done _init_packagenames")


_init_osrelease()
_init_packagenames()
_init_commands()
