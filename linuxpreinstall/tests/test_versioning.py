import unittest
import sys

from linuxpreinstall import (
    prerr,
    set_verbose,
)

from linuxpreinstall.versioning import (
    splitVersion,
    splitNestedVersion,
    prerr,
)

set_verbose(True)

class TestStringMethods(unittest.TestCase):

    def test_version(self):
        testName = "something-2.79b+my_patch"
        sys.stderr.write('* testing splitVersion("{}")...'
                         ''.format(testName))
        parts, version = splitVersion(testName)
        prerr('got ("{}", "{}")\n'.format(parts, version))
        self.assertEqual(parts, ["something-", "2.79b", "+my_patch"])
        self.assertEqual(version, "2.79b")
        # prerr('* testing splitVersion("{}", {})...'
        #       ''.format(version, True))
        prerr('* testing splitNestedVersion("{}")...'.format(testName))
        vinfo = splitNestedVersion(testName, verbose=True)
        self.assertEqual(vinfo['parts'],
                         ["something-", "2.79b", "+my_patch"])
        self.assertEqual(vinfo['version'], "2.79b")
        self.assertEqual(vinfo['number'], 2.79)
        self.assertEqual(vinfo['suffix'], "b")
