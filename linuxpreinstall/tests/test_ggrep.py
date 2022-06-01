import unittest
import sys

from linuxpreinstall import (
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
        set_verbose(2)
        self.assertEqual(is_like("abcdecde", "*cde"), True)
        set_verbose(1)
        self.assertEqual(is_like("abcabcde", "abc*"), True)
        self.assertEqual(is_like("/home/foo", "*/foo"), True)
        # As per <https://git-scm.com/docs/gitignore#:~:
        # text=Two%20consecutive%20asterisks%20(%22%20**%20%22,
        # means%20match%20in%20all%20directories.>:
        self.assertEqual(is_like("/home/foo", "**/foo"), True)
        self.assertEqual(is_like("/home/example/foo", "**/foo"), True)
        self.assertEqual(is_like("/home/foo/bar", "**/foo/bar"), True)
        self.assertEqual(is_like("/home/example/foo/bar", "**/foo/bar"), True)
        self.assertEqual(is_like("/home/example/foo/bar", "**/f*o/bar"), True)
        self.assertEqual(is_like("/home/example/foo/bar", "/home/**/foo/bar"), True)
        self.assertEqual(is_like("/home/examplefoo/bar", "/home/**/foo/bar"), False)
        # self.assertEqual(is_like("/home/examplefoo/bar", "/home/**foo/bar"), False)
        self.assertEqual(is_like("/home/example/foobar", "/home/**/foo/bar"), False)
        # set_verbose(2)
        self.assertEqual(is_like("/home/example/foo/bar", "/home/example/foo/**"), True)
        # set_verbose(1)
        self.assertEqual(is_like("/home/example/foo/bar", "**/bar"), True)
        self.assertEqual(is_like("/home/example/foo/bar", "**/bar/bar"), False)

        # As per python gitignore such as in
        # python-lsp-server/.gitignore such as in spyder/external-deps/:
        self.assertEqual(is_like("/home/foo.vscode/", "**/*.vscode/"), True)

        got_the_right_error = False
        try:
            self.assertEqual(is_like("/workspace.xml", None), False)
        except TypeError as ex:
            self.assertTrue(str(ex) in ["'NoneType' object is not iterable", "'NoneType' object is not subscriptable"])
            got_the_right_error = True
        self.assertEqual(got_the_right_error, True)

        got_the_right_error = False
        try:
            self.assertEqual(is_like(None, "/workspace.xml"), False)
        except TypeError as ex:
            self.assertTrue(str(ex)in ["object of type 'NoneType' has no len()", "'NoneType' object is not subscriptable"])
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
            self.assertTrue(str(ex) in ["object of type 'NoneType' has no len()", "'NoneType' object is not subscriptable"])
            got_the_right_error = True
        self.assertEqual(got_the_right_error, True)

