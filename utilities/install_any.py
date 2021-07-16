#!/usr/bin/env python
import sys
import stat
import os
import shutil
import tarfile
import tempfile
from zipfile import ZipFile
import platform

python_mr = 3  # major revision
try:
    import urllib.request
    request = urllib.request
except:
    # python2
    python_mr = 2
    import urllib2 as urllib
    request = urllib

'''
    class SubprocessError(Exception):
        pass


    class CalledProcessError(SubprocessError):
        def __init__(self, returncode, cmd, output=None):
            self.returncode = returncode
            self.cmd = cmd
            self.output = output
            self.stdout = None
            self.stderr = None
        # commented since same in Python 2 & 3
'''
# from subprocess import CalledProcessError
# from subprocess import SubprocessError

import subprocess
try:
    # from subprocess import run as sp_run
    from subprocess import CompletedProcess
except ImportError:
    # Python 2
    class CompletedProcess:
        _custom_impl = True

        def __init__(self, args, returncode, stdout=None, stderr=None):
            self.args = args
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

        def check_returncode(self):
            if self.returncode != 0:
                err = subprocess.CalledProcessError(self.returncode,
                                                    self.args,
                                                    output=self.stdout)
                raise err
            return self.returncode

    def sp_run(*popenargs, **kwargs):
        '''
        CC BY-SA 4.0
        by Martijn Pieters
        https://stackoverflow.com/a/40590445
        and Poikilos
        '''
        input = kwargs.pop("input", None)
        check = kwargs.pop("handle", False)

        if input is not None:
            if 'stdin' in kwargs:
                raise ValueError('stdin and input arguments may not '
                                 'both be used.')
            kwargs['stdin'] = subprocess.PIPE

        process = subprocess.Popen(*popenargs, **kwargs)
        try:
            outs, errs = process.communicate(input)
        except:
            process.kill()
            process.wait()
            raise
        returncode = process.poll()
        # print("check: {}".format(check))
        # print("returncode: {}".format(returncode))
        if check and returncode:
            raise subprocess.CalledProcessError(returncode, popenargs,
                                                output=outs)
        return CompletedProcess(popenargs, returncode, stdout=outs,
                                stderr=errs)
    subprocess.run = sp_run


digits = "0123456789"
# me = os.path.split(sys.argv[0])[-1]
# ^ doesn't work correctly if used as a module
me = "install_any.py"
myDir = os.path.dirname(os.path.abspath(__file__))
repoDir = os.path.dirname(myDir)
version_chars = digits + "."

# The following dictionaries contain information that can't be derived
# from the installer file's name.
icons = {}  # A list of preferred icon file names indexed by LUID
icons["freecad"] = "org.freecadweb.FreeCAD"
icons["ultimaker.cura"] = "cura"
iconLinks = {}  # A list URLs to icon graphics indexed by LUID
iconLinks["ultimaker.cura"] = "https://github.com/Ultimaker/Cura/raw/master/icons/cura-48.png"
iconLinks["prusaslicer"] = "https://github.com/prusa3d/PrusaSlicer/raw/master/resources/icons/PrusaSlicer.png"
iconLinks["pycharm.community"] = "https://github.com/JetBrains/intellij-community/raw/master/python/resources/PyCharmCore128.png"
iconLinks["keepassxc"] = "https://github.com/keepassxreboot/keepassxc/raw/develop/share/icons/application/scalable/apps/keepassxc.svg"
iconLinks["unityhub"] = "https://img.icons8.com/ios-filled/50/000000/unity.png"
casedNames = {}  # A list of correct icon captions indexed by LUID
casedNames["umlet"] = "UMLet Standalone"  # as opposed to a plugin/web ver
casedNames["freecad"] = "FreeCAD"
casedNames["android.studio.ide"] = "Android Studio IDE"
casedNames["flashprint"] = "FlashPrint"
casedNames["argouml"] = "ArgoUML"
annotations = {}
annotations[".deb"] = "deb"
annotations[".appimage"] = "AppImage"


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


shortcut_data_template = """[Desktop Entry]
Name={Name}
Exec={Exec}
Icon={Icon}
Terminal=false
Type=Application
"""


def test_CompletedProcessException(code):
    proc = CompletedProcess(["(tests)"], code, sys.stdout,
                            sys.stderr)
    try:
        proc.check_returncode()
        raise ValueError("* The exception test failed (running"
                         " check_returncode on returncode {} didn't"
                         " succeed in producing CalledProcessError)"
                         "".format(proc.returncode))
    except subprocess.CalledProcessError:
        pass
        print("* The exception test passed.")


def test_subprocess_run(argsOrString):
    fn_msg = (" (Python {}'s standard implementation)"
              "".format(sys.version_info[0]))
    if hasattr(CompletedProcess, '_custom_impl'):
        fn_msg = " (Python 2 polyfill)"
    print("* Testing subprocess.run{} with {}..."
          "".format(fn_msg, type(argsOrString).__name__))
    proc = subprocess.run(argsOrString)
    print("* proc.returncode: {}".format(proc.returncode))
    print("* proc.stdout: {}".format(proc.stdout))
    print("* proc.stderr: {}".format(proc.stdout))


def tests():
    # if hasattr(CompletedProcess, "_custom_impl"):
    test_CompletedProcessException(1)
    test_subprocess_run("ls")
    test_subprocess_run(["ls", "-l"])
    test_return_sh = os.path.join(repoDir, "tests", "data", "exit1.sh")
    if os.path.isfile(test_return_sh):
        test_subprocess_run(test_return_sh)
    else:
        print("* [{}] skipped the process return test since"
              " \"{}\" does not exist.".format(me, test_return_sh))
        #raise RuntimeError("The {} process return test failed since"
        #                   " \"{}\" does not exist."
        #                   "".format(me, test_return_sh))
    # else:
    #     print("* The exception test was skipped since you are using"
    #           " Python's implementation of CompletedProcess.")

    # if failures == 0:
    print("* All tests passed.")
    # else:
    #     print("* Tests completed with {} failure(s).".format(failures))


# TODO: Run tests() using nose.

def toLUID(name):
    return name.replace(" ", ".").lower()


def get_annotation(s):
    '''
    Get the annotation which separates the software from a differently-
    packaged copy.
    '''
    bad_endings = [".sh", ".appimage", ".deb"]
    for ending in bad_endings:
        if s.lower().endswith(ending):
            annotation = annotations.get(ending)
            if annotation is not None:
                return annotation
    # print("  - {} is ok.".format(s))
    return None


def find_all_cs(haystack, needle):
    '''get indices of every match of the needle (case sensitive)'''
    results = []
    i = 0
    nLen = len(needle)
    while i < len(haystack):
        if haystack[i:i+nLen] == needle:
            results.append(i)
            i += nLen
            continue
        i += 1
    return results


def find_all_ci(haystack, needle):
    '''get indices of every match of the needle (case insensitive)'''
    haystack = haystack.lower()
    needle = needle.lower()
    return find_all_cs(haystack, needle)
    # ^ lower so ok to call *_cs


def find_all_any_cs(haystack, needles):
    '''
    Get a list of tuples where each pair is an index of a match of every
    needle (case sensitive) paired with the needle in the second slot.
    '''
    results = []
    for needle in needles:
        found = find_all_cs(haystack, needle)
        results += list(zip(found, [needle]*len(found)))
    return results


def find_all_any_ci(haystack, needles):
    '''
    Get a list of tuples where each pair is an index of a match of every
    needle (case insensitive) paired with the needle in the second slot.
    '''
    results = []
    haystackL = haystack.lower()
    for needle in needles:
        found = find_all_cs(haystackL, needle.lower())
        results += list(zip(found, [needle]*len(found)))
        # ^ lower so ok to call *_cs
    return results


def find_tuple_with(tuples, index, needle):
    '''
    Find the index where element 'index' of the tuple is needle
    (case-sensitive).
    '''
    for i in range(len(tuples)):
        if tuples[i][index] == needle:
            return i
    return -1


def has_tuple_with(tuples, index, needle):
    '''
    Determine if needle is in any element 'index' of any tuple in the
    list of tuples.
    '''
    return find_tuple_with(tuples, index, needle) > -1


def split_any(s, delimiters, blobs=None):
    '''
    Sequential arguments:
    delimiters -- a list of one-character delimiters at which to split s

    Keyword arguments:
    blobs -- a list of strings to never split (for example, include
             'x86_64' as a blob when '_' is in delimiters but you want
             to not split at '_' in cases where it is in that blob)
    '''
    ret = []
    start = 0
    blobIs = None
    oldS = s
    print("[split_any] checking for {}".format(blobs))
    if blobs is not None:
        # replace bad dots with delimiters (example: change .i386 to
        # _i386.
        i = -1
        while i + 1 < len(s):
            i += 1
            for blob in blobs:
                if i == 0:
                    continue
                elif s[i-1] != '.':
                    continue
                if s[i:i+len(blob)].lower() == blob.lower():
                    # if s[i-1] == '.':
                    if len(delimiters[0]) > 1:
                        raise ValueError("delimiter[0] ('{}') is too"
                                         " long (should be 1"
                                         " character)."
                                         "".format(delimiters[0]))
                    s = s[:i-1] + delimiters[0] + s[i:]
                # else:
                #     print("[split_any] {} is not {}"
                #           "".format(s[i:i+len(blob)].lower(),
                #                     blob.lower()))
        del i
    if s != oldS:
        print("[split_any] preprocessed {} to {}".format(oldS, s))
    else:
        print("[split_any] There was nothing to preprocess in {}"
              "".format(s))
    if blobs is not None:
        blobIs = find_all_any_ci(s, blobs)
    i = 0
    while i < len(s):
        c = s[i]
        if blobIs is not None:
            # print("[split_any] checking in {}".format(blobIs))
            foundI = find_tuple_with(blobIs, 0, i)
            if foundI > -1:
                # print("[split_any] {} is in {}".format(i, blobIs))
                # If a blob had been found at i, skip i to end of blob.
                # Do not end here.
                i += len(blobIs[foundI][1])
                continue
        if c in delimiters:
            print("[split_any] {} is in {}".format(c, delimiters))
            ret.append(s[start:i])
            start = i + 1
        i += 1
    # Add the last slice, whether ends in delimiter or not.
    ret.append(s[start:i])
    '''
    parts = s.split(delimiters[0])
    if len(delimiters) > 1:
        for part in parts:
            ret += split_any(part, delimiters[1:])
    else:
        ret = parts
    '''
    # print("[split_any] split into {}".format(ret))
    return ret


def is_version(s, allowLettersAtEnd, allowMore=None):
    '''
    Sequential arguments:
    allowLettersAtEnd -- If True, allow letters (but no more numbers
                         after the first letter) at the end if starts
                         with a number (such as for "2.79b").

    Keyword arguments:
    allowMore -- a list such as PackageInfo.VPARTS of entire words to
                 allow (case-insensive) such as "master" or "dev"
    '''
    # if s.lower in version_strings:
    if allowMore is not None:
        for vPart in allowMore:
            vOpener = vPart.lower()
            if s.lower() == vOpener:
                return True
            elif s.startswith(vOpener) and s[len(vOpener):].isnumeric():
                return True

    startsWithNum = False
    if s[:1] in digits:
        startsWithNum = True

    for c in s:
        if c not in version_chars:
            if (allowLettersAtEnd and startsWithNum):
                if (not c.isalpha()):
                    return False
            else:
                return False
    return True


def is_digits(s):
    '''
    Only numbers, no dots or other symbols.
    '''
    if len(s) < 1:
        raise ValueError("is_digits got an empty string.")
    for c in s:
        if c not in digits:
            # print("{} is not in {}.".format(c, digits))
            return False
    return True


downloading = False


def dl_progress(evt):
    global downloading
    dl_msg_w = 80
    if downloading:
        sys.stderr.write("\r")
    line = "{}".format(evt['loaded']).ljust(dl_msg_w)
    # ^ 2nd param of ljust (,`character`) is optional
    sys.stderr.write(line)
    pass


def dl_done(evt):
    global downloading
    downloading = False
    print("  DONE")


def download(file_path, url, cb_progress=None, cb_done=None,
             chunk_len=16*1024):
    '''
    Download a file in binary mode (based on download from
    LinkManager from blendernightly).
    '''
    response = request.urlopen(url)
    evt = {}
    evt['loaded'] = 0
    # evt['total'] is not implemented (would be from contentlength
    # aka content-length)
    with open(file_path, 'wb') as f:
        while True:
            chunk = response.read(chunk_len)
            if not chunk:
                break
            evt['loaded'] += chunk_len
            if cb_progress is not None:
                cb_progress(evt)
            f.write(chunk)
    if cb_done is not None:
        cb_done(evt)


class PackageInfo:
    '''
    To get a globally unique name based on whether multiVersion or
    multiPackage installs can coexist, use get_coexisting_id(luid,
    multiPackage, multiVersion). See the constructor documentation for
    more info.
    '''
    DELIMITERS = "_- +"
    X64S = ["x64", "64bit", "linux64", "win64", "windows64", "64-bit",
            "x86_64", "amd64"]
    X32S = ["x32", "686", "386", "i386", "i686", "32bit", "32-bit",
            "windows32", "win32", "x86"]
    NOARCHES = ["noarch"]
    ARCHES = X64S + X32S + NOARCHES
    # ^ NOTE: x86_64 is handled manually below since it contains a
    #   delimiter
    LINS = ["linux", "linux64", "linux32"]
    WINS = ["windows", "windows64", "windows32", "win64", "win32"]
    VPARTS = ['master', 'dev', 'prealpha', 'alpha', 'beta', 'rc']
    verbosity = 1

    def __init__(self, src_path, **kwargs):
        '''
        Sequential arguments:
        src_path -- If the constructor parameter is a directory, the
        extension will not be removed.

        Keyword arguments
        arch -- 64bit or 32bit, to match the first element in the tuple
                returned by Python's platform.architecture(). If no
                delimited segment of the filename is in X64S or X32S,
                the arch will be None after the contructor call.

        platform -- uppercase platform such as "Linux" or "Windows"
                    to match the output of Python's platform.system(). If no
                    delimited segment of the filename is in LINS or WINS,
                    the platform will be None after the contructor call.

        casedName -- The casedName is the human-readable name without the
                     version, possibly including uppercase and spaces
                     (generated if None).

        luid -- the name ("locally unique identifier" uniquely identifying
                the program (no version); ready to be used as an icon file
                name; used as a key for the icons dict or casedNames dict
                default: toLUID(casedName)
        version -- You must specify a version if the name has no
                   version. This script should automatically pass along
                   the version such as if the archive but not directory
                   (or directory but not not binary) has the version.
        '''
        print("[PackageInfo __init__] * checking src_path {}..."
              "".format(src_path))
        if PackageInfo.verbosity > 0:
            print("")
            print("Creating PackageInfo...")
        self.metas = ['casedName', 'luid', 'version',
                      'caption', 'platform', 'arch']
        self.casedName = kwargs.get('casedName')
        self.luid = kwargs.get("luid")
        # ^ decided by transforming casedName below if None
        self.version = kwargs.get('version')
        self.platform = None
        self.arch = None
        self.path = src_path
        self.suffix = ""
        is_dir = kwargs.get('is_dir')
        if is_dir is None:
            if not os.path.exists(src_path):
                raise ValueError(
                    "src_path \"{}\" must exist or you must specify the"
                    " is_dir keyword argument for the PackageInfo"
                    " constructor (only if running a test)."
                    "".format(src_path)
                )
            is_dir = os.path.isdir(src_path)
        removeExt = kwargs.get('removeExt')
        if removeExt is None:
            removeExt = not is_dir
        self.fname = os.path.split(self.path)[-1]
        fnamePartial = self.fname
        if removeExt:
            fnamePartial = os.path.splitext(self.fname)[0]
            if fnamePartial.lower().endswith(".tar"):
                fnamePartial = fnamePartial[:-4]
        startChar = 0
        while not fnamePartial[startChar].isalpha():
            startChar += 1
            if startChar >= len(fnamePartial):
                msg = ("Parsing names with no alphabetic"
                       " characters is not possible.")
                raise ValueError(msg)
                # print(msg)
                # break
                # startChar = 0
        fnamePartial = fnamePartial[startChar:]
        self.caption = kwargs.get('caption')
        parts = split_any(fnamePartial, PackageInfo.DELIMITERS,
                          blobs=PackageInfo.ARCHES)
        part1 = None
        part2 = None
        archI = -1
        if PackageInfo.verbosity > 0:
            print("* name without extension: \"{}\""
                  "".format(fnamePartial))
        platformI = -1
        versionI = -1
        if len(parts) < 2:
            # re-split
            tmpParts = fnamePartial.split(".")
            parts, versionI = PackageInfo.unsplit_version(tmpParts)
            print("* split {} into {} len {} (version is at [{}])"
                  "".format(fnamePartial, tmpParts, len(tmpParts),
                            versionI))
        else:
            oldDelimiters = []
            cI = 0
            for i in range(len(parts)):
                cI += len(parts[i])
                if cI < len(fnamePartial):
                    oldDelimiters.append(fnamePartial[cI])
                    cI += 1  # add the delimiter length
                else:
                    oldDelimiters.append("")
                if parts[i][:1].lower() == "v":
                    # Remove v such as "v1.0" to "1.0".
                    if is_digits(parts[i][1:]):
                        parts[i] = parts[i][1:]
                partL = parts[i].lower()
                if partL in PackageInfo.X64S:
                    self.arch = "64bit"
                    archI = i
                    # Always do 64-bit first so that x86_64 is found
                    # before x86.
                elif partL in PackageInfo.X32S:
                    self.arch = "32bit"
                    archI = i
                elif partL == "x86":
                    if (len(parts) > i + 1) and (parts[i+1] == "64"):
                        self.arch = "64bit"
                    else:
                        self.arch = "32bit"
                elif partL in PackageInfo.NOARCHES:
                    self.arch = "noarch"
                if partL in PackageInfo.LINS:
                    self.platform = "Linux"
                    platformI = i
                elif partL in PackageInfo.WINS:
                    self.platform = "Windows"
                    platformI = i
            parts, versionI = PackageInfo.unsplit_version(
                parts,
                oldDelimiters=oldDelimiters
            )
            # ^ still do unsplit_version, because the version may be
            #   multiple parts such as in ['Slic3r', '1.3.1', 'dev']
            del i
        if (len(parts) < 2) and (self.version is None):
            usage()
            raise ValueError("The end of the program name (any of '{}'"
                             " or '.' is not in {} and you didn't"
                             " specify a version such as:\n"
                             " install_any.py {} --version x"
                             "".format(PackageInfo.DELIMITERS,
                                       fnamePartial, src_path))
        if self.version is None:
            # INFO: Any "v" prefix was already removed and multi-part
            #       versions were already un-split into one part
            #       using unsplit_version (in re-split code or the
            #       `else` case).
            if versionI > -1:
                self.version = parts[versionI]
                if True:  # TODO: if PackageInfo.verbosity > 0:
                    print("* using '" + self.version + "' as version")
        else:
            if True:  # TODO: PackageInfo.verbosity > 0:
                print("* using specified '{}' as version"
                      "".format(self.version))

        nameEnder = -1
        if versionI > -1:
            nameEnder = versionI
            if PackageInfo.verbosity > 0:
                print("* ending name at version \"{}\""
                      "".format(parts[versionI]))
        if platformI > -1:
            if nameEnder < 0 or (platformI < nameEnder):
                nameEnder = platformI
        if versionI > -1:
            if (nameEnder < 0) or (versionI < nameEnder):
                nameEnder = versionI

        if self.casedName is None:
            self.casedName = parts[0]
            if nameEnder > 0:
                self.casedName = " ".join(parts[:nameEnder])
            else:
                print("WARNING: there is no name ender such as arch,"
                      " platform or version, so the first part will be"
                      " the name: \"{}\"."
                      "".format(self.casedName))
            if PackageInfo.verbosity > 0:
                print("* using '{}' as human-readable name"
                      " before adding version".format(self.casedName))
        else:
            if PackageInfo.verbosity > 0:
                print("* using specified name: {}".format(self.casedName))

        annotation = get_annotation(src_path)
        if annotation is not None:
            self.suffix = "-" + annotation

        if self.luid is None:
            self.luid = toLUID(self.casedName)

        if kwargs.get('casedName') is None:
            # only use a build-in cased name if not specified manually
            # (a casedName may have been generated above, but the
            # following can't be completed until LUID is generated if
            # not present)
            tryCasedName = casedNames.get(self.luid)
            if tryCasedName is None:
                if self.casedName.lower() == self.casedName:
                    if PackageInfo.verbosity > 1:
                        print("* The program \"{}\" is not in the"
                              " casedNames dict and is all lowercase,"
                              " so the caption \"{}\" will become"
                              " title case (parts: {})."
                              "".format(self.casedName, fnamePartial,
                                        parts))
                    self.casedName = self.casedName.title()
                # else use self.casedName since not all lower.
            else:
                self.casedName = tryCasedName
                if PackageInfo.verbosity > 1:
                    print("* detected '{}' so changed case to '{}'"
                          "".format(self.luid, tryCasedName))

        if PackageInfo.verbosity > 0:
            print("* using \"{}\" as icon filename prefix (luid)"
                  " (The version will be added later if multiVersion)"
                  "".format(self.luid))
        if self.caption is None:
            if versionI > -1:
                self.caption = self.casedName + " " + parts[versionI]
            else:
                print("WARNING: the caption will not have a version"
                      " since no version was detected in {}"
                      "".format(parts))
                self.caption = self.casedName
            if annotation is not None:
                suffix = " (" + annotation + ")"
                if PackageInfo.verbosity > 1:
                    print("* appending \" ({})\" to caption..."
                          "".format(annotation))
                if not self.caption.endswith(suffix):
                    self.caption += suffix
                    print("  OK")
                else:
                    if PackageInfo.verbosity > 0:
                        print("  - skipped: it already ends with \"{}\""
                              "".format(suffix))

    # @classmethod
    # def unsplitArch(cls, tmpParts):


    @classmethod
    def unsplit_version(cls, tmpParts, TwoOnly=False,
                        oldDelimiters=None):
        '''
        Get a ([], int) tuple of (parts, versionI) where versionI is the
        index of the version and parts is the same list except where the
        version is in one element.

        Example: ['blender','2','9','3'] becomes
                 (['blender', '2.9.3'], 1)

        Sequential arguments:
        cls -- Class (Don't specify this--Call
               PackageInfo.unsplit_version to prepend the class)
        TwoOnly -- Combine everything before the version and after the
                   start of the version.
        oldDelimiters -- Add old delimiters back when un-splitting.
        '''
        fn = 'unsplit_version'
        firstNumI = -1
        lastNumI = -1
        letteredI = -1
        versionI = -1
        parts = tmpParts
        if PackageInfo.verbosity > 1:
            print("[unsplit_version] tmpParts={}".format(tmpParts))
        if not hasattr(tmpParts, 'append'):
            raise ValueError("tmpParts must be a list but is {}"
                             "".format(tmpParts))
        for i in range(len(tmpParts)):
            if tmpParts[i][:1].lower() == "v":
                # Remove v such as "v1" to "1".
                if is_version(tmpParts[i][1:], True,
                              PackageInfo.VPARTS):
                    tmpParts[i] = tmpParts[i][1:]
                    if PackageInfo.verbosity > 1:
                        print("  * unsplit_version removed a 'v'")
                else:
                    if PackageInfo.verbosity > 1:
                        print("  * unsplit_version kept a 'v'")
            tmpPart = tmpParts[i]
            if is_version(tmpPart, False, PackageInfo.VPARTS):
                if PackageInfo.verbosity > 1:
                    print("  * {} ({}) is a version part."
                          "".format(tmpPart, i))
                if firstNumI < 0:
                    firstNumI = i
                lastNumI = i
            elif is_version(tmpPart, True, PackageInfo.VPARTS):
                if PackageInfo.verbosity > 1:
                    print("  * {} is a lettered version part."
                          "".format(tmpPart))
                if letteredI < 0:
                    letteredI = firstNumI
                if firstNumI < 0:
                    firstNumI = i
                lastNumI = i
            else:
                if PackageInfo.verbosity > 1:
                    print("  * {} ({}) is not a version part."
                          "".format(tmpPart, i))
                if firstNumI > -1:
                    # end the version parts
                    break
        if firstNumI > -1:
            if letteredI > -1:
                if lastNumI > letteredI:
                    print(
                        "  [{}] WARNING: version numbers {} appear"
                        " after the alphabetical suffix {} in {}."
                        "".format(fn, tmpParts[lastNumI],
                                  tmpParts[letteredI],
                                  tmpParts)
                    )
            if firstNumI == 0:
                parts = ["", ".".join(tmpParts)]
                print("  [{}] WARNING: No name was detected in {}"
                      "".format(fn, tmpParts))
            else:
                firstNameI = 0
                lastNameI = firstNumI - 1
                if TwoOnly:
                    parts = [
                        ".".join(tmpParts[firstNameI:lastNameI+1]),
                        ".".join(tmpParts[firstNumI:lastNumI+1]),
                    ]
                    versionI = 1
                    print("  [{}] TwoOnly is enabled, so version part"
                          " is {}".format(fn, parts[versionI]))
                else:
                    if oldDelimiters is not None:
                        parts = tmpParts[:firstNumI]
                        i = len(parts)
                        print("  [{}] firstNumI={}, lastNumI={}"
                              "".format(fn, firstNumI, lastNumI))
                        joined = ""
                        while i <= lastNumI:
                            oldDelimiter = oldDelimiters[i]
                            # ^ last delimiter is ""
                            # print("  [{}]re-adding '{}'"
                            #       "".format(fn, oldDelimiter))
                            if i == lastNumI:
                                oldDelimiter = ""
                                # ^ Don't add the ending delimiter.
                            joined += tmpParts[i] + oldDelimiter
                            i += 1
                        parts.append(joined)
                        parts += tmpParts[lastNumI+1:]
                    else:
                        parts = (
                            tmpParts[:firstNumI]
                            + [".".join(tmpParts[firstNumI:lastNumI+1])]
                            + tmpParts[lastNumI+1:]
                        )
                    versionI = firstNumI
            if PackageInfo.verbosity > 0:
                print("  [{}] changed parts to {}".format(fn, parts))
            # "since no "
            # "".format(parts, PackageInfo.DELIMITERS))
        else:
            print("  [{}] There are no version strings in {}"
                  "".format(fn, tmpParts))
        return parts, versionI

    def get_bits(self):
        '''
        Get 32 or 64 (integer) or None if unknown.
        '''
        if self.arch is None:
            return None
        if self.arch in PackageInfo.X64S:
            return 64
        elif self.arch in PackageInfo.X32S:
            return 32
        return None

    def toDict(self):
        ret = {}
        for k in self.metas:
            ret[k] = self.__dict__[k]
        return ret

    def get_coexisting_id(self, multiPackage, multiVersion):
        '''
        To allow multiple versions, append "-"+pkginfo.version to the
        name when naming the desktop file or for other uses requiring
        separating multiple versions. The output will always be
        lowercase.
        '''
        ret = self.luid
        if multiPackage:
            ret += self.suffix
        if multiVersion:
            ret += "-" + self.version
        return ret

    def toList(self):
        return [self.__dict__[k] for k in self.metas]

    def __str__(self):
        return str(self.toDict())


def dir_is_empty(folder_path):
    count = 0
    sub_names = os.listdir(folder_path)
    for sub_name in sub_names:
        count += 1
    return count < 1


profile = os.environ.get("HOME")
if profile is None:
    profile = os.environ.get("USERPROFILE")
    AppDatas = os.path.join(profile, "AppData", "Local")
    if not os.path.isdir(AppDatas):
        raise RuntimeError("USERPROFILE {} is used (since HOME is"
                           "not defined), but there is no {}"
                           "".format(profile, AppDatas))
    myAppData = os.path.join(AppDatas, "install_any")
else:
    AppDatas = os.path.join(profile, ".config")
    myAppData = os.path.join(AppDatas, "install_any")
    local_path = os.path.join(profile, ".local")
    share_path = os.path.join(local_path, "share")
    icons_path = os.path.join(share_path, "pixmaps")
if not os.path.isdir(myAppData):
    os.makedirs(myAppData)
logPath = os.path.join(myAppData, "install_any.log")
lib64 = os.path.join(local_path, "lib64")
lib = os.path.join(local_path, "lib")
fm = None


def logLn(line, path=logPath):
    print("[logged]:" + line)
    global fm
    if fm is None:
        fm = 'w'
        if os.path.isfile(path):
            fm = 'a'
    with open(path, 'a') as outs:
        outs.write(line + "\n")
        fm = 'a'


def install_program_in_place(src_path, **kwargs):
    version = kwargs.get("version")
    if version is not None:
        print("- version: {}".format(version))
    casedName = kwargs.get("casedName")
    caption = kwargs.get("caption")
    luid = kwargs.get("luid")
    do_uninstall = kwargs.get("do_uninstall")
    if do_uninstall is None:
        do_uninstall = False
    enable_reinstall = kwargs.get("enable_reinstall")
    if enable_reinstall is None:
        enable_reinstall = False
    detect_program_parent = kwargs.get("detect_program_parent")
    if detect_program_parent is None:
        detect_program_parent = False
    multiVersion = kwargs.get("multiVersion")
    icon_path = kwargs.get("icon_path")
    move_what = kwargs.get("move_what")
    pull_back = kwargs.get("pull_back")
    """Install binary program src_path

    Keyword arguments:
    casedName --
    If casedName is not specified, the name and version will be
    calculated from either the filename at src_path or the path's
    parent directory's name.
    Example:
    src_path = \
    ../Downloads/blender-2.79-e045fe53f1b0-linux-glibc217-x86_64/blender
    (In this case, this function will extract the name and version from
    blender-2.79-e045fe53f1b0-linux-glibc217-x86_64 since it has more
    delimiters than the filename "blender")

    move_what -- Only set this to 'file' if src_path is an AppImage or
    other self-contained binary file. Otherwise you may set it to
    'directory'. The file or directory will be moved to ~/.local/lib64/
    (or whatever programs directory is detected as a parent of the
    directory if detect_program_parent is True [automaticaly True by
    calling itself in the case of deb]).
    move_what='file' example:
    If name is not specified, the name and version will be calculated
    from either the filename at src_path or the path's parent
    directory's name.
    Example:
    src_path=(
    "../Downloads/"
    "FreeCAD_0.18-16131-Linux-Conda_Py3Qt5_glibc2.12-x86_64.AppImage"
    )
    (In this case, this function will extract the name and version from
    FreeCAD_0.18-16131-Linux-Conda_Py3Qt5_glibc2.12-x86_64.AppImage)

    multiVersion -- Allow the version to be in the installed directory
                    name and the icon name so that multiple versions of
                    the same program (with same luid such as "blender"
                    or "ultimaker.cura") can be installed at once.
                    If None, will be set to True if "blender" is the
                    luid.

                    Even if false, If the file is an appimage, it can
                    coexist with other non-appimage installs, since the
                    non- appimage install will be a directory or
                    non-appimage binary and since -appimage will be
                    appended to the icon filename.

    luid -- This is the unique program name without the version, with
            dots instead of spaces and all lowercase.
            It is detected automatically from the file or directory name
            if None.
    """
    enable_force_script = False
    dst_programs = lib64  # changed if deb has a different programs dir
    if '32' in platform.architecture()[0]:
        dst_programs = lib
    dirname = None
    dirpath = None
    ex_tmp = None
    suffix = ""
    new_tmp = None
    verb = "uninstall" if do_uninstall else "install"
    is_dir = None
    pull_back = None
    if src_path.lower().endswith(".appimage"):
        is_dir = False
        # ^ ONLY manually set this for files that won't be
        # extracted!
        pull_back = True
        if not os.path.exists(src_path):
            print("* attempting to recover to \"{}\"..."
                  "".format(src_path))

    ending = ".deb"
    if src_path.lower()[-(len(ending)):] == ending:
        logLn("* switching to --reinstall mode automatically...")
        if enable_reinstall:
            logLn("  * already done")
        else:
            enable_reinstall = True
            logLn("  * OK")
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
            raise RuntimeError("{} did not complete.".format(verb))


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
                elif sub_name == "signal-desktop-beta":
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

        pkginfo = PackageInfo(
            src_path,
            casedName=casedName,
            version=version,
            caption=caption,
        )
        # ^ Do NOT specify is_dir (The program must exist since it was
        #   extracted from a package)
        if casedName is None:
            casedName = pkginfo.casedName
        if version is None:
            version = pkginfo.version
        if caption is None:
            caption = pkginfo.caption
        if luid is None:
            luid = pkginfo.luid
        suffix = pkginfo.suffix
        # ^ Get the info now, because the extracted directory name will
        #   not contain the version.
        print("* forwarding info for recursion: {} luid:{}"
              "".format([casedName, version, caption], luid))
        print("")
        print("")
        result = install_program_in_place(
            binary_path,
            caption=program+" (deb)",
            casedName=casedName,
            version=version,
            move_what='directory',
            do_uninstall=do_uninstall,
            luid=luid,
            icon_path=icon_path,
            enable_reinstall=enable_reinstall,
            detect_program_parent=True,
            pull_back=pull_back,
        )
        shutil.rmtree(next_temp)
        print("* removed '{}'".format(next_temp))
        return result
        # ^ return archive within extracted archive
        # end if deb (containing tar.xz)

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
                pkginfo = PackageInfo(
                    src_path,
                    casedName=casedName,
                    version=version,
                    caption=caption,
                )
                # ^ Do NOT specify is_dir
                if casedName is None:
                    casedName = pkginfo.casedName
                if version is None:
                    version = pkginfo.version
                    print("* version from archive name is: {}"
                          "".format(version))
                if caption is None:
                    caption = pkginfo.caption
                if luid is None:
                    luid = pkginfo.luid
                suffix = pkginfo.suffix
                # ^ Get the info now, because the extracted directory
                #   name may not contain the version.

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
        dirpath = src_path
        print("* trying to detect binary...")
        src_name = os.path.split(src_path)[-1]
        only_name = src_name.strip("-0123456789. ")
        try_name = src_name.split("-")[0]
        try_names = []
        name_partial = src_name.split("-")[0]
        try_names.append(name_partial + ".sh")
        # ^ sh takes priority in case environment vars are necessary
        try_names.append(name_partial)
        if len(src_name.split("-")) > 1:
            try_names.append(src_name.split("-")[1] + ".sh")
            # ^ such as studio.sh for android-studio
        print("  src_name: {}".format(src_name))
        print("  only_name: {}".format(only_name))
        print("  name_partial: {}".format(name_partial))
        got_path = None
        try_paths = []
        for try_name in try_names:
            try_paths.append(os.path.join(src_path, "bin", try_name))
            try_paths.append(os.path.join(src_path, try_name))
        for try_path in try_paths:
            if os.path.isfile(try_path):
                got_path = try_path
                break

        if got_path is not None:
            print("* detected binary: '{}'".format(got_path))
            src_path = got_path
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
                for i in range(len(scripts)):
                    script = scripts[i]
                    if script.startswith(only_name):
                        good_indices.append(i)
                    elif script == "monero-wallet-gui":
                        good_indices.append(i)
                    else:
                        bad_indices.append(i)
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
    if dirpath is None:
        dirpath = os.path.split(src_path)[-2]
    else:
        print("* using detected \"{}\" for dirpath instead of \"{}\""
              "".format(dirpath, os.path.split(src_path)[-2]))
        filename = src_path[len(dirpath)+1:]  # 1 for slash
        # INFO: The filename is a relative path (not merely a name) in
        #       this case.
        print("  * therefore the filename is \"{}\""
              "".format(filename))
        if move_what == 'file':
            raise RuntimeError("A single file install is impossible"
                               " since there is a directory.")
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
    # luid = None

    if (casedName is None) or (version is None):
        # try_names = [filename, dirname]
        try_sources = [src_path]
        if not src_path.lower().endswith(".appimage"):
            try_sources.append(dirpath)
        pkg = None
        pkgs = []
        for try_source in try_sources:
            print("[install_program_in_place] * try_source {}"
                  "".format(try_source))
            thisPkg = PackageInfo(
                try_source,
                casedName=casedName,
                version=version,
                caption=caption,
                is_dir=is_dir,
            )
            pkgs.append(thisPkg)
        for thisPkg in pkgs:
            if pkg is None:
                pkg = thisPkg
            if thisPkg.version is not None:
                if version is None:
                    version = pkg.version
            if thisPkg.casedName is not None:
                if casedName is None:
                    casedName = pkg.casedName
                elif len(casedName) < len(thisPkg.casedName):
                    print("WARNING: the previously collected name"
                          " \"{}\ is shorter than the detected name"
                          " \"{}\" (tries: {})".format(pkgs))
                    casedName = pkg.casedName
                    if luid is None:
                        if thisPkg.luid is None:
                            print("WARNING: converting casedName to"
                                  " LUID in install_program_in_place")
                            luid = toLUID(pkg.casedName)
            if len(thisPkg.suffix) > 0:
                suffix = thisPkg.suffix
            if thisPkg.luid is not None:
                if luid is None:
                    luid = pkg.luid
            if thisPkg.caption is not None:
                if caption is None:
                    caption = thisPkg.caption
            if thisPkg.luid is not None:
                if luid is None:
                    luid = thisPkg.luid
    else:
        print("* The casedName was set to \"{}\"".format(casedName))
        print("* The version was set to \"{}\"".format(version))
        print("* The luid was set to \"{}\"".format(luid))
        print("* The icon filename suffix was set to \"{}\""
              "".format(suffix))

    applications = os.path.join(share_path, "applications")
    sc_path = None
    sc_name = None
    old_sc_name = None
    if luid == "blender":
        if multiVersion is None:
            multiVersion = True
            print("* enabling multiVersion since using Blender")
        if version is not None:
            sc_name = "blender{}-{}".format(suffix, version)
            if do_uninstall:
                old_sc_name = "org.blender-{}".format(version)
        else:
            if multiVersion is True:
                print("  but the version was not detected!")
            sc_name = "blender" + suffix
            if do_uninstall:
                old_sc_name = "org.blender"
        print("* using {} as shortcut name".format(sc_name))
    elif version is not None:
        if multiVersion is True:
            sc_name = "{}{}-{}".format(luid, suffix, version)
        else:
            sc_name = "{}{}".format(luid, suffix)
    else:
        print("* no version is detected in {}".format(src_path))
        sc_name = "{}".format(luid)

    sc_name += ".desktop"
    sc_path = os.path.join(applications, sc_name)
    old_sc_path = None
    if old_sc_name is not None:
        old_sc_name += ".desktop"
        print("* WARNING: legacy name before git 2021-02-25) name"
              " was {} as shortcut name".format(sc_name))
        old_sc_path = os.path.join(applications, old_sc_name)
    if luid is None:
        print("WARNING: luid was never set, so setting to:")
        luid = toLUID(casedName)
        print("  " + luid)
    try_icon = icons.get(luid)
    try_icon_url = iconLinks.get(luid)
    print("* checking for known icon related to '{}'..."
          "".format(luid))

    if try_icon is not None:
        luid = try_icon
        print("  * using known icon luid '{}'".format(luid))
    if caption is None:
        luid = try_icon
        print("  * using unknown icon luid '{}'".format(luid))
        caption = luid
        if version is not None:
            caption += " " + version
        caption = caption[:1].upper() + caption[1:].lower()
        print("* using '" + caption + "' as caption (from luid)")
    logLn("luid=\"{}\"".format(luid))
    if icon_path is None:
        if try_icon_url is not None:
            icon_name = try_icon_url.split('/')[-1]
            icon_path = os.path.join(icons_path, icon_name)
            if not do_uninstall:
                if not os.path.isdir(icons_path):
                    os.makedirs(icons_path)
                if os.path.isfile(icon_path):
                    if os.stat(icon_path).st_size == 0:
                        print("* removing bad 0-size icon \"{}\""
                              "".format(icon_path))
                        os.remove(icon_path)
                if not os.path.isfile(icon_path):
                    print("* downloading \"{}\" to \"{}\"..."
                          "".format(try_icon_url, icon_path))
                    download(icon_path, try_icon_url,
                             cb_progress=dl_progress,
                             cb_done=dl_done)
                else:
                    print("* \"{}\" already exists (skipping download)"
                          "".format(icon_path))
    print("    (The version will be added later if multiVersion)")
    path = src_path
    # dst_programs = os.path.join(os.environ.get("HOME"), ".config")
    dst_dirpath = os.path.join(dst_programs, dirname)
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
                    logLn("install_file:{}".format(dst_dirpath))
                else:
                    print("The file is already at '{}'.".format(path))
                    logLn("#install_file:{}".format(dst_dirpath))
            else:
                if os.path.isfile(path):
                    if not os.path.isfile(src_path) and pull_back:
                        print("mv \"{}\" \"{}\"".format(path, src_path))
                        shutil.move(path, src_path)
                        logLn("uninstall_file:{}\n"
                              "recovered_to:{}"
                              "".format(path, src_path))
                        if src_path == path:
                            print("The source path"
                                  " \"{}\" was moved to \"{}\"."
                                  "".format(path, src_path))
                    else:
                        print("rm \"{}\"".format(path))
                        os.remove(path)
                        path("uninstall_dir:{}\n".format(dst_dirpath))
                        if src_path == path:
                            print("The source path"
                                  " '{}' is removed.".format(path))
                else:
                    print("'{}' does not exist, so there is nothing to"
                          " {}.".format(path, verb))

    elif move_what == 'directory':
        if do_uninstall:
            if os.path.isdir(dst_dirpath):
                shutil.rmtree(dst_dirpath)
            else:
                print("There is no '{}'.".format(dst_dirpath))
            logLn("uninstall_dir:{}".format(dst_dirpath))
        else:
            print("mv '{}' '{}'".format(dirpath, dst_dirpath))
            if os.path.isdir(dst_dirpath):
                if enable_reinstall:
                    shutil.rmtree(dst_dirpath)
                else:
                    logLn("ERROR: '{}' already exists. Use the"
                          " --reinstall option to ERASE the"
                          " directory.".format(dst_dirpath))
                    return False
            shutil.move(dirpath, dst_dirpath)
            path = os.path.join(dst_dirpath, filename)
            logLn("install_move_dir:{}".format(dst_dirpath))


    if not do_uninstall:
        sys.stderr.write("* marking \"{}\" as executable..."
                         "".format(path))
        os.chmod(path, stat.S_IRWXU | stat.S_IXGRP | stat.S_IRGRP
                       | stat.S_IROTH | stat.S_IXOTH)
        sys.stderr.write("OK\n")
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
        icon_path = luid

    shortcut_data = shortcut_data_template.format(Exec=path,
                                                  Name=caption,
                                                  Icon=icon_path)

    my_dir = os.path.dirname(os.path.realpath(__file__))
    meta_dir = os.path.join(my_dir, "shortcut-metadata")
    meta_path = os.path.join(meta_dir, "{}.txt".format(luid))

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
    if old_sc_path is not None:
        if os.path.isfile(old_sc_path):
            u_cmd_parts = [desktop_installer, "uninstall", old_sc_path]
            if os.path.isfile(sc_path):
                logLn("WARNING: You'll have to run uninstall again"
                      " because both shortcut path \"{}\" and legacy"
                      " shortcut path \"{}\" are present."
                      "".format(sc_path, old_sc_path))

    if do_uninstall:
        logLn("uninstall_shortcut:{}".format(sc_path))
        if os.path.isfile(sc_path):
            print(u_cmd_parts)
            install_proc = subprocess.run(u_cmd_parts)
            if install_proc.returncode != 0:
                if os.path.isfile(sc_path):
                    print("rm \"{}\"".format(sc_path))
                    os.remove(sc_path)
                else:
                    print("{} failed but \"{}\" was not present so no"
                          " steps seem to be necessary."
                          "".format(" ".join(u_cmd_parts)))
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
            # print("sp_run's returned process {} has {}"
            #       "".format(install_proc, dir(install_proc)))
            if install_proc.returncode != 0:
                inst_msg = "FAILED"
            if os.path.isfile(sc_path):
                os.chmod(sc_path,
                         (stat.S_IROTH | stat.S_IREAD | stat.S_IRGRP
                          | stat.S_IWUSR))
                print("* installing '{}'...{}".format(sc_path,
                                                      inst_msg))
                sys.stderr.write("* marking \"{}\" as executable..."
                                 "".format(path))
                os.chmod(path, stat.S_IRWXU | stat.S_IXGRP
                         | stat.S_IRGRP
                         | stat.S_IROTH | stat.S_IXOTH)
                sys.stderr.write("OK\n")

            else:
                print("* installing '{}'...".format(sc_name,
                                                    inst_msg))
            print("  Name={}".format(caption))
            print("  Exec={}".format(path))
            logLn("install_shortcut:{}".format(path))
            print("  Icon={}".format(icon_path))
            # print("")
            # print("You may need to reload the application menu, such"
            # #     " as via one of the following commands:")
            # print("  ")
            # or xdg-desktop-menu install mycompany-myapp.desktop
        else:
            logLn("install_shortcut_failed:{}".format(path))
        return ok
    return False

if __name__ == "__main__":
    print("")
    caption = None
    src_path = None
    if len(sys.argv) < 2:
        usage()
        logLn("You must specify a directory or binary file.")
        print("")
        print("")
        exit(1)
    do_uninstall = False
    enable_reinstall = False
    move_what = None
    multiVersion = None
    valueParams = {}
    valueParamsKey = None
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg[:2] == "--":
            if arg == "--uninstall":
                do_uninstall = True
            elif arg == "--move":
                move_what = 'any'
            elif arg == "--version":
                valueParamsKey = "version"
            elif arg == "--reinstall":
                enable_reinstall = True
            elif arg == "--multi-version":
                multiVersion = True
            elif arg == "--help":
                usage()
                exit(0)
            else:
                print("ERROR: '{}' is not a valid option.".format(arg))
                exit(1)
        elif valueParamsKey is not None:
            valueParams[valueParamsKey] = arg
            valueParamsKey = None
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
    version = valueParams.get('version')
    install_program_in_place(
        src_path,
        caption=caption,
        move_what=move_what,
        do_uninstall=do_uninstall,
        enable_reinstall=enable_reinstall,
        multiVersion=multiVersion,
        version=version,
    )
