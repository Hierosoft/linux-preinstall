#!/usr/bin/env python
#from utilities.install_any import PackageInfo
import sys
import os

def toPythonLiteral(v):
    if v is None:
        return None
    elif v is False:
        return "False"
    elif v is True:
        return "True"
    elif ((type(v) == int) or (type(v) == float)):
        return str(v)
    return "'{}'".format(
        v.replace("'", "\\'").replace("\r", "\\r").replace("\n", "\\n")
    )

def assertEqual(v1, v2):
    '''
    Show the values if they differ before the assertion error stops the
    program.
    '''
    if ((v1 is True) or (v2 is True) or (v1 is False) or (v2 is False)
            or (v1 is None) or (v2 is None)):
        if v1 is not v2:
            print("")
            print("{} is not {}".format(toPythonLiteral(v1),
                                        toPythonLiteral(v2)))
        assert(v1 is v2)
    else:
        if v1 != v2:
            print("")
            print("{} != {}".format(toPythonLiteral(v1),
                                    toPythonLiteral(v2)))
        assert(v1 == v2)



sys.path.append("utilities")
from install_any import PackageInfo

PackageInfo.verbosity = 2

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

src_path = "FreeCAD_0.18-16131-Linux-Conda_Py3Qt5_glibc2.12-x86_64.AppImage"
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

src_path = "blender-2.49b-linux-glibc236-py26-x86_64.tar.bz2"
pkg = PackageInfo(src_path, is_dir=False)
assertEqual(pkg.caption, "Blender 2.49b")
assertEqual(pkg.arch, "64bit")

fileNames = [
    "mfcl2740dwlpr-3.2.0-1.i386.rpm",
    "Meshroom-2019.2.0-linux.tar.gz",
    "brscan-skey-0.2.4-1.x86_64.rpm",
    "tsetup.1.8.2.tar.xz",
    "DAIN_APP Alpha 0.41.rar",
    "duplicati-2.0.4.5-2.0.4.5_beta_20181128.noarch.rpm",
    "monero-gui-linux-x64-v0.17.1.9.tar.bz2",
    "org.gimp.GIMP.flatpakref",
]

dirNames = [
    "bash2py-3.6",
]

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
