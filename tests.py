#!/usr/bin/env python
#from utilities.install_any import PackageInfo
import sys
import os

def toPythonLiteral(v):
    '''
    [copied from pycodetools.parsing by author]
    '''
    if v is None:
        return None
    elif v is False:
        return "False"
    elif v is True:
        return "True"
    elif ((type(v) == int) or (type(v) == float)):
        return str(v)
    elif (type(v) == tuple) or (type(v) == list):
        enclosures = '()'
        if type(v) == list:
            enclosures = '[]'
        s = enclosures[0]
        for val in v:
            s += toPythonLiteral(val) + ", "
            # ^ Ending with an extra comma has no effect on length.
        s += enclosures[1]
        return s
    return "'{}'".format(
        v.replace("'", "\\'").replace("\r", "\\r").replace("\n", "\\n")
    )


def assertEqual(v1, v2, tbs=None):
    '''
    [copied from pycodetools.parsing by author]
    Show the values if they differ before the assertion error stops the
    program.

    Keyword arguments:
    tbs -- traceback string (either caller or some sort of message to
           show to describe what data produced the arguments if they're
           derived from something else)
    '''
    if ((v1 is True) or (v2 is True) or (v1 is False) or (v2 is False)
            or (v1 is None) or (v2 is None)):
        if v1 is not v2:
            print("")
            print("{} is not {}".format(toPythonLiteral(v1),
                                        toPythonLiteral(v2)))
            if tbs is not None:
                print("for {}".format(tbs))
        assert(v1 is v2)
    else:
        if v1 != v2:
            print("")
            print("{} != {}".format(toPythonLiteral(v1),
                                    toPythonLiteral(v2)))
            if tbs is not None:
                print("for {}".format(tbs))
        assert(v1 == v2)


def assertAllEqual(list1, list2, tbs=None):
    '''
    [copied from pycodetools.parsing by author]
    '''
    if len(list1) != len(list2):
        print("The lists are not the same length: list1={}"
              " and list2={}".format(list1, list2))
        assertEqual(len(list1), len(list2))
    for i in range(len(list1)):
        assertEqual(list1[i], list2[i], tbs=tbs)


sys.path.append("utilities")
from install_any import PackageInfo

from install_any import find_all_any_ci

from install_any import tests

print()
print()
print()
print("BEGIN install_any.py self tests")
tests()
print("END install_any.py self tests")
print()
print()
print()

PackageInfo.verbosity = 2

fn = "blender-2.79b-linux-glibc219-x86_64"
chunks =['linux', 'X86_64']  # intentionally different case for CI test
results = find_all_any_ci(
    fn,
    chunks,
)
assertAllEqual(results, [(14, 'linux'), (29, 'X86_64')],
               tbs="{} in {}".format(chunks, fn))
print("* find_all_any_ci test...OK ({} at {} in {})"
      "".format(chunks, results, fn))

pkg = PackageInfo("flashprint_4.6.2_amd64.deb", is_dir=False)
assertEqual(pkg.luid, "flashprint")
assertEqual(pkg.luid+pkg.suffix, "flashprint-deb")
assertEqual(pkg.casedName, "FlashPrint")
assertEqual(pkg.caption, "FlashPrint 4.6.2 (deb)")

pkg = PackageInfo("FlashPrint-4.5.1.deb", is_dir=False)
assertEqual(pkg.luid, "flashprint")
assertEqual(pkg.luid+pkg.suffix, "flashprint-deb")
assertEqual(pkg.casedName, "FlashPrint")
assertEqual(pkg.caption, "FlashPrint 4.5.1 (deb)")

tests_dir = "tests"
test1_dir = os.path.join(tests_dir, "someprogram-1.0")
src_path = test1_dir
pkg = PackageInfo(src_path)
assertEqual(pkg.luid, "someprogram")
assertEqual(pkg.version, "1.0")

src_path = "blender-2.79b-linux-glibc219-x86_64"
pkg = PackageInfo(src_path, is_dir=True)
assertEqual(pkg.luid, "blender")
assertEqual(pkg.caption, "Blender 2.79b")
assertEqual(pkg.arch, "64bit")

src_path = os.path.join(tests_dir, "some_program-1.0.0.dummy")
pkg = PackageInfo(src_path)
assertEqual(pkg.caption, "Some Program 1.0.0")
assertEqual(pkg.casedName, "Some Program")

src_path = "blender-2.79b-linux-glibc219-x86"
pkg = PackageInfo(src_path, is_dir=True)
assertEqual(pkg.caption, "Blender 2.79b")
assertEqual(pkg.arch, "32bit")

src_path = \
    "FreeCAD_0.18-16131-Linux-Conda_Py3Qt5_glibc2.12-x86_64.AppImage"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.caption, "FreeCAD 0.18-16131 (AppImage)")
assertEqual(pkg.arch, "64bit")
assertEqual(pkg.platform, "Linux")

src_path = "Mirage-v0.6.4-x86_64.AppImage"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.caption, "Mirage 0.6.4 (AppImage)")
assertEqual(pkg.arch, "64bit")

src_path = "Slic3r-1.3.1-dev-2ef957d-x86_64.AppImage"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.caption, "Slic3r 1.3.1-dev-2ef957d (AppImage)")
assertEqual(pkg.arch, "64bit")

src_path = "Slic3r-master-latest.AppImage"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.caption, "Slic3r master (AppImage)")
assertEqual(pkg.version, "master")

src_path = "Ultimaker_Cura-4.8.0.AppImage"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.caption, "Ultimaker Cura 4.8.0 (AppImage)")
assertEqual(pkg.luid, "ultimaker.cura")

src_path = "4.9_20210511_Ultimaker_Cura-4.9.1.AppImage"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.caption, "Ultimaker Cura 4.9.1 (AppImage)")
assertEqual(pkg.luid, "ultimaker.cura")

found = False
try:
    src_path = "4.9_20210511-4.9.1.AppImage"
    pkg = PackageInfo(src_path, is_dir=False)
except ValueError as ex:
    if "no alphabetic" in str(ex):
        found = True
    else:
        raise ex
if not found:
    raise RuntimeError("The program should have detected a filename (not including extension) with no alphabetic characters as bad (See code near `startChar` in install_any.py).")

src_path = "blender-2.49b-linux-glibc236-py26-x86_64.tar.bz2"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.caption, "Blender 2.49b")
assertEqual(pkg.arch, "64bit")

src_path = "PrusaSlicer-2.3.0+linux-x64-202101111322.AppImage"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.platform, "Linux")
assertEqual(pkg.luid, "prusaslicer")
assertEqual(pkg.caption, "PrusaSlicer 2.3.0 (AppImage)")
assertEqual(pkg.version, "2.3.0")
assertEqual(pkg.arch, "64bit")

PackageInfo.verbosity = 2
src_path = "mfcl2740dwlpr-3.2.0-1.i386.rpm"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.casedName, "Mfcl2740Dwlpr")
assertEqual(pkg.luid, "mfcl2740dwlpr")
# assertEqual(pkg.caption, "Mfcl2740Dwlpr 3.2.0-1.i386")
assertEqual(pkg.caption, "Mfcl2740Dwlpr 3.2.0-1")
assertEqual(pkg.arch, "32bit")
# ^ i386 becomes "32bit" (see PackageInfo.X32S)

src_path = "Meshroom-2019.2.0-linux.tar.gz"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.casedName, "Meshroom")
assertEqual(pkg.platform, "Linux")
assertEqual(pkg.luid, "meshroom")
assertEqual(pkg.caption, "Meshroom 2019.2.0")

src_path = "brscan-skey-0.2.4-1.x86_64.rpm"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.casedName, "Brscan Skey")
assertEqual(pkg.luid, "brscan.skey")
assertEqual(pkg.caption, "Brscan Skey 0.2.4-1")
assertEqual(pkg.arch, "64bit")
# ^ x86_64 becomes "64bit" (see PackageInfo.X64S)

src_path = "tsetup.1.8.2.tar.xz"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.casedName, "Tsetup")
assertEqual(pkg.luid, "tsetup")
assertEqual(pkg.caption, "Tsetup 1.8.2")
assertEqual(pkg.version, "1.8.2")

src_path = "DAIN_APP Alpha 0.41.rar"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.casedName, "DAIN APP")
assertEqual(pkg.luid, "dain.app")
assertEqual(pkg.caption, "DAIN APP Alpha 0.41")
assertEqual(pkg.version, "Alpha 0.41")

src_path = "duplicati-2.0.4.5-2.0.4.5_beta_20181128.noarch.rpm"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.casedName, "Duplicati")
assertEqual(pkg.luid, "duplicati")
# assertEqual(pkg.caption, "Duplicati 2.0.4.5-2.0.4.5")
# assertEqual(pkg.caption, "Duplicati 2.0.4.5-2.0.4.5 beta")
# ^ TODO: add BETA
# assertEqual(pkg.caption, "Duplicati 2.0.4.5-2.0.4.5_beta_20181128.noarch")
assertEqual(pkg.caption, "Duplicati 2.0.4.5-2.0.4.5_beta_20181128")
assertEqual(pkg.arch, "noarch")
print("{}:\n  {}".format(src_path, pkg))

src_path = "monero-gui-linux-x64-v0.17.1.9.tar.bz2"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.casedName, "Monero Gui")
assertEqual(pkg.platform, "Linux")
assertEqual(pkg.luid, "monero.gui")
assertEqual(pkg.caption, "Monero Gui 0.17.1.9")
assertEqual(pkg.version, "0.17.1.9")
assertEqual(pkg.arch, "64bit")

# src_path = "org.gimp.GIMP.flatpakref"
# ^ not relevant, but the resulting casedName is "Org".

fileNames = [
]

dirNames = [
]

src_path = "bash2py-3.6"
pkg = PackageInfo(src_path, is_dir=True)
assertEqual(pkg.casedName, "Bash2Py")
assertEqual(pkg.luid, "bash2py")
assertEqual(pkg.caption, "Bash2Py 3.6")
assertEqual(pkg.version, "3.6")

for fname in fileNames:
    print("")
    pkg = PackageInfo(fname, is_dir=False)
    print("{}:\n  {}".format(fname, pkg))

for fname in dirNames:
    print("")
    pkg = PackageInfo(fname, is_dir=True)
    print("{}:\n  {}".format(fname, pkg))

print("")
print("All tests passed.")
print("")
