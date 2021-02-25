#!/usr/bin/env python
#from utilities.install_any import PackageInfo
import sys
import os

def assertEqual(v1, v2):
    '''
    Show the values if they differ before the assertion error stops the
    program.
    '''
    if ((v1 is True) or (v2 is True) or (v1 is False) or (v2 is False)
            or (v1 is None) or (v2 is None)):
        if v1 is not v2:
            print("")
            print("{} is not {}".format(v1, v2))
        assert(v1 is v2)
    else:
        if v1 != v2:
            print("")
            print("{} != {}".format(v1, v2))
        assert(v1 == v2)



sys.path.append("utilities")
from install_any import PackageInfo

pkg = PackageInfo("flashprint_4.6.2_amd64.deb")
assertEqual(pkg.name, "flashprint")
assertEqual(pkg.caption, "FlashPrint 4.6.2 (deb)")
pkg = PackageInfo("FlashPrint-4.5.1.deb")
assertEqual(pkg.name,  "flashprint")
assertEqual(pkg.caption, "FlashPrint 4.5.1 (deb)")

tests_dir = "tests"
test1_dir = os.path.join(tests_dir, "someprogram-1.0")
src_path = test1_dir
pkg = PackageInfo(src_path)
assertEqual(pkg.name, "someprogram")
assertEqual(pkg.version, "1.0")

src_path = os.path.join(tests_dir, "some_program-1.0.0.dummy")
pkg = PackageInfo(src_path)
assertEqual(pkg.caption, "Some Program 1.0.0")
assertEqual(pkg.name, "some_program")

packageNames = [
    "mfcl2740dwlpr-3.2.0-1.i386.rpm",
    "Meshroom-2019.2.0-linux.tar.gz",
    "bash2py-3.6",
    "brscan-skey-0.2.4-1.x86_64.rpm",
    "Ultimaker_Cura-4.7.1.appimage",
    "tsetup.1.8.2.tar.xz",
    "DAIN_APP Alpha 0.41.rar",
    "duplicati-2.0.4.5-2.0.4.5_beta_20181128.noarch.rpm",
    "monero-gui-linux-x64-v0.17.1.9.tar.bz2",
    "org.gimp.GIMP.flatpakref",
]

for fname in packageNames:
    print("")
    pkg = PackageInfo(fname)
    print("{}:\n  {}".format(fname, pkg))
