#!/usr/bin/env python
from __future__ import print_function
import sys
import os
# import pprint
import shlex
import subprocess
import json
from linuxpreinstall import (
    echo0,
    echo1,
    echo2,
    set_verbose,
    profile,
)

from linuxpreinstall.bash import (
    get_bash_value,
)

me = os.path.basename(__file__)

ui_env_path = os.path.join(profile, ".profile")
sh_env_path = os.path.join(profile, ".bash_profile")
'''
^ "Use .bash_profile to run commands that should run only once, such as
  customizing the $PATH environment variable."
  -<https://linuxize.com/post/bashrc-vs-bash-profile/>
'''
sh_rc_path = os.path.join(profile, ".bashrc")
'''
^ "Put the commands that should run every time you launch a new shell in
  the .bashrc file. This include your aliases and functions , custom
  prompts, history customizations , and so on."
  -<https://linuxize.com/post/bashrc-vs-bash-profile/>
'''

chm_lines = [
    'HISTCONTROL=ignoredups:erasedups',  #
    'shopt -s histappend',
    ('PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND$\'\\n\'}'
     'history -a; history -c; history -r"'),
]
# ^ as per the websites cited in cmd_history_multisession_sh below.
# chm is short for: command history multi-session.
# TODO: (?) (from first website):
# - export HISTFILESIZE=10000

cmd_history_multisession_sh = '''
# region added by linux-preinstall
# As per <https://www.shellhacks.com/tune-command-line-history-bash/>,
#   append instead of overwrite history:
{}
# For multiple sessions as per
#   <https://unix.stackexchange.com/a/1292/343286>:
#   answered Aug 26, 2010 at 14:37 by Pablo R.
#   edited Jun 13, 2020 at 8:39 by Vlastimil Burián
{}
{}
# region added by linux-preinstall
'''.format(chm_lines[0], chm_lines[1], chm_lines[2])

old_set_line = "PROMPT_COMMAND='history -a'"
old_add_line = "PROMPT_COMMAND='$PROMPT_COMMAND; history -a'"
old_cmd_history_multisession_sh = '''
# As per <https://www.shellhacks.com/tune-command-line-history-bash/>,
#   save history immediately (instead of only on proper exit):
if [ -z "$PROMPT_COMMAND" ]; then
    {}
else
    {}
fi
'''.format(old_set_line, old_add_line)

echo0()
echo0("This file will setup the linux-preinstall shell backend.")



def get_conf_value(path, name):
    opener = "{}=".format(name)
    with open(path, 'r') as ins:
        lineN = 0
        for rawL in ins:
            lineN += 1
            line = rawL.strip()
            if line.startswith("#"):
                continue
            if line.startswith(opener):
                v = line[len(opener):]
                if ((v.startswith("'") and v.endswith("'"))
                        or (v.startswith('"') and v.endswith('"'))):
                    return v[1:-1]
                return v


def get_line(path, needle, comment_mark="#", indent="  "):
    '''
    Keyword arguments:
    comment_mark -- Ignore any line that starts with this (whitespace
        is excluded).
    '''
    if not os.path.isfile(path):
        return None
    with open(path, 'r') as ins:
        for rawL in ins:
            line = rawL.rstrip("\r\n")
            if comment_mark is not None:
                if line.strip().startswith(comment_mark):
                    continue
            if needle in line:
                return line
            else:
                echo2(indent+"- {} is not in {}".format(needle, line))
    return None


def get_line_startswith(path, needle, strip_line=True):
    if not os.path.isfile(path):
        return None
    with open(path, 'r') as ins:
        for rawL in ins:
            line = rawL.rstrip("\r\n")
            if strip_line:
                line = line.strip()
            if line.startswith(needle):
                return line
    return None


def appendFileLine(path, line):
    mode = 'a'
    if not os.path.isfile(path):
        mode = 'w'
        echo2("  - creating {} since doesn't exist for append"
              "".format(json.dumps(path)))
    with open(path, mode) as outs:
        outs.write(line + "\n")


myConfDir = os.path.join(profile, ".config", "linux-preinstall")
if not os.path.isdir(myConfDir):
    os.makedirs(myConfDir)

globalsPath = os.path.join(myConfDir, "globals.rc")

def appendConfLine(line):
    appendFileLine(globalsPath, line)


def main():
    enable_server = False
    enable_dev = False
    for argI in range(1, len(sys.argv)):
        arg = sys.argv[argI]
        if arg.startswith("--"):
            if arg == "--verbose":
                set_verbose(1)
            elif arg == "--debug":
                set_verbose(2)
            elif arg == "--server":
                enable_server = True
            elif arg == "--developer":
                enable_dev = True
            else:
                raise ValueError("The argument is incorrect: {}"
                                 "".format(arg))
    LINUX_PREINSTALL = os.path.dirname(os.path.realpath(__file__))
    lp_path = LINUX_PREINSTALL
    utilities = os.path.join(lp_path, "utilities")
    utilities = utilities.replace(profile, "$HOME")
    utilities_dev = os.path.join(lp_path, "utilities-developer")
    utilities_dev = utilities_dev.replace(profile, "$HOME")
    utilities_server = os.path.join(lp_path, "utilities-server")
    utilities_server = utilities_server.replace(profile, "$HOME")
    rcName = "api.rc"
    rcPath = os.path.join(LINUX_PREINSTALL, rcName)
    goodFlagPath = rcPath
    if not os.path.isfile(rcPath):
        raise RuntimeError(
            "You must run install-shell-backend from the"
            " linux-preinstall repo directory containing api.rc"
            " (tried in {})".format(rcPath)
        )

    indent = ""
    confLine = 'LINUX_PREINSTALL="{}"'.format(LINUX_PREINSTALL)
    if not os.path.isfile(globalsPath):
        appendConfLine(confLine)
        echo0('* wrote "{}"'.format(globalsPath))
    else:
        echo0('* checking "{}"'.format(globalsPath))
        old_lp = get_bash_value(globalsPath, 'LINUX_PREINSTALL')
        echo2("* old LINUX_PREINSTALL={}".format(old_lp))

        gotLine = get_line_startswith(globalsPath, "LINUX_PREINSTALL=")
        if gotLine is None:
            appendConfLine(confLine)
            echo0('* added LINUX_PREINSTALL to "{}"'
                  ''.format(globalsPath))
            # elif not os.path.isfile(globalsPath):
            # echo0("WARNING: LINUX_PREINSTALL in {} was bad."
            #       "  It will be changed to \"{}\"."
            #       "".format(globalsPath, LINUX_PREINSTALL))
            # appendConfLine(confLine)
        else:
            echo0("* '{}' is already present in \"{}\": {}"
                  "".format(confLine, globalsPath, gotLine))

    ui_path_line = get_line(ui_env_path, "/.local/bin")
    if ui_path_line is None:
        appendFileLine(ui_env_path,
                      'export PATH="$PATH:$HOME/.local/bin"')
        print("* added $HOME/.local/bin to PATH in {}"
              "".format(ui_env_path))
    else:
        print("* {} already has {}".format(ui_env_path, ui_path_line))

    line_flags = {}
    line_flags['export PATH="$PATH:$HOME/.local/bin"'] = "/.local/bin"
    line_flags['export PATH="$PATH:{}"'.format(utilities)] = utilities
    help_lines = []
    if enable_server:
        line_flags['export PATH="$PATH:{}"'.format(utilities_server)] = \
            utilities_server
    else:
        help_lines.append("- add the --server option to add the"
                          " utilities-server folder to your path in"
                          " {}."
                          "".format(sh_env_path))
    if enable_dev:
        line_flags['export PATH="$PATH:{}"'.format(utilities_dev)] = \
            utilities_dev
    else:
        help_lines.append("- add the --developer option to add the"
                          " utilities-developer folder to your path in"
                          " {}."
                          "".format(sh_env_path))
    echo2(indent+"* reading {}:".format(json.dumps(sh_env_path)))
    for line,flag in line_flags.items():
        got_sh_line = get_line(sh_env_path, flag)
        if got_sh_line is None:
            echo2("  - {} is not in {}".format(flag, sh_env_path))
            alt_flag = flag.replace("$HOME", "~")
            if alt_flag != flag:
                got_sh_line = get_line(sh_env_path, alt_flag)
                if got_sh_line is not None:
                    echo2("    - {} is.".format(alt_flag))
                else:
                    echo2("    - neither is {}.".format(alt_flag))
        if got_sh_line is None:
            appendFileLine(sh_env_path, line)
            print("* added {} to {}"
                  "".format(line, sh_env_path))
        else:
            print("* {} already has {}"
                  "".format(sh_env_path, got_sh_line))

    echo2(indent+"* reading {}:".format(json.dumps(sh_rc_path)))
    tmp_got_chm_lines = []
    for i in range(len(chm_lines)):
        tmp_got_chm_lines.append(get_line(sh_rc_path, chm_lines[i]))
    got_chm_lines = []
    missing_chm_lines = []
    for i in range(len(tmp_got_chm_lines)):
        got_line = tmp_got_chm_lines[i]
        if got_line is not None:
            got_chm_lines.append(got_line)
        else:
            missing_chm_lines.append(chm_lines[i])

    got_old_lines = []

    bad_lines = []
    echo2(indent+"* reading {}:".format(json.dumps(sh_env_path)))
    odd_add_line = 'PROMPT_COMMAND="history -a;$PROMPT_COMMAND"'
    odd_chm_lines = [old_add_line, old_set_line, odd_add_line]
    for chm_line in chm_lines + odd_chm_lines:
        echo1("  - checking for misplaced: {}".format(chm_line))
        bad_line =  get_line(sh_env_path, chm_line, indent="    ")
        # ^ check if in sh_env_path instead of correct sh_rc_path
        if bad_line is not None:
            bad_lines.append(bad_line)

    got_old_add_line = get_line(sh_rc_path, old_add_line)
    if got_old_add_line is not None:
        got_old_lines.append(got_old_add_line)
    got_old_set_line = get_line(sh_rc_path, old_set_line)
    if got_old_set_line is not None:
        got_old_lines.append(got_old_set_line)
    remove_existing_lines = None
    edit_path = sh_rc_path
    if len(bad_lines) > 0:
        echo0("Error: lines are in {} but should be in {}."
             "".format(sh_env_path, sh_rc_path))
        remove_existing_lines = bad_lines
        edit_path = sh_env_path
    elif len(got_old_lines) > 0:
        remove_existing_lines = got_old_lines
        echo0("Error: Bash has a legacy history configuration.")
    else:
        if len(got_chm_lines) == 0:
            appendFileLine(sh_rc_path, cmd_history_multisession_sh)
            echo0("* wrote multi-session bash history saving to {}"
                  "".format(sh_rc_path))
        elif len(got_chm_lines) == 3:
            echo0("* {} already has multi-session bash history saving."
                  "".format(sh_rc_path))
        else:
            echo0("Error: the bash history setup is not recognized."
                  " Line(s) present but not {}"
                  "".format(missing_chm_lines))
            remove_existing_lines = got_chm_lines
    if remove_existing_lines is not None:
        echo0("- To install the improved multi-session bash history"
              " code, remove/comment the following {} line(s) from {}"
              " then run {} again:"
              "".format(len(remove_existing_lines),
                        json.dumps(edit_path), me))
        for old_line in remove_existing_lines:
            echo0(old_line)
        echo0("")
        return 1
    else:
        echo0("* Setup of bash tools completed successfully.")
        if len(help_lines) > 0:
            echo0()
            for help_line in help_lines:
                print(help_line)
        echo0()
    return 0

if __name__ == "__main__":
    sys.exit(main())
