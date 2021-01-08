#!/usr/bin/env python3
import sys
import stat
import os
import shutil
import tarfile
import tempfile
from zipfile import ZipFile
import subprocess

me = os.path.split(sys.argv[0])[-1]
version_chars = "0123456789."
icons = {}
icons["freecad"] = "org.freecadweb.FreeCAD"
icons["ultimaker.cura"] = "cura"
captions = {}
captions["umlet"] = "UMLet Standalone"  # as opposed to a plugin/web ver
captions["freecad"] = "FreeCAD"
captions["argouml"] = "ArgoUML"
annotations = {}
annotations[".deb"] = " (deb)"
annotations[".appimage"] = " (AppImage)"


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
    print(me + " <file.deb> <Icon Caption>")
    print(me + " <path> --move")
    print(" "*len(me) + " ^ moves the directory to $HOME/.local/lib64")
    print(me + " <path> --uninstall")
    print(" "*len(me) + " ^ removes it from $HOME/.local/lib64")
    print(me + " <path> --reinstall")
    print(" "*len(me) + " ^ removes it from $HOME/.local/lib64 first")
    print("")
    print(me + " --help")
    print(" "*len(me) + " ^ Show this help screen.")
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

def dir_is_empty(folder_path):
    count = 0
    sub_names = os.listdir(folder_path)
    for sub_name in sub_names:
        count += 1
    return count < 1

shortcut_data_template = """[Desktop Entry]
Name={name}
Exec={x}
Icon={icon}
Terminal=false
Type=Application
"""

def get_annotation(s):
    bad_endings = [".sh", ".appimage", ".deb"]
    for ending in bad_endings:
        if s.lower().endswith(ending):
            annotation = annotations.get(ending)
            if annotation is not None:
                return annotation
    # print("  - {} is ok.".format(s))
    return ""



def without_ender(s, enable_annotations):
    bad_endings = [".sh", ".appimage", ".deb"]
    for ending in bad_endings:
        if s.lower().endswith(ending):
            if enable_annotations:
                annotation = annotations.get(ending)
                if annotation is not None:
                    return s[:-len(ending)] + annotation
            return s[:-len(ending)]
    # print("  - {} is ok.".format(s))
    return s


def install_program_in_place(src_path, caption=None, name=None,
        version=None, move_what=None, do_uninstall=False,
        icon_path=None, enable_reinstall=False,
        detect_program_parent=False):
    """Install binary program src_path

    If name is not specified, the name and version will be calculated
    from either the filename at src_path or the path's parent
    directory's name.
    Example:
    src_path=../Downloads/blender-2.79-e045fe53f1b0-linux-glibc217-x86_64/blender
    (In this case, this function will extract the name and version from
    blender-2.79-e045fe53f1b0-linux-glibc217-x86_64 since it has more
    delimiters than the filename "blender")

    move_what: Only set this to 'file' if src_path is an AppImage or
    other self-contained binary file. Otherwise you may set it to
    'directory'. The file or directory will be moved to ~/.local/lib64/
    (or whatever programs directory is detected as a parent of the
    directory if detect_program_parent is True [automaticaly True by
    calling itself in the case of deb]).
    move_what='file' example:
    If name is not specified, the name and version will be calculated from
    either the filename at src_path or the path's parent directory's name.
    Example:
    src_path=../Downloads/FreeCAD_0.18-16131-Linux-Conda_Py3Qt5_glibc2.12-x86_64.AppImage
    (In this case, this function will extract the name and version from
    FreeCAD_0.18-16131-Linux-Conda_Py3Qt5_glibc2.12-x86_64.AppImage)
    """
    local_path = os.path.join(os.environ["HOME"], ".local")
    share_path = os.path.join(local_path, "share")
    icons_path = os.path.join(share_path, "pixmaps")
    lib64 = os.path.join(local_path, "lib64")
    dst_programs = lib64  # changed if deb has a different programs dir
    dirname = None
    ex_tmp = None
    new_tmp = None
    verb = "uninstall" if do_uninstall else "install"
    ending = ".deb"
    if src_path.lower()[-(len(ending)):] == ending:
        ex_tmp = tempfile.mkdtemp()
        print("* extracting '{}' to '{}'...".format(src_path, ex_tmp))
        ex_command = "cd '{}' && ar xv '{}'".format(ex_tmp, src_path)
        # NOTE: Instead of `ar`, python-libarchive could also work.
        cmd_return = os.system(ex_command);
        if dir_is_empty(ex_tmp):
            print("ERROR: `{}` did not result in any extracted files or"
                  " directories in"
                  " '{}'".format(ex_command, ex_tmp))
            return False
        elif cmd_return != 0:
            print("ERROR: `{}` returned an error value"
                  " ({})".format(ex_command, cmd_return))
            return False
        print("")
        # tar = tarfile.open(src_path)
        # tar.extractall(path=ex_tmp)
        # tar.close()
        next_path = os.path.join(ex_tmp, "data.tar.xz")
        if not os.path.isfile(next_path):
            print("ERROR: Extracting deb did not result in"
                  " '{}'.".format(next_path))
            shutil.rmtree(ex_tmp)
            print("  * deleted {}.".format(ex_tmp))
            return False
        next_temp = tempfile.mkdtemp()
        print("* extracting '{}'...".format(next_path))
        try:
            tar = tarfile.open(next_path)
            tar.extractall(path=next_temp)
            tar.close()
        except tarfile.ReadError:
            print("ERROR: tar could not extract '{}'".format(next_path))
            return False
        shutil.rmtree(ex_tmp)  # Remove temporary directory containing
                               # only control.tar.gz, data.tar.xz, and
                               # debian-binary.
        # Now next_temp should contain directories such as usr & etc.
        src_usr = os.path.join(next_temp, "usr")
        src_opt = os.path.join(next_temp, "opt")
        src_usr_share = os.path.join(src_usr, "share")
        try_programs_paths = [src_usr_share, src_opt]
        found_any = False
        for folder_path in try_programs_paths:
            if os.path.isdir(folder_path):
                found_any = True
        if not found_any:
            print("ERROR: extracting '{}' from '{}' did not result in"
                  " any of the following:"
                  " '{}'".format(next_temp, next_path,
                                 try_programs_paths))
            shutil.rmtree(next_temp)
            return False
        found_programs_paths = []
        sub_names = None
        for folder_path in try_programs_paths:
            if not os.path.isdir(folder_path):
                continue
            not_programs = ["applications", "icons", "doc"]
            sub_names = os.listdir(folder_path)
            for sub_name in sub_names:
                sub_path = os.path.join(folder_path, sub_name)
                if os.path.isdir(sub_path) and (sub_name[:1] != "."):
                    if sub_name not in not_programs:
                        found_programs_paths.append(sub_path)
        if len(found_programs_paths) == 0:
            print("ERROR: extracting '{}' from '{}' did not result in"
                  " any programs in any known directories:".format(
                    next_temp,
                    next_path,
                )
            )
            for folder_path in try_programs_paths:
                if os.path.isdir(folder_path):
                    print("{} only contains:"
                          " {}".format(folder_path,
                                       os.listdir(folder_path)))
            shutil.rmtree(next_temp)
            print("* removed '{}'".format(next_temp))
            return False
        elif len(found_programs_paths) > 1:
            print("ERROR: extracting '{}' from '{}' resulted in"
                  " too many unknown directories in '{}': ({})".format(
                    next_temp,
                    next_path,
                    try_programs_paths,
                    found_programs_paths
                )
            )
            shutil.rmtree(next_temp)
            print("* removed '{}'".format(next_temp))
            return False
        program_temp = tempfile.mkdtemp()
        program_path = found_programs_paths[0]
        program = os.path.split(found_programs_paths[0])[-1]
        this_programs_path = os.path.split(found_programs_paths[0])[0]
        this_programs = os.path.split(this_programs_path)[-1]
        dst_programs = os.path.join(local_path, this_programs)
        print("* found programs path in deb: '{}'".format(dst_programs))

        if dst_programs == local_path:
            print("ERROR: source programs directory (directory"
                  " containing {}) was not"
                  " detected in deb.".format(program_path))
            shutil.rmtree(next_temp)
            print("* removed '{}'".format(next_temp))
            print("")
            print("{} did not complete.".format(verb))

            print("")
            exit(1)

        binaries = []
        binary_path = None
        folder_path = program_path
        sub_names = os.listdir(folder_path)
        print("* looking for {}...".format(program))
        try_program_names = [program, program.lower(), program.title(),
                             program.upper()]
        for sub_name in sub_names:
            sub_path = os.path.join(folder_path, sub_name)
            if os.path.isfile(sub_path) and (sub_name[:1] != "."):
                binaries.append(sub_name)
                print("* detected possible program file"
                      " '{}'".format(sub_path))
                if sub_name in try_program_names:
                    binary_path = sub_path
                    break
        if binary_path is None:
            if len(binaries) == 1:
                binary_path = os.path.join(program_path, binaries[0])
            else:
                shutil.rmtree(next_temp)
                if len(binaries) == 0:
                    print("ERROR: extracting '{}' from '{}' did not"
                          " result in any files such as binaries in"
                          " '{}' (only {})".format(
                            next_temp,
                            next_path,
                            program_path,
                            sub_names
                        )
                    )
                else:
                    print("ERROR: extracting '{}' from '{}'"
                          " resulted in more than one file in"
                          " '{}' and one is not named {}, so the binary"
                          " could not be detected (among {})".format(
                            next_temp,
                            next_path,
                            program_path,
                            try_program_names,
                            binaries
                        )
                    )
                return False

        # The program is extracted and detected. Now, find the icon:
        src_icons = os.path.join(src_usr_share, "icons")
        icon_path = None
        icon_count = 0
        if os.path.isdir(src_icons):
            for root, dirs, files in os.walk(src_icons):
                for sub_name in files:
                    sub_path = os.path.join(root, sub_name)
                    icon_path = os.path.join(icons_path, sub_name)
                    if do_uninstall:
                        if os.path.isfile(icon_path):
                            os.remove(icon_path)
                            print("* removed '{}'".format(icon_path))
                    else:
                        if not os.path.isdir(icons_path):
                            os.makedirs(icons_path)
                        try:
                            shutil.move(sub_path, icon_path)
                            print("* added '{}'".format(icon_path))
                        except Exception as e:
                            print("ERROR: moving '{}' to '{}'"
                                  " failed.".format(sub_path,
                                                    icon_path), e)
                            shutil.rmtree(next_temp)
                            print("* removed '{}'".format(next_temp))
                            return False
                    icon_count += 1
            if icon_count == 0:
                print("INFO: No icons were found in '{}' or its"
                      " subdirectories.".format(src_icons))
            if do_uninstall:
                for root, dirs, files in os.walk(src_icons):
                    for sub_name in dirs:
                        sub_path = os.path.join(icons_path, sub_name)
                        if not os.path.isdir(sub_path):
                            print("* WARNING: '{}' is already not"
                                  " present.".format(sub_path))
                            continue
                        if dir_is_empty(sub_path):
                            # This should work (deepest will be listed
                            # first) since walk sets topdown to False by
                            # default.
                            os.rmdir(sub_path)
                            print("* removed '{}'".format(sub_path))
            else:
                print("* using '{}' as icon".format(icon_path))
        else:
            print("INFO: No '{}' directory was found."
                  "".format(src_icons))
        # Now install the program:
        result = install_program_in_place(
            binary_path,
            caption=program+" (deb)",
            name=name,
            version=version,
            move_what='directory',
            do_uninstall=do_uninstall,
            icon_path=icon_path,
            enable_reinstall=enable_reinstall,
            detect_program_parent=True
        )
        shutil.rmtree(next_temp)
        print("* removed '{}'".format(next_temp))
        return result
    archive_categories = {}
    archive_categories["tar"] = [".tar.bz2", ".tar.gz", ".tar.xz"]
    archive_categories["zip"] = [".zip"]
    found_ending = None
    ar_cat = None
    for category, endings in archive_categories.items():
        for ending in endings:
            if src_path.lower()[-(len(ending)):] == ending:
                dirname = src_path[:-(len(ending))]
                found_ending = ending
                ar_cat = category
                break
    if (dirname is not None) and (not do_uninstall):
        move_what = 'directory'
        ex_tmp = tempfile.mkdtemp()
        print("* created '{}'".format(ex_tmp))
        print("* enabling move from directory '{}'".format(ex_tmp))
        sub_dirs = []
        sub_files = []
        print("* extracting '{}'...".format(src_path))
        if ar_cat == "tar":
            tar = tarfile.open(src_path)
            tar.extractall(path=ex_tmp)
            tar.close()
        elif ar_cat == "zip":
            with ZipFile(src_path, 'r') as zipfile:
                zipfile.extractall(path=ex_tmp)
        else:
            raise NotImplementedError("There is no case for " + ar_cat)
        print("* extracted '{}'".format(ex_tmp))
        folder_path = ex_tmp
        for sub_name in os.listdir(folder_path):
            sub_path = os.path.join(folder_path, sub_name)
            if os.path.isfile(sub_path):  #sub_name[:1]!="." and
                sub_files.append(sub_path)
            elif os.path.isdir(sub_path):
                sub_dirs.append(sub_path)
        dirpath = None
        new_tmp = None
        if (len(sub_dirs) == 1) and (len(sub_files) == 0):
            dirpath = sub_dirs[0]
            print("* detected program path '{}'".format(dirpath))
        else:
            dirpath = ex_tmp
            print("* detected program path '{}'".format(dirpath))
            new_tmp = tempfile.mkdtemp()
            dirpath = os.path.join(new_tmp, dirname)
            shutil.move(ex_tmp, dirpath)
            print("* changed temp program path to '{}'".format(dirpath))
        src_path = dirpath
        move_what = 'directory'
        print("* changed {} source to '{}'".format(verb, src_path))

    if os.path.isdir(src_path):
        print("* trying to detect binary...")
        src_name = os.path.split(src_path)[-1]
        only_name = src_name.strip("-0123456789. ")
        try_name = src_name.split("-")[0]
        try_path = os.path.join(src_path, try_name)
        print("  src_name: {}".format(src_name))
        print("  only_name: {}".format(only_name))
        if os.path.isfile(try_path):
            print("* detected binary: '{}'".format(try_path))
            src_path = try_path
        else:
            all_files = os.listdir(src_path)
            scripts = []
            jars = []
            for sub in all_files:
                sub_path = os.path.join(src_path, sub)
                ext = os.path.splitext(sub)[1].strip(".")
                if sub.startswith("."):
                    continue
                if os.path.isdir(sub_path):
                    continue
                if sub.endswith(".jar"):
                    jars.append(sub)
                elif (ext == "sh") or (ext == ""):
                    scripts.append(sub)
            if len(scripts) >= 2:
                bad_indices = []
                good_indices = []
                for script in scripts:
                    if script.startswith(only_name):
                        good_indices.append(only_name)
                    else:
                        bad_indices.append(only_name)
                if len(good_indices) == 1:
                    for bad_ii in range(len(bad_indices)-1, -1, -1):
                        bad_i = bad_indices[bad_ii]
                        del scripts[bad_i]
                    print("  only one matches \"{}\"".format(only_name))
                    enable_force_script = True
            if len(scripts) == 2:
                short_i = 0
                long_i = 1
                if len(scripts[0]) > len(scripts[1]):
                    short_i = 1
                    long_i = 0
                sName = scripts[short_i]
                lName = scripts[long_i]
                if lName.startswith(os.path.splitext(lName)):
                    # if has something like argouml.sh and
                    # argouml2.sh (experimental), use argouml.sh.
                    del scripts[long_i]
            if len(jars) > 0:
                enable_force_script = True
            if enable_force_script and (len(scripts) == 1):
                src_path = os.path.join(src_path, scripts[0])
                print("* detected executable script: '{}'"
                      "".format(src_path))
            else:
                print("* could not detect binary in {}"
                      "".format(all_files))
                print("  scripts: {}".format(scripts))
                print("  jars: {}".format(jars))
                return False



    if src_path is None:
        usage()
        print("ERROR: You must specify a path to a binary file.")
        return False
    elif not os.path.isfile(src_path):
        usage()
        print("ERROR: '{}' is not a file.".format(src_path))
        src_name = os.path.split(src_path)[-1]
        try_dest_path = os.path.join(dst_programs, src_name)
        if not do_uninstall:
            if os.path.isfile(try_dest_path):
                print("'{}' is already {}ed.".format(try_dest_path,
                                                     verb))
            return False
    print("{} started.".format(verb.title()))

    filename = os.path.split(src_path)[-1]
    dirpath = os.path.split(src_path)[-2]
    if detect_program_parent:
        this_programs_path = os.path.split(dirpath)[0]
        this_programs = os.path.split(this_programs_path)[-1]
        dst_programs = os.path.join(local_path, this_programs)
        if dst_programs == local_path:
            print("ERROR: source programs directory (directory"
                  " containing {}) was not"
                  " detected.".format(src_path))
            if ex_tmp is not None:
                if os.path.isdir(ex_tmp):
                    shutil.rmtree(ex_tmp)
                    print("* removed '{}'".format(ex_tmp))
            if new_tmp is not None:
                if os.path.isdir(new_tmp):
                    shutil.rmtree(new_tmp)
                    print("* removed '{}'".format(new_tmp))
            print("")
            print("{} did not complete.".format(verb.title()))
            print("")
            exit(1)

    print("* using programs path: '{}'".format(dst_programs))
    dirname = os.path.split(dirpath)[-1]
    icon_name = None

    if (name is None) or (version is None):
        try_names = [filename, dirname]
        parts = None
        for try_name in try_names:
            delimiters = "_-"
            try_parts = split_any(try_name, delimiters)
            if (parts is None) or (len(try_parts) > len(parts)):
                parts = try_parts
        if parts is not None:
            version_flags = []
            for part in parts:
                version_flags.append(False)
            del part
            part1 = None
            part2 = None
            if version is None:

                if len(parts) > 1:
                    part1 = without_ender(parts[1], False)
                if len(parts) > 2:
                    part2 = without_ender(parts[2], False)
                if (part1 is not None) and (is_version(part1)):
                    version = part1
                    version_flags[1] = True
                    print("* using '" + version + "' as version")
                elif (part2 is not None) and (is_version(part2)):
                    version = part2
                    version_flags[2] = True
                    print("* using '" + version + "' as version")
                else:
                    print("* INFO: \"{}\" is not a version"
                          "".format(part1))
            if name is None:
                name = parts[0]
                annotation = get_annotation(src_path)
                if len(annotation) > 0:
                    print("* appending \"{}\" to caption"
                          "".format(annotation))
                name = without_ender(name, False)
                if caption is None:
                    try_name = parts[0].lower()
                    if len(parts) > 1:
                        try_name += " " + parts[1].lower()
                    try_name = without_ender(try_name, False)
                    caption = captions.get(try_name)
                if caption is None:
                    part0 = captions.get(name.lower())
                    if part0 is None:
                        part0 = without_ender(name, False)
                        if part0.lower() == part0:
                            print("* The program {} is unknown and"
                                  " all lowercase, so the"
                                  " caption will be {} in title case"
                                  " (parts: {})."
                                  "".format(name, try_name, parts))
                            part0 = part0.title()
                        # else Retain existing case (if any not lower).
                    if len(parts) > 1:
                        part1 = without_ender(parts[1], False)
                        if part1.lower() == part1:
                            part1 = part1.title()
                        # else Retain existing case (if any not lower).
                        caption = part0 + " " + part1
                        caption += annotation
                    else:
                        caption = part0
                        caption += annotation
                        print("* WARNING: there is only 1 part, so the"
                              " caption \"{}\" may not be correct for"
                              " parts: {}".format(caption, parts))
                    # print("* generated caption: {}".format(caption))
                    # TODO: remove redundant code above--see below.
                icon_name = name.lower()
                if (len(parts) > 1) and (len(parts[1]) > 0) and (parts[1][0] == parts[1][0].upper()) and (not version_flags[1]):
                    name += " " + parts[1]
                name = name.lower()
                name = name.replace(" ", ".")
                print("* using '" + name + "' as internal program name")
            else:
                print("* using specified name: {}".format(name))
        else:
            usage()
            print("End of program name (any of '" + breakers
                  + "') is not in " + try_name)
            print("")
            print("")
            return False
    else:
        print("* The name was set to {}".format(name))
        print("* The version was set to {}".format(version))

    applications = os.path.join(share_path, "applications")
    sc_path = None
    sc_name = None
    is_appimage = False
    dotted_parts = src_path.split(".")
    if dotted_parts[-1].lower() == "appimage":
        is_appimage = True

    if name.lower() == "blender":
        if version is not None:
            sc_name = "org.blender-{}".format(version)
        else:
            sc_name = "org.blender"
        print("* using {} as shortcut name".format(sc_name))
    elif version is not None:
        sc_name = "{}-{}".format(name.lower(), version)
    else:
        print("* no version is detected in {}".format(src_path))
        sc_name = "{}".format(name.lower())
    if is_appimage:
        sc_name += "-appimage"
    sc_name += ".desktop"
    sc_path = os.path.join(applications, sc_name)
    if icon_name is None:
        icon_name = name.lower()
    try_icon = icons.get(name.lower())
    print("* checking for known icon related to '{}'..."
          "".format(name.lower()))

    if try_icon is not None:
        icon_name = try_icon
        print("  * using known icon '{}'".format(icon_name))
    if caption is None:
        icon_name = try_icon
        print("  * using unknown icon '{}'".format(icon_name))
        caption = name
        if version is not None:
            caption += " " + version
        caption = caption[:1].upper() + caption[1:].lower()
        if is_appimage:
            caption += " (AppImage)"
        print("* using '" + caption + "' as caption")
    path = src_path
    # dst_programs = os.path.join(os.environ.get("HOME"), ".config")
    if move_what == 'file':
        if not os.path.isdir(dst_programs):
            if not do_uninstall:
                os.makedirs(dst_programs)
            else:
                print("'{}' does not exist, so there is nothing to {}."
                      "".format(dst_programs, verb))
                return True
        path = os.path.join(dst_programs, filename)
        if src_path != path:
            if not do_uninstall:
                print("mv \"{}\" \"{}\"".format(src_path, path))
                if src_path != path:
                    shutil.move(src_path, path)
                else:
                    print("The file is already at '{}'.".format(path))
            else:
                print("rm \"{}\"".format(path))
                os.remove(path)
                if src_path == path:
                    print("The source path"
                          " '{}' is removed.".format(path))
    elif move_what == 'directory':
        dst_dirpath = os.path.join(dst_programs, dirname)
        if do_uninstall:
            if os.path.isdir(dst_dirpath):
                shutil.rmtree(dst_dirpath)
            else:
                print("There is no '{}'.".format(dst_dirpath))
        else:
            print("mv '{}' '{}'".format(dirpath, dst_dirpath))
            if os.path.isdir(dst_dirpath):
                if enable_reinstall:
                    shutil.rmtree(dst_dirpath)
                else:
                    print("ERROR: '{}' already exists. Use the"
                          " --reinstall option to ERASE the"
                          " directory.".format(dst_dirpath))
                    return False
            shutil.move(dirpath, dst_dirpath)
            path = os.path.join(dst_dirpath, filename)


    if not do_uninstall:
        os.chmod(path, stat.S_IRWXU | stat.S_IXGRP | stat.S_IRGRP
                       | stat.S_IROTH | stat.S_IXOTH)
        # stat.S_IRWXU : Read, write, and execute by owner
        # stat.S_IEXEC : Execute by owner
        # stat.S_IXGRP : Execute by group
        # stat.S_IXOTH : Execute by others
        # stat.S_IREAD : Read by owner
        # stat.S_IRGRP : Read by group
        # stat.S_IROTH : Read by others
        # stat.S_IWOTH : Write by others
        # stat.S_IXOTH : Execute by others

    if icon_path is None:
        icon_path = icon_name

    shortcut_data = shortcut_data_template.format(x=path,
                                                  name=caption,
                                                  icon=icon_path)

    my_dir = os.path.dirname(os.path.realpath(__file__))
    meta_dir = os.path.join(my_dir, "shortcut-metadata")
    meta_path = os.path.join(meta_dir, "{}.txt".format(name))

    shortcut_append_lines = None
    if os.path.isfile(meta_path):
        with open(meta_path) as f:
            print("* using shortcut metadata from '{}'"
                  "".format(meta_path))
            lines = f.readlines()  # includes newlines!
            shortcut_append_lines = []
            for line_original in lines:
                line = line_original.rstrip()
                shortcut_append_lines.append(line)

    if shortcut_append_lines is not None:
        shortcut_data += "\n".join(shortcut_append_lines)
    if shortcut_data[-1] != "\n":
        shortcut_data += "\n"
    if not do_uninstall:
        # shutil.rmtree(dirpath)
        if ex_tmp is not None:
            if os.path.isdir(ex_tmp):
                shutil.rmtree(ex_tmp)
        if new_tmp is not None:
            if os.path.isdir(new_tmp):
                shutil.rmtree(new_tmp)
    desktop_installer = "xdg-desktop-menu"
    u_cmd_parts = [desktop_installer, "uninstall", sc_path]
    if do_uninstall:
        if os.path.isfile(sc_path):
            print(u_cmd_parts)
            subprocess.run(u_cmd_parts)
            print("rm \"{}\"".format(sc_path))
            os.remove(sc_path)
        else:
            print("* The shortcut was not present: {}".format(sc_path))
        return True
    else:
        tmp_sc_dir_path = tempfile.mkdtemp()
        tmp_sc_path = os.path.join(tmp_sc_dir_path, sc_name)
        ok = False
        with open(tmp_sc_path, 'w') as outs:
            outs.write(shortcut_data)
            ok = True
        if ok:
            # NOTE: There is no vendor prefix but xdg specifies that
            # there should be. The --novendor flag forces the install.
            if os.path.isfile(sc_path):
                # Remove the old one, otherwise xdg-desktop-menu install
                # will not refresh the icon from storage.
                # print("* removing shortcut \"{}\"".format(sc_path))
                # os.remove(sc_path)
                print("* uninstalling shortcut \"{}\"".format(sc_path))
                subprocess.run(u_cmd_parts)
                # ^ using only the name also works: sc_name])
                # ^ uninstall ensures that the name updates if existed
            install_proc = subprocess.run([desktop_installer,
                                           "install", "--novendor",
                                           tmp_sc_path])
            inst_msg = "OK"
            if install_proc.returncode != 0:
                inst_msg = "FAILED"
            if os.path.isfile(sc_path):
                os.chmod(sc_path,
                         (stat.S_IROTH | stat.S_IREAD | stat.S_IRGRP
                          | stat.S_IWUSR))
                print("* installing '{}'...{}".format(sc_path,
                                                      inst_msg))
            else:
                print("* installing '{}'...".format(sc_name,
                                                    inst_msg))
            print("  Name={}".format(caption))
            print("  Exec={}".format(path))
            print("  Icon={}".format(icon_path))
            # print("")
            # print("You may need to reload the application menu, such"
            # #     " as via one of the following commands:")
            # print("  ")
            # or xdg-desktop-menu install mycompany-myapp.desktop
        return ok
    return False

if __name__ == "__main__":
    print("")
    caption = None
    src_path = None
    if len(sys.argv) < 2:
        usage()
        print("You must specify a binary file.")
        print("")
        print("")
        exit(1)
    do_uninstall = False
    enable_reinstall = False
    move_what = None
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg[:2] == "--":
            if arg == "--uninstall":
                do_uninstall = True
            elif arg == "--move":
                move_what = 'any'
            elif arg == "--reinstall":
                enable_reinstall = True
            elif arg == "--help":
                usage()
                exit(0)
            else:
                print("ERROR: '{}' is not a valid option.".format(arg))
                exit(1)
        else:
            if src_path is None:
                src_path = arg
            elif caption is None:
                caption = arg
            else:
                print("A 3rd parameter is unexpected: '{}'".format(arg))
                exit(1)
    if src_path is None:
        print("You must specify a source path.")
        exit(1)
    src_path = os.path.abspath(src_path)
    if move_what == 'any':
        if os.path.isdir(src_path):
            move_what = 'directory'
        elif os.path.isfile(src_path):
            move_what = 'file'
        else:
            print("{} is not a file nor a directory.".format(src_path))
            exit(1)


    parts = src_path.split('.')
    if parts[-1] == "AppImage":
        move_what='file'

    install_program_in_place(
        src_path,
        caption=caption,
        move_what=move_what,
        do_uninstall=do_uninstall,
        enable_reinstall=enable_reinstall
    )
