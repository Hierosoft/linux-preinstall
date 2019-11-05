#!/usr/bin/env python
import sys
import stat
import os
import shutil

me = os.path.split(sys.argv[0])[-1]
version_chars = "0123456789."
icons = {}
icons["freecad"] = "org.freecadweb.FreeCAD"

def is_version(s):
    for c in s:
        if c not in version_chars:
            return False
    return True

def usage():
    print("")
    print("USAGE:")
    print(me + " <Program Name_version.AppImage>")
    print(me + " <file.AppImage> <Icon Caption>")
    print("")
    print("")

def split_any(s, delimiters):
    ret = []
    parts = s.split(delimiters[0])
    if len(delimiters) > 1:
        for part in parts:
            ret += split_any(part, delimiters[1:])
    else:
        ret = parts
    return ret

shortcut_data_template = """[Desktop Entry]
Name={name}
Exec={x}
Icon={iconName}
Terminal=false
Type=Application
"""

"""Install binary program src_path

If name is not specified, the name and version will be calculated from
either the filename at src_path or the path's parent directory's name.
Example: src_path=../Downloads/blender-2.79-e045fe53f1b0-linux-glibc217-x86_64/blender
(In this case, this function will extract the name and version from
blender-2.79-e045fe53f1b0-linux-glibc217-x86_64 since it has more
delimiters than the filename "blender")

do_move: Only set this to true if src_path is an AppImage or other self-
contained binary file. The file will be moved to ~/.local/lib64/
do_move=True example:
If name is not specified, the name and version will be calculated from
either the filename at src_path or the path's parent directory's name.
Example: src_path=../Downloads/FreeCAD_0.18-16131-Linux-Conda_Py3Qt5_glibc2.12-x86_64.AppImage
(In this case, this function will extract the name and version from
FreeCAD_0.18-16131-Linux-Conda_Py3Qt5_glibc2.12-x86_64.AppImage)
"""
def install_program_in_place(src_path, caption=None, name=None, version=None, do_move=False):

    local = os.path.join(os.environ["HOME"], ".local")
    lib64 = os.path.join(local, "lib64")
    programs = lib64

    if src_path is None:
        usage()
        print("ERROR: You must specify a path to a binary file.")
        return False
    elif not os.path.isfile(src_path):
        usage()
        print("ERROR: '{}' is not a file.".format(src_path))
        src_name = os.path.split(src_path)[-1]
        try_dest_path = os.path.join(programs, src_name)
        if os.path.isfile(try_dest_path):
            print("'{}' is already installed.".format(try_dest_path))
        return False

    filename = os.path.split(src_path)[-1]
    dirpath = os.path.split(src_path)[-2]
    dirname = os.path.split(dirpath)[-1]
    version = None

    if (name is None) or (version is None):
        try_names = [filename, dirname]
        parts = None
        for try_name in try_names:
            delimiters = "_-"
            try_parts = split_any(try_name, delimiters)
            if (parts is None) or (len(try_parts) > len(parts)):
                parts = try_parts
        if parts is not None:
            if name is None:
                name = parts[0]
                print("* using '" + name + "' as program name")
            if version is None:
                if (len(parts) > 1) and (is_version(parts[1])):
                    version = parts[1]
                    print("* using '" + version + "' as version")
        else:
            usage()
            print("End of program name (any of '" + breakers
                  + "') is not in " + try_name)
            print("")
            print("")
            return False


    share = os.path.join(local, "share")
    applications = os.path.join(share, "applications")
    shortcut = None
    shortcut_name = None
    is_appimage = False
    dotted_parts = src_path.split(".")
    if dotted_parts[-1].lower() == "appimage":
        is_appimage = True

    if name.lower() == "blender":
        if version is not None:
            shortcut_name = "org.blender-{}".format(version)
        else:
            shortcut_name = "org.blender"
    elif version is not None:
        shortcut_name = "{}-{}".format(name.lower(),version)
    else:
        shortcut_name = "{}".format(name.lower())
    if is_appimage:
        shortcut_name += "-appimage"
    shortcut_name += ".desktop"
    shortcut = os.path.join(applications, shortcut_name)
    iconName = name.lower()
    try_icon = icons.get(name.lower())

    if try_icon is not None:
        iconName = try_icon
    if caption is None:
        caption = name
        if version is not None:
            caption += " " + version
        caption = caption[:1].upper() + caption[1:].lower()
        if is_appimage:
            caption += " (AppImage)"
        print("* using '" + caption + "' as caption")
    path = src_path
    # programs = os.path.join(os.environ.get("HOME"), ".config")
    if do_move:
        if not os.path.isdir(programs):
            os.makedirs(programs)
        path = os.path.join(programs, filename)
        if src_path != path:
            print("mv \"{}\" \"{}\"".format(src_path, path))
            shutil.move(src_path, path)

    os.chmod(path, stat.S_IRWXU | stat.S_IXGRP | stat.S_IRGRP | stat.S_IROTH | stat.S_IXOTH)
    # stat.S_IRWXU : Read, write, and execute by owner
    # stat.S_IEXEC : Execute by owner
    # stat.S_IXGRP : Execute by group
    # stat.S_IXOTH : Execute by others
    # stat.S_IREAD : Read by owner
    # stat.S_IRGRP : Read by group
    # stat.S_IROTH : Read by others
    # stat.S_IWOTH : Write by others
    # stat.S_IXOTH : Execute by others

    shortcut_data = shortcut_data_template.format(x=path,
                                                  name=caption,
                                                  iconName=iconName)

    my_dir = os.path.dirname(os.path.realpath(__file__))
    meta_dir = os.path.join(my_dir, "shortcut-metadata")
    meta_path = os.path.join(meta_dir, "{}.txt".format(name))

    shortcut_append_lines = None
    if os.path.isfile(meta_path):
        with open(meta_path) as f:
            print("* using shortcut metadata from '{}'".format(meta_path))
            lines = f.readlines()  # includes newlines!
            shortcut_append_lines = []
            for line_original in lines:
                line = line_original.rstrip()
                shortcut_append_lines.append(line)

    if shortcut_append_lines is not None:
        shortcut_data += "\n".join(shortcut_append_lines)
    if shortcut_data[-1] != "\n":
        shortcut_data += "\n"
    with open(shortcut, 'w') as outs:
        outs.write(shortcut_data)
        print("Wrote '{}'".format(shortcut))
        print("  Name={}".format(caption))
        print("  Exec={}".format(path))
        print("  Icon={}".format(iconName))
        os.chmod(shortcut, stat.S_IROTH | stat.S_IREAD | stat.S_IRGRP | stat.S_IWUSR)
        return True
    return False

if __name__ == "__main__":
    caption = None
    src_path = None
    if len(sys.argv) < 2:
        usage()
        print("You must specify a binary file.")
        print("")
        print("")
        exit(1)
    src_path = sys.argv[1]
    if len(sys.argv) >= 3:
        caption = sys.argv[2]
    parts = src_path.split('.')
    do_move=False
    if parts[-1] == "AppImage":
        do_move=True

    install_program_in_place(src_path, caption=caption, do_move=do_move)
