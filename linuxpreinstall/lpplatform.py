#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import os
import platform
import sys
import subprocess

import linuxpreinstall

from linuxpreinstall import (
    list_installed_parts,
    SCRIPT_DIRS,
)
from linuxpreinstall.lplogging import (  # noqa: E402
    echo0,
)
from linuxpreinstall.logging2 import (  # noqa: E402
    getLogger,
)

logger = getLogger(__name__)


# region from hierosoft and relicensed by author for linux-preinstall
def run_and_get_lists(cmd_parts, collect_stderr=True):
    '''Run a command and check the output.

    Args:
        collect_stderr (bool): Collect stderr output for the err return
            list Defaults to True.

    Returns:
        tuple[list[str], list[str], int]: (out, err, returncode) where
            out and err are each a list of 0 or more lines, and return
            code is the code returned by the process (0 if ok).
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
                    logger.warning(
                        "Removing a backspace from the"
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


WIN_EXECUTABLE_DOT_EXTS = [".exe", ".ps1", ".bat", ".com"]


def is_exe(path):
    """Check if the path exists and is executable.

    Returns:
        bool: Is an executable file.
    """
    # Jay, & Mar77i. (2017, November 10). Path-Test if executable exists in
    #     Python? [Answer]. Stack Overflow.
    #     https://stackoverflow.com/questions/377017/
    #     test-if-executable-exists-in-python
    return os.path.isfile(path) and os.access(path, os.X_OK)



def which_nearby_cmd(name, allow_py_on_win=False):
    """Return absolute path to command or None."""
    # 1. Standard lookup in PATH
    # if hasattr(shutil, 'which'):
    #     # Python 3.3 or higher
    #     path = shutil.which(name)
    #     if path:
    #         return os.path.abspath(path)
    # else:
    path = which(name)
    if path:
        return os.path.abspath(path)

    # 2. Exact extension lists and order as required
    if sys.platform.startswith("win"):
        if allow_py_on_win:
            extensions = tuple(WIN_EXECUTABLE_DOT_EXTS + [".py", ".pyw"])
        else:
            extensions = tuple(WIN_EXECUTABLE_DOT_EXTS)
    else:
        extensions = ("", ".sh", ".py")

    for ext in extensions:
        for script_dir in SCRIPT_DIRS:
            candidate = os.path.join(script_dir, name + ext)
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return os.path.abspath(candidate)

    return None


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
            logger.info(prefix+"looking in {}".format(path))
            try_path = os.path.join(path, filename)
            if is_exe(try_path):
                return try_path
            elif os.path.isfile(try_path):
                echo0(prefix+'Warning: "{}" exists'
                      ' but is not executable.'.format(try_path))
                fallback_path = try_path
            else:
                logger.info(prefix+"There is no {}".format(try_path))
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


def get_installed():
    assert linuxpreinstall.is_initialized()
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

