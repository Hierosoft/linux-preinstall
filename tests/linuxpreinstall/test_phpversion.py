from __future__ import print_function
import unittest
import sys

from linuxpreinstall import (
    echo0,  # formerly prerr
    set_verbosity,
    find_not_decimal,
    rfind_not_decimal,
    split_package_parts,
)

# from linuxpreinstall.phpversion import (
# )

# TODO: Require nopackage and use the version feature from it instead?

set_verbosity(True)


class TestPackageStringMethods(unittest.TestCase):

    def test_version_detection(self):
        good_parts = ["php", "7.3", "pgsql"]
        test_name = "php7.3-pgsql"
        echo0("* test_version_detection: find_not_decimal, rfind_not_decimal, split_package_parts")
        echo0("  * test_name is '{}'".format(test_name))
        parts = test_name.split("-")

        self.assertEqual(rfind_not_decimal(parts[0]), 2)
        self.assertEqual(rfind_not_decimal(test_name, 3), 2)
        self.assertEqual(find_not_decimal(parts[0]), 0)
        good_i = 6
        echo0("  * character at {} is '{}'".format(good_i, test_name[good_i]))
        self.assertEqual(find_not_decimal(test_name, 3), 6)
        # ^ 6 is -
        # Therefore it should also stop at start if starts at 6 since
        #   6 is not part of a float number:
        self.assertEqual(find_not_decimal(test_name, 6), 6)
        got_parts = split_package_parts(test_name)
        echo0("  * parts: {}".format(got_parts))
        self.assertEqual(got_parts, good_parts)

        self.assertEqual(split_package_parts("php7.4"), ["php", "7.4"])

        self.assertEqual(split_package_parts("php"), ["php"])

        test_lib_name = "libapache2-mod-php7.3"
        good_lib_parts = ["libapache2-mod-php", "7.3"]
        self.assertEqual(split_package_parts(test_lib_name), good_lib_parts)
