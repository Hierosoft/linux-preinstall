#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import json

from linuxpreinstall.lplogging import (  # noqa: E402
    echo0,
)
from linuxpreinstall.logging2 import (  # noqa: E402
    getLogger,
)

logger = getLogger(__name__)


# region hierosoft.ggrep relicensed by author for linux-preinstall
def _wild_increment(haystack_c, needle_c):
    if needle_c == "*":
        return 0
    if needle_c == "?":
        return 1
    if needle_c == haystack_c:
        return 1
    return -1


def contains(haystack, needle, allow_blank=False, quiet=False):
    '''Check if the substring "needle" is in haystack.

    The behavior differs from the Python "in" command according to the
    arguments described below.

    Args:
        haystack (str): a string to look in
        needle (str): a string for which to look
        allow_blank (bool): Instead of raising an exception on a blank
            needle, return False and show a warning (unless quiet).
        quiet (bool): Do not report errors to stderr.

    Raises:
        ValueError: If allow_blank is not True, a blank needle will
            raise a ValueError, otherwise there will simply be a False
            return.
        TypeError: If no other error occurs, the "in" command will raise
            "TypeError: argument of type 'NoneType' is not iterable" if
            haystack is None (or haystack and needle are None), or
            "TypeError: 'in <string>' requires string as left operand,
            not NoneType" it needle is None.
    '''
    if len(needle) == 0:
        if not allow_blank:
            raise ValueError(
                'The needle can\'t be blank or it would match all.'
                ' Set to "*" to match all explicitly.'
            )
        else:
            if not quiet:
                echo0("The needle is blank so the match will be False.")
        return False
    return needle in haystack


def any_contains(haystacks, needle, allow_blank=False, quiet=False,
                 case_sensitive=True):
    '''Check whether any haystack contains the needle.
    For documentation of keyword arguments, see the "contains" function.

    Returns:
        bool: The needle is in any haystack.
    '''
    if not case_sensitive:
        needle = needle.lower()
    for rawH in haystacks:
        haystack = rawH
        if not case_sensitive:
            haystack = rawH.lower()
        # Passing case_sensitive isn't necessary since lower()
        # is already one in that case above:
        if contains(haystack, needle, allow_blank=allow_blank, quiet=quiet):
            logger.debug("is_in_any: {} is in {}".format(needle, haystack))
            return True
    return False


def contains_any(haystack, needles, allow_blank=False, quiet=False,
                 case_sensitive=True):
    '''Check whether the haystack contains any of the needles.

    For documentation of keyword arguments, see the "contains" function.

    Returns:
        bool: Any needle is in the haystack.
    '''
    if not case_sensitive:
        needle = haystack.lower()
    for rawN in needles:
        needle = rawN
        if not case_sensitive:
            needle = rawN.lower()
        # Passing case_sensitive isn't necessary since lower()
        # is already one in that case above:
        if contains(haystack, needle, allow_blank=allow_blank, quiet=quiet):
            logger.debug("is_in_any: {} is in {}".format(needle, haystack))
            return True
    return False


def is_like(haystack, needle, allow_blank=False, quiet=False,
            haystack_start=None, needle_start=None, indent=2):
    '''Compare to needle using wildcard notation not regex.

    Args:
        haystack (str): a string in which to find the needle.
        needle (str): It is a filename pattern such as "*.png" not
            regex, so the only wildcards are '*' and '?'.
        allow_blank (Optional[bool]): Instead of raising an exception on
            a blank needle, return False and show a warning (unless
            quiet).
        quiet (Optional[bool]): Do not report errors to stderr.
        haystack_start (Optional[bool]): Start at this character index
            in haystack.
        needle_start (Optional[bool]): Start at this character index in
            needle.
        indent (Optional[int]): Set the visual indent level for debug
            output, expressed as a number of spaces. The default is 2
            since some higher level debugging will normally be taking
            place and calling this method.

    Returns:
        bool: If needle in literal text or wildcard syntax matches
            haystack.
    '''
    tab = " " * indent
    if haystack_start is None:
        haystack_start = 0
    if needle_start is None:
        needle_start = 0
    haystack = haystack[haystack_start:]
    needle = needle[needle_start:]
    logger.debug(
        tab+"in is_like({}, {})"
        .format(json.dumps(haystack), json.dumps(needle)))
    if needle_start == 0:
        double_star_i = needle.find("**")
        if "***" in needle:
            raise ValueError("*** is an invalid .gitignore wildcard.")
        if needle == "**":
            raise ValueError("** would match every directory!")
        if (double_star_i > 0):
            # and (double_star_i < len(needle) - 2):
            # It is allowed to be at the end.
            logger.debug(
                tab+"* splitting needle {} at **"
                .format(json.dumps(needle)))
            left_needle = needle[:double_star_i] + "*"
            right_needle = needle[double_star_i+2:]
            logger.debug(
                tab+"* testing left_needle={}"
                .format(json.dumps(left_needle)))
            if is_like(haystack, left_needle,
                       allow_blank=allow_blank, quiet=quiet,
                       indent=indent+2):
                right_haystack = haystack[len(left_needle)-1:]
                # ^ -1 to skip '*'
                # ^ -2 to skip '*/' but that's not all that needs to be
                #   skipped, the whole matching directory needs to be
                #   skipped, so:
                next_slash_i = right_haystack.find("/")
                if next_slash_i > -1:
                    right_haystack = right_haystack[next_slash_i:]
                elif right_needle == "":
                    logger.debug(
                        tab+"  * there is no right side,"
                        " so it matches")
                    # ** can match any folder, so the return is True
                    # since:
                    # - There is nothing to match after **, so any
                    #   folder (leaf only though) matches.
                    # - The remainder of haystack has no slash, so it is
                    #   a leaf.
                    return True
                logger.debug(
                    tab+"* testing right_haystack={}, right_needle={}"
                    .format(json.dumps(right_haystack),
                            json.dumps(right_needle)))
                if (right_needle == ""):
                    if (right_haystack == ""):
                        return True
                    else:
                        logger.debug(tab+"* WARNING: right_haystack")
                return is_like(right_haystack, right_needle,
                               allow_blank=True, quiet=quiet,
                               indent=indent+2)
            else:
                logger.debug(tab+"  * False")
                # It is already false, so return
                # (prevent issue 22: "More than one '*' in a row").
                return False
        if needle.startswith("**/"):
            needle = needle[1:]
            # It is effectively the same, and is only different when
            # a subfolder is specified (See
            # <https://git-scm.com/docs/gitignore#:~:
            # text=Two%20consecutive%20asterisks%20(%22%20**%20%22,
            # means%20match%20in%20all%20directories.>.
            # That circumstance is tested in test_ggrep.py.
        elif needle.startswith("!"):
            raise ValueError(
                "The value should not start with '!'."
                " The higher-level logic should check for inverse"
                " results and handle them differently."
            )
    req_count = 0
    prev_c = None
    for i in range(0, len(needle)):
        # ^ 0 since needle = needle[needle_start:]
        c = needle[i]
        if c == "*":
            if prev_c == "*":
                raise ValueError(
                    "More than one '*' in a row in needle isn't allowed"
                    " (needle={}). Outer logic should handle special"
                    " syntax if that is allowed."
                    "".format(json.dumps(needle))
                )
            prev_c = c
            continue
        req_count += 1
        prev_c = c
    if len(needle) == 0:
        if not allow_blank:
            raise ValueError(
                'The needle can\'t be blank or it would match all.'
                ' Set to "*" to match all explicitly.'
            )
        else:
            if not quiet:
                echo0(
                    tab
                    + "The needle is blank so the match will be False."
                )
        return False
    if req_count == 0:
        # req_count may be 0 even if has one character: "*"
        return True
    hI = 0  # 0 since haystack = haystack[haystack_start:]
    nI = 0  # 0 since needle = needle[needle_start:]
    matches = 0
    while hI < len(haystack):
        if nI >= len(needle):
            # If still in haystack, there are more things to match so
            # there aren't enough needle characters/wildcards.
            return False
        inc = _wild_increment(haystack[hI], needle[nI])
        if inc == 0:
            # *
            if (nI+1) == len(needle):
                # The needle ends with *, so the matching is complete.
                return True
            # match_indices = []
            next_needle_c = needle[nI+1]
            logger.debug(
                tab+"* checking for each possible continuation of"
                " needle[needle.find('*')+1]"
                " in haystack {}[{}:] -> {}"
                .format(haystack, hI, haystack[hI:]))
            for try_h_i in range(hI, len(haystack)):
                if haystack[try_h_i] == next_needle_c:
                    logger.debug(
                        tab+"  * is_like({}[{}:] -> {}, {}[{}+1:]"
                        " -> {})"
                        .format(haystack, try_h_i,
                                haystack[try_h_i:],
                                needle, nI, needle[nI+1:]))
                    if is_like(haystack, needle,
                               allow_blank=allow_blank,
                               quiet=quiet, haystack_start=try_h_i,
                               needle_start=nI+1,
                               indent=indent+2):
                        logger.debug(tab+"    * True")
                        # The rest may match from ANY starting point of
                        # the character after *, such as:
                        # abababc is like *ababc (should be True)
                        # - If next_needle_c were used, that wouldn't
                        #   return True as it should.
                        # - To return True, the recursion will occur
                        #   twice:
                        #   - (abababc, ababc) -> False
                        #   - (ababc, ababc) -> True
                        #   - or:
                        #     - (abababc, a*c) -> False
                        #     - (ababc, a*c) -> True
                        return True
                    else:
                        logger.debug(tab+"    * False")

            if next_needle_c == haystack[hI]:
                nI += 2
                matches += 1  # Only 1 since req_count doesn't have '*'
            hI += 1
        elif inc == 1:
            hI += 1
            nI += 1
            matches += 1
        elif inc == -1:
            return False
    logger.debug(
        tab+"is_like matches={} req_count={}"
        .format(matches, req_count))
    return matches == req_count


def is_like_any(haystack, needles, allow_blank=False, quiet=False):
    for needle in needles:
        if is_like(haystack, needle, allow_blank=allow_blank,
                   quiet=quiet):
            return True
    return False
# endregion hierosoft.ggrep relicensed by author for linux-preinstall
