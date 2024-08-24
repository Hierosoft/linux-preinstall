#!/usr/bin/env python3
"""
Compare two keypass kdbx files.

Usage:
diffkeypass.py <file1.kdbx> <file2.kdbx>
diffkeypass.py <file2.kdbx>
# The second example will work if there is a default file,
#   which is determined as the newest file in ~/Nextcloud
#   (one that is at least 4 characters [plus ".kdbx"] is preferred)

Options:
--quiet                    Do not show warnings.
--min_date YYYY-MM-DD      Only show files modified *on or after* this date.

The program will use meld if present in your PATH.
"""
import os
import platform
import pykeepass
import lxml
import subprocess
import sys
import tempfile

from collections import OrderedDict
from datetime import datetime
from getpass import getpass
from pykeepass import PyKeePass

HOME = None
if platform.system() == "Windows":
    HOME = os.environ['USERPROFILE']
else:
    HOME = os.environ['HOME']

if sys.version_info.major < 3:
    input = raw_input  # noqa F821 # type: ignore


if __name__ == "__main__":
    SCRIPTS_PATH = os.path.dirname(os.path.realpath(__file__))
    REPO_PATH = os.path.dirname(SCRIPTS_PATH)
    sys.path.insert(0, REPO_PATH)


from linuxpreinstall import which  # noqa: E402

MELD_PATH = which("meld")

def echo0(*args, **kwargs):
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)
    return True


def compare_keepass(file1, file2, pwd1=None, pwd2=None, options=None,
                    tmp1=None, tmp2=None):
    prefix = "[compare_keepass] "
    if options is None:
        options = {}
    quiet = options.get('quiet')
    min_date_s = options.get('min_date')
    min_date = None
    if min_date_s:
        min_date = datetime.strptime(min_date_s, "%Y-%m-%d")
    echo0("min_date: {}".format(min_date))
    def pushm(*args):
        pass
    if not quiet:
        pushm = echo0
    if quiet not in [True, False, None]:
        raise TypeError("quiet must be True or False (got {} {})"
                        "".format(type(quiet).__name__, quiet))
    echo0('Comparing "{}" to "{}"'.format(file1, file2))
    try:
        kp1 = PyKeePass(file1, password=pwd1)
    except pykeepass.exceptions.CredentialsError:
        echo0('Incorrect password for "{}"'
              ''.format(file1))
        return 1
    # group = kp1.find_groups(name='social', first=True)
    # group.entries  # example result:
    # [Entry: "social/facebook (myusername)", Entry: "social/twitter (myusername)"]
    # entry = kp.find_entries(title='facebook', first=True)
    # entry.password  # example of getting value
    # entry.notes = 'primary facebook account'  # example of setting value
    # group = kp.add_group(kp.root_group, 'email')
    # kp.add_entry(group, 'gmail', 'myusername', 'myPassw0rdXX')
    # Entry: "email/gmail (myusername)"
    # kp.save()
    file1dir, file1name = os.path.split(file1)
    try:
        kp2 = PyKeePass(file2, password=pwd2)
    except pykeepass.exceptions.CredentialsError:
        echo0('Incorrect password for "{}"'
              ''.format(file2))
        return 1

    for entry2 in kp2.entries:
        # print("dir(entry2)={}".format(dir(entry2))):
        # 'add_attachment', 'atime', 'attachments', 'autotype_enabled',
        # 'autotype_sequence', 'ctime', 'custom_properties', 'delete',
        # 'delete_attachment', 'delete_custom_property',
        # 'delete_history', 'deref', 'dump_xml', 'expired', 'expires',
        # 'expiry_time', 'get_custom_property', 'group', 'history',
        # 'icon', 'is_a_history_entry', 'is_custom_property_protected',
        # 'mtime', 'notes', 'otp', 'parentgroup', 'password', 'path',
        # 'ref', 'save_history', 'set_custom_property', 'tags', 'title',
        # 'touch', 'url', 'username', 'uuid'

        if min_date:
            # INFO: Documentation of datetime says the following is offset-aware:
            #   d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None
            #   and following is naive:
            #   d.tzinfo is None or d.tzinfo.utcoffset(d) is None
            if min_date.tzinfo is None or min_date.tzinfo.utcoffset(min_date) is None:
                d = entry2.mtime
                if d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None:
                    # assume the user-specified date was the same time zone
                    #   as the keepass file:
                    min_date = min_date.replace(tzinfo=d.tzinfo)
            if entry2.mtime < min_date:
                continue
        # NOTE: atime, ctime, & mtime are datetime objects.
        differences = {
            "file1": OrderedDict(),
            "file2": OrderedDict(),
        }
        if not entry2.title:
            echo0("Warning: no title in entry (URL={}, group={})"
                  "".format(entry2.url, entry2.group))
            if not entry2.url:
                echo0("& no URL.")
                continue
        else:
            try:
                entry1 = kp1.find_entries_by_uuid(entry2.uuid, first=True)
            except lxml.etree.XPathEvalError:
                if entry2.url:
                    pushm('Warning: XPathEvalError in entry "{}" (URL={})'
                        ''.format(entry1.title, entry2.url))
                else:
                    pushm('Warning: XPathEvalError in entry "{}" (group={})'
                        ''.format(entry1.title, entry2.group))
                continue
        if not entry1 and entry2.title:
            # ^ and entry2.title avoids "Invalid predicate" lxml error
            #   (See issue #37)
            entry1 = kp1.find_entries(title=entry2.title, first=True)
        if not entry1 and entry2.url:
            entry1 = kp1.find_entries(url=entry2.url, first=True)
        if not entry1:
            print('- "{}" (URL="{}") is not in "{}"'
                  ' (tried uuid, title, and url)'
                  ''.format(entry2.title, entry2.url, file1name))
            if tmp1:
                tmp1.write('TITLE={}\n'.format(entry2.title))
                tmp1.write('URL={}\n'.format(entry2.url))
            continue

        if entry1.title != entry2.title:
            differences['file1']['title'] = entry1.username
            differences['file2']['title'] = entry2.username
            print('* title "{}" != "{}" (URL="{}")'
                  ''.format(entry1.title, entry2.title, entry2.group))

        if entry1.username != entry2.username:
            differences['file1']['username'] = entry1.username
            differences['file2']['username'] = entry2.username
            print('* username "{}" != "{}" for "{}" (URL="{}")'
                  ''.format(entry1.username, entry2.username, entry2.title, entry2.group))

        if entry1.password != entry2.password:
            differences['file1']['password'] = entry1.password
            differences['file2']['password'] = entry2.password
            print('* passwords differ "{}" != "{}" for {} (URL="{}")'
                  ''.format(entry1.password, entry2.password, entry2.title, entry2.group))

        if entry1.notes != entry2.notes:
            differences['file1']['notes'] = entry1.notes
            differences['file2']['notes'] = entry2.notes
            print('* notes differ """{}""" != """{}""" for {} (URL="{}")'
                  ''.format(entry1.notes, entry2.notes, entry2.title, entry2.group))

        if differences['file1'] or differences['file2']:
            if tmp1:
                print("+WRITE tmp1: " + 'TITLE={}\n'.format(entry1.title))
                tmp1.write('TITLE={}\n'.format(entry1.title))
                tmp1.write('URL={}\n'.format(entry1.url))
                for k, v in differences['file1'].items():
                    tmp1.write('{}="{}"\n'.format(k, v))
            if tmp2:
                print("+WRITE tmp2: " + 'TITLE={}\n'.format(entry1.title))
                tmp2.write('TITLE={}\n'.format(entry2.title))
                tmp2.write('URL={}\n'.format(entry2.url))
                for k, v in differences['file2'].items():
                    tmp2.write('{}="{}"\n'.format(k, v))

    echo0(prefix+"Done checking entries.")


def get_names_and_default(folder, min_len=None, ending=".kdbx"):
    try_names = []
    default_name = None
    for sub in os.listdir(folder):
        sub_path = os.path.join(folder, sub)
        if os.path.isdir(sub_path):
            continue
        if not sub.lower().endswith(ending):
            continue
        if (min_len is not None) and (len(sub) < min_len):
            continue
        if ((default_name is None)
                or (len(sub) < len(default_name))):
            default_name = sub
        try_names.append(sub)
    return {
        'names': try_names,
        'default_name': default_name,
    }


def join_all(folder, names):
    return [os.path.join(folder, name) for name in names]


def usage():
    echo0(__doc__)
    if not MELD_PATH:
        echo0("(meld was not found)")
    echo0("")


def main():
    default_dir = os.path.join(HOME, "Nextcloud")
    default_name = None
    default_path = None
    name_info = get_names_and_default(default_dir, min_len=9)
    # ^ First try to get a longer name (dev computer has unrelated db)
    # if not name_info.get('names'):
    #     name_info = get_names_and_default(default_dir)
    try_names = name_info.get('names')
    default_name = name_info.get('default_name')
    try_paths = []
    if default_name is not None:
        if default_name in try_names:
            try_names.remove(default_name)
        try_paths = join_all(default_dir, try_names)
        # ^ may still be [] (if only has default_name)
        default_path = os.path.join(default_dir, default_name)
    file1 = None
    file2 = None
    options = {}
    keys = ["min_date"]
    key_args = ["--"+key for key in keys]
    files = []
    key = None
    for argi in range(1, len(sys.argv)):
        arg = sys.argv[argi]
        # print("arg[{}]={}".format(argi, arg))
        if key:
            options[key] = arg
            key = None
        elif arg.startswith("--"):
            if arg == "--quiet":
                options['quiet'] = True
            elif arg in key_args:
                key = arg[2:].strip()
                if not key.strip():
                    usage()
                    echo0("-- should be followed by an option (no space)")
                    return 1
                elif key not in keys:
                    usage()
                    echo0("Error: Invalid option: {}".format(arg))
                    return 1
                elif key in options:
                    usage()
                    echo0("Error: {} was specified twice.".format(arg))
                    return 1
            else:
                usage()
                echo0("{} is not in {}".format(key, keys))
                echo0('Error: Invalid argument: {}'.format(arg))
                return 1
        else:
            if len(files) >= 2:
                usage()
                echo0('Error: Unexpected 3rd filename: "{}"'
                      ''.format(arg))
                return 1
            files.append(arg)
    if key:
        echo0("Error: {} must be followed by a value.".format(key))
        return 1
    if len(files) > 0:
        file1 = files[0]
    if len(files) > 1:
        file2 = files[1]
    else:
        file1 = None
        if len(files) > 0:
            file2 = files[0]
        # If only one arg, compare specified one to default
        if not default_path:
            echo0('Specify a old then new path.'
                  ' There is no kdbx in "{}"'
                  ''.format(default_dir))
            return 1
    if file1 is None:
        if default_path:
            file1 = default_path
    file2_m = None
    if file2 is None:
        for try_path in try_paths:
            this_m = os.path.getmtime(try_path)
            if ((file2_m is None)
                    or (this_m > file2_m)):
                file2 = try_path
                file2_m = this_m

    echo0("files:")
    echo0('- "{}"'.format(file1))
    echo0('- "{}"'.format(file2))
    pwd = getpass("Password: ")
    tmp_names = []
    with tempfile.NamedTemporaryFile(mode='w') as tmp1:
        echo0('Created "{}"'.format(tmp1.name))
        with tempfile.NamedTemporaryFile(mode='w') as tmp2:
            echo0('Created "{}"'.format(tmp2.name))
            tmp_names = [
                tmp1.name,
                tmp2.name,
            ]
            compare_keepass(
                file1,
                file2,
                pwd1=pwd,
                pwd2=pwd,
                options=options,
                tmp1=tmp1,
                tmp2=tmp2,
            )
            # Make a blocking call so meld can use the tmp files
            # but they will be deleted afterward:
            # os.system(cmd)  # also blocking
            # subprocess.call(cmd)
            # run is Preferred in Python > 3.5:
            if not MELD_PATH:
                echo0("Warning: meld is not present,"
                      " so the files {} will not be compared."
                      "".format(tmp_names))
                return 0
            elif not os.path.isfile(MELD_PATH):
                # This problem indicates which is faulty
                #   if that touched MELD_PATH last!
                raise FileNotFoundError('MELD_PATH was wrong: "{}"'
                                        ''.format(MELD_PATH))
            tmp1.flush()
            tmp2.flush()
            cmd_parts = [
                MELD_PATH,
                tmp1.name,
                tmp2.name,
            ]
            # Run and wait (wait so tmp files don't get deleted)
            subprocess.run(cmd_parts)
    if tmp_names:
        echo0("Deleted temp files:")
        for tmp_name in tmp_names:
            echo0('- "{}"'.format(tmp_name))
    echo0("Done comparing:")
    echo0('- "{}"'.format(file1))
    echo0('- "{}"'.format(file2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
