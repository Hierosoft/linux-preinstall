import unittest
import sys

from linuxpreinstall import (
    prerr,
    set_verbose,
)

from linuxpreinstall.ggrep import (
    is_like,
    is_like_any,
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
        self.assertEqual(is_like("/workspace.xml", "/workspace.xml"), True)

        got_the_right_error = False
        try:
            self.assertEqual(is_like("/workspace.xml", None), False)
        except TypeError as ex:
            self.assertEqual(str(ex), "'NoneType' object is not iterable")
            got_the_right_error = True
        self.assertEqual(got_the_right_error, True)

        got_the_right_error = False
        try:
            self.assertEqual(is_like(None, "/workspace.xml"), False)
        except TypeError as ex:
            self.assertEqual(str(ex), "object of type 'NoneType' has no len()")
            got_the_right_error = True
        self.assertEqual(got_the_right_error, True)

        got_the_right_error = False
        try:
            self.assertEqual(is_like("/workspace.xml", ""), False)
        except ValueError as ex:
            got_the_right_error = True
        self.assertEqual(got_the_right_error, True)


    def test_is_like_any(self):
        set_verbose(True)

        got_the_right_error = False
        try:
            self.assertEqual(is_like_any("/home/1/abab", None), False)
        except TypeError as ex:
            self.assertEqual(str(ex), "'NoneType' object is not iterable")
            got_the_right_error = True
        self.assertEqual(got_the_right_error, True)

        got_the_right_error = False
        try:
            self.assertEqual(is_like_any(None, "/home/1/abab"), False)
        except TypeError as ex:
            self.assertEqual(str(ex), "object of type 'NoneType' has no len()")
            got_the_right_error = True
        self.assertEqual(got_the_right_error, True)

