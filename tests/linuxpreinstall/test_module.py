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
from linuxpreinstall import human_readable
set_verbosity(True)


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
