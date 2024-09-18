from __future__ import print_function
import unittest
import os
import sys

if __name__ == "__main__":
    TEST_MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
    TESTS_DIR = os.path.dirname(TEST_MODULE_DIR)
    REPO_DIR = os.path.dirname(TESTS_DIR)
    sys.path.insert(0, REPO_DIR)

# TODO: Require nopackage and use the version feature from it instead?
from linuxpreinstall import (
    human_readable,
    sorted_versions,
)
import linuxpreinstall.logging2 as logging

logging.basicConfig(level=logging.DEBUG)


class TestLinuxPreinstall(unittest.TestCase):

    def test_human_readable(self):
        self.assertEqual(
            human_readable(1000000),
            "976.56K"
        )
        self.assertEqual(
            human_readable(1000000, 1),
            "976.6K"
        )
        self.assertEqual(
            human_readable(1000000, 3),
            "976.562K"  # 976.562 since using Python's default
            # banker's rounding (more stable--see human_readable's
            # docstring)
        )
        self.assertEqual(
            human_readable(1000000, 10),
            "976.5625K"
        )

    def test_compare_versions(self):
        """_summary_
        """
        # TODO: consider:
        # from packaging.version import parse  # requires packaging from PyPI
        # versions.sort(key=lambda v: parse(v.split('-')[0]))

        versions = [
            "4.5",
            "4.6-api",
            "4.5.2-api",
            "4.5-api",
            "4.7.1-api",
            "4.6.1-api",
            "4.7-api",
            "4.5.1-api",
            "4.40",
            "4.8-api",
            "4.7.2-api",
            "4.6.2-api"
        ]

        good_order = ['4.5', '4.5-api', '4.5.1-api', '4.5.2-api', '4.6-api', '4.6.1-api', '4.6.2-api', '4.7-api', '4.7.1-api', '4.7.2-api', '4.8-api', '4.40']
        self.assertEqual(sorted_versions(versions), good_order)


if __name__ == "__main__":
    unittest.main()