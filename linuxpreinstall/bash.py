#!/usr/bin/env python
from __future__ import print_function
import sys
from linuxpreinstall import (
    echo0,
    echo1,
    echo2,
)
python_mr = sys.version_info.major

def get_bash_values(path, only_exported=False,
        builtins=['PWD', 'SHLVL', '_', '']):
    '''
    Process a script using bash then get all values from its
    environment as a dict.

    Keyword arguments:
    only_exported -- Only get variables that are exported using bash's
        export statement.
    builtins -- Remove these builtins from the results.

    Returns:
    A dictionary of values as bash interprets them.
    '''

    '''
    This was done with mostly trial and error and the documentation but
    looking at <https://stackoverflow.com/a/3505826/4541104> helped
    somewhat... *None* of the following commands will be able to
    display the variables with env if shell=True (which also keeps
    appending to PATH over and over)!
    '''

    if only_exported:
        echo2("* get_bash_values({})".format(json.dumps(path)))
        command = shlex.split("env -i bash -c 'source \"{}\" && env'"
                              "".format(path))
        '''
        ^ only gets exported variables and builtin variables:
            PWD="/home/owner/git/linux-preinstall"
            SHLVL="0"
            _="/usr/bin/env"
            =""
        '''

        # command = ['env', '-i', 'bash', '-c',
        #            'source {} && env'.format(path)]
        '''
        ^ Set all variables to exported as per xaviersjs' comment
          Sep 4, 2018 at 22:09
          * gets env but only exported variables.
            * env only shows exported and builtin variables:
              PWD="/home/owner/git/linux-preinstall"
              SHLVL="0"
              _="/usr/bin/env"
              =""
        '''
    else:
        # command = ['bash', '-c',
        #            'set -a && source "{}" && env'.format(path)]
        '''
        ^ shows all internal and external vars.
        ^ Set all variables to exported as per ahal's comment
          Sep 25, 2013 at 1:46
        '''

        command = ['env', '-i', 'bash', '-c',
                   'set -a; source {}; env'.format(path)]
        '''
        # ^ Set all variables to exported as per xaviersjs' comment

        #   Sep 4, 2018 at 22:09
        #   edited by Poikilos: -a to export all variables, change to
        #   ';'
        #   Tests:
        #   - It works in python.
        #   - It works in bash:
        #   env -i bash -c 'set -a && \
        #     source ~/.config/linux-preinstall/globals.rc && env'
        #   or:
        #   env -i bash -c 'set -a; \
        #     source /home/owner/.config/linux-preinstall/globals.rc; env'
        #     - It still doesn't provide the shell with the vars, but it
        #       does display them (Python can get the vars with env).
        '''
    results = {}
    count = 0
    if python_mr > 2:
        # based on <https://docs.python.org/3/library/subprocess.html
        # #subprocess.Popen>
        from subprocess import PIPE, Popen
        data = ""
        with Popen(command, stdout=PIPE, stderr=None, shell=False) as process:
            # ^ shell=True breaks it!
            out, err = process.communicate()
            line = out.decode("utf-8")
            data += line
        splitter = "\n"
        if len(data.split("\r")) > len(data.split("\n")):
            splitter = "\r"
            echo0("Warning: using \\r for newline in bash output.")
        for rawL in data.split(splitter):
            count += 1
            line = rawL.rstrip("\r\n")
            (key, _, value) = line.partition("=")
            # os.environ[key] = value
            if key.strip() == "":
                continue
            results[key] = value
            echo2('{}="{}"'.format(key, value.replace('"', '\\"')))
        echo2("* done processing {} line(s) of output".format(count))
    else:
        # based on code by Lesmana answered Aug 17, 2010 at 18:45
        # edited Sep 5, 2018 at 11:58
        # on <https://stackoverflow.com/a/3505826/4541104>
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        for line in proc.stdout:
            count += 1
            (key, _, value) = line.partition("=")
            # os.environ[key] = value
            if key.strip() == "":
                continue
            results[key] = value
            echo2('{}="{}"'.format(key, value.replace('"', '\\"')))
        proc.communicate()
        # pprint.pprint(dict(os.environ))
        echo2("* done reading {} line(s) of output".format(count))

    for key in builtins:
        if key in results:
            del results[key]
    # return dict(os.environ)
    return results


def get_bash_value(path, name):
    d = get_bash_values(path)
    return d.get(name)
