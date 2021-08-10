#!/usr/bin/env python3

import os
import sys
import subprocess

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


def error(msg):
    sys.stderr.write("{}\n".format(msg))

def _init_commands():
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
        error("WARNING: GTK3_DEV_PKG is unknown for pacman")

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
        refresh_result = subprocess.run(refresh_parts)
        result_msg = "FAILED"
        if refresh_result.returncode == 0:
            result_msg = "OK"
        error("* refreshing package list..." + result_msg)


def run_and_get_lists(cmd_parts, collect_stderr=True):
    '''
    Returns:
    a tuple of (out, err) where each is a list of 0 or more lines.
    '''
    # See <https://stackabuse.com/executing-shell-commands-with-python>:
    # called = subprocess.run(list_installed_parts, stdout=subprocess.PIPE, text=True)
    # , input="Hello from the other side"
    # error(called.stdout)
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
            error("Error running {}:"
                  "".format(" ".join(list_installed_parts)))
            for line in err:
                error(line)
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
    global osrelease
    if osrelease is None:
        osrelease = {}
    osrelease_path = os.path.join("/etc", "os-release")
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
        error("osrelease_path \"{}\" was not found. osrelease:{}"
              "".format(osrelease_path, osrelease))


def bin_exists(name):
    paths = os.environ['PATH'].split(os.pathsep)
    for root in paths:
        if os.path.isfile(os.path.join(root, name)):
            return True
    return False


def _init_packagenames():
    listPath = os.path.join(data_path, packages_name)
    if not os.path.isfile(listPath):
        raise FileNotFoundError(listPath)
    raise NotImplementedError("_init_packagenames")


_init_osrelease()
_init_packagenames()
_init_commands()
