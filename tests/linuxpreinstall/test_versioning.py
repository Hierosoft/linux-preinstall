import unittest
import sys

from linuxpreinstall.lplogging import (
    echo0,
)

import linuxpreinstall.logging2 as logging


from linuxpreinstall.versioning import (
    splitVersion,
    splitNestedVersion,
)

# TODO: Require nopackage and use the version feature from it instead?


logging.basicConfig(level=logging.INFO)


class TestStringMethods(unittest.TestCase):

    def test_version(self):
        testName = "something-2.79b+my_patch"
        sys.stderr.write('* testing splitVersion("{}")...'
                         ''.format(testName))
        parts, version = splitVersion(testName)
        echo0('got ("{}", "{}")\n'.format(parts, version))
        self.assertEqual(parts, ["something-", "2.79b", "+my_patch"])
        self.assertEqual(version, "2.79b")
        # echo0('* testing splitVersion("{}", {})...'
        #       ''.format(version, True))
        echo0('* testing splitNestedVersion("{}")...'.format(testName))
        vinfo = splitNestedVersion(testName, verbose=True)
        self.assertEqual(vinfo['parts'],
                         ["something-", "2.79b", "+my_patch"])
        self.assertEqual(vinfo['version'], "2.79b")
        self.assertEqual(vinfo['number'], 2.79)
        self.assertEqual(vinfo['suffix'], "b")
