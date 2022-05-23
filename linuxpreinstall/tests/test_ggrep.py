import unittest
import sys

from linuxpreinstall import (
    prerr,
    set_verbose,
)

from linuxpreinstall.ggrep import (
    is_like,
)

class TestGrepStringMethods(unittest.TestCase):

    def test_is_like(self):
        set_verbose(True)
        self.assertEqual(is_like("abc", "abc"), True)
        self.assertEqual(is_like("abc", "?bc"), True)
        self.assertEqual(is_like("abc", "a?c"), True)
        self.assertEqual(is_like("abc", "ab?"), True)
        self.assertEqual(is_like("abc", "?b?"), True)
        self.assertEqual(is_like("abc", "???"), True)
        self.assertEqual(is_like("ab", "???"), False)
        self.assertEqual(is_like("abc", "????"), False)
        self.assertEqual(is_like("abc", "??"), False)
        self.assertEqual(is_like("abcd", "???"), False)
        self.assertEqual(is_like("ababab", "ab"), False)
        self.assertEqual(is_like("ab", "ababab"), False)
        self.assertEqual(is_like("a", "aaa"), False)
        self.assertEqual(is_like("aaa", "a"), False)
        self.assertEqual(is_like("ababab", "*ababab"), True)
        self.assertEqual(is_like("ababab", "ababab*"), True)
        self.assertEqual(is_like("abcdab", "*cd*"), True)
        self.assertEqual(is_like("abcdef", "*ef"), True)
        self.assertEqual(is_like("abcdef", "*ab"), False)
        self.assertEqual(is_like("abcdef", "ab*"), True)
        self.assertEqual(is_like("abcdef", "ef*"), False)
        self.assertEqual(is_like("abcdef", "a*f"), True)
        self.assertEqual(is_like("abcdef", "a*f*"), True)
        self.assertEqual(is_like("abcdef", "*a*f"), True)
        self.assertEqual(is_like("abcdef", "*a*f*"), True)
        self.assertEqual(is_like("abcdef", "*b*e*"), True)
        self.assertEqual(is_like("abcdef", "*ab*ef"), True)
        self.assertEqual(is_like("abcdef", "*ab*ef*"), True)
        self.assertEqual(is_like("abcdef", "ab*ef"), True)
        self.assertEqual(is_like("abcdef", "abcde"), False)
        self.assertEqual(is_like("abcdef", "bcdef"), False)
        self.assertEqual(is_like("ababab", "ab"), False)


