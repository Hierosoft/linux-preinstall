#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Strict import tests for the linuxpreinstall package.

Every submodule is imported exactly once during test discovery.
Any import failure aborts the entire test run immediately.
"""

from __future__ import print_function

import os
import sys
import unittest
import pkgutil

# ----------------------------------------------------------------------
# Make the repository importable when running from the source tree
# ----------------------------------------------------------------------
TESTS_SUB_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(os.path.dirname(TESTS_SUB_DIR))

if REPO_DIR not in sys.path:
    sys.path.insert(0, REPO_DIR)

# ----------------------------------------------------------------------
# Import helper that works on Python 2.7 and Python 3
# ----------------------------------------------------------------------
if sys.version_info[0] >= 3:
    def import_module(name):
        import importlib
        return importlib.import_module(name)
else:
    def import_module(name):
        __import__(name)
        return sys.modules[name]

# Import the top-level package now -- fail immediately if broken
linuxpreinstall = import_module("linuxpreinstall")


class TestLinuxPreinstallImports(unittest.TestCase):
    """One merciless test per submodule."""

    maxDiff = None

    def test_00_import_main_package(self):
        """Top-level package must import cleanly."""
        self.assertIn("linuxpreinstall", sys.modules)
        self.assertEqual(
            sys.modules["linuxpreinstall"].__name__,
            "linuxpreinstall",
        )


def _generate_import_tests():
    """Create one test per module -- collected only once."""
    discovered = []                     # (full_name, is_pkg)

    def crawl(pkg, prefix):
        """Recursively walk the package."""
        for _imp, modname, ispkg in pkgutil.walk_packages(
            pkg.__path__, prefix + "."
        ):
            full_name = modname
            discovered.append((full_name, ispkg))

            if ispkg:
                subpkg = import_module(full_name)   # fails hard if broken
                crawl(subpkg, full_name)

    crawl(linuxpreinstall, "linuxpreinstall")

    # Deterministic order
    discovered.sort(key=lambda item: item[0])

    for idx, (full_name, ispkg) in enumerate(discovered, start=1):
        test_name = "test_%04d_import_%s" % (
            idx, full_name.replace(".", "_")
        )

        def test(self, name=full_name):
            """Import must succeed."""
            module = import_module(name)        # will raise if broken
            self.assertIs(sys.modules[name], module)
            self.assertEqual(module.__name__, name)

        test.__name__ = test_name
        test.__doc__ = "Import %s%s" % (
            full_name, " (package)" if ispkg else ""
        )
        setattr(TestLinuxPreinstallImports, test_name, test)


# Generate tests -- any broken sub-package raises ImportError right here
_generate_import_tests()


if __name__ == "__main__":
    unittest.main(verbosity=2)
