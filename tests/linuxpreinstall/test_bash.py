from __future__ import print_function
import unittest
import os
import sys

TEST_MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
TESTS_DIR = os.path.dirname(TEST_MODULE_DIR)
REPO_DIR = os.path.dirname(TESTS_DIR)

if __name__ == "__main__":
    sys.path.insert(0, REPO_DIR)


from linuxpreinstall.bash import compare_files  # noqa: E402
import linuxpreinstall.logging2 as logging  # noqa: E402

logging.basicConfig(logging.INFO)

TESTS_DIR = os.path.join(REPO_DIR, "tests")
TEST_DATA_DIR = os.path.join(TESTS_DIR, "data")
COMPARE_DIR = os.path.join(TEST_DATA_DIR, "compare_files")

file1 = os.path.join(COMPARE_DIR, "file1")
file2same = os.path.join(COMPARE_DIR, "file2same")
file2different_bigger = os.path.join(COMPARE_DIR, "file2different-bigger")
file2different_smaller = os.path.join(COMPARE_DIR, "file2different-smaller")


class TestLinuxPreinstall(unittest.TestCase):

    def test_compare_files(self):
        self.assertTrue(compare_files(file1, file2same))
        self.assertFalse(compare_files(file1, file2different_bigger))
        self.assertFalse(compare_files(file1, file2different_smaller))


if __name__ == "__main__":
    unittest.main()