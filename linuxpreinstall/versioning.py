import os
import sys
import select

from linuxpreinstall import (
    write0,
    write1,
    echo0,  # formerly prerr
    echo1,
    is_verbose,
)

digits = "1234567890"
versionStarters  = digits
versionChars = versionStarters + "."
versionEnders = "+-"

more_nums_err_fmt = ("strings with more than one number is not"
                     " implemented in sortversion's splitVersion"
                     " function: \"{}\"")


def nextIsDigit(s, i):
    if i + 1 >= len(s):
        return False
    return s[i+1] in digits


def isVersionChar(s, i):
    '''
    Only return true on digit, or on "." if there is a digit after it.
    '''
    if i >= len(s):
        return False
    if s[i] == '.':
        if nextIsDigit(s, i):
            return True
    elif s[i] in digits:
        return True
    return False


def isVersionEnder(s, i):
    '''
    Only return true on special character, or on "." if there is not a
    digit after it.
    '''
    if s[i] == '.':
        if nextIsDigit(s, i):
            return False
        return True
    elif s[i] in versionEnders:
        return True
    return False


def splitVersion(s, onlyNumeric=False):
    '''
    Split a name into segments where one segment is a version and as
    the second tuple element return the version. The
    process is made more precise by only collecting one version then
    ignoring other numbers after that.
    For example, "linux-1.1b+my_patch-2.2.bin" becomes
    (["linux-", "1.1b", "+my_patch-2.2.bin"], "1.1b").
    If the "onlyNumeric" option is True, then the onlyNumeric part will be
    returned separately. The recommended use is to call the function
    twice and the second time provide the version and set onlyNumeric=True
    to get the numerically sortable part of it. That way, you can do a
    custom sort where "1.1" can be sorted as the primary criteria and
    "b" can be the secondary criteria. To do this automatically,
    use splitNestedVersion instead.
    '''
    parts = []
    num = False
    tmp = ""
    version = None
    # curVerStarters = versionStarters
    # ^ change to "" when done collecting to stop.
    for i in range(len(s)):
        c = s[i]
        if num:
            if ((not onlyNumeric) and (isVersionEnder(s, i))) or (onlyNumeric and (not isVersionChar(s, i))):
                num = False
                if version is None:
                    version = tmp
                else:
                    raise ValueError(more_nums_err_fmt.format(s))
                parts.append(tmp)
                tmp = ""
                if i+1 < len(s):
                    parts.append(s[i:])
                    # ^ Also return whatever is after version (as one).
                    #   Use i not i+1 because this char is not matching!
                if onlyNumeric:
                    return version, s[i:]
                else:
                    return parts, version
            else:
                tmp += c
        else:
            if c in versionStarters:
                num = True
                if len(tmp) > 0:
                    parts.append(tmp)
                    tmp = ""
                tmp += c
            else:
                tmp += c
    if len(tmp) > 0:
        if num:
            if version is not None:
                raise ValueError(more_nums_err_fmt.format(s))
            version = tmp
        parts.append(tmp)
        tmp = ""

    if onlyNumeric:
        return version, parts[-1]
    else:
        return parts, version


def splitNestedVersion(s, verbose=False):
    '''
    Split a filename or program name into the string before the version,
    the version, any suffix after the version number, and whatever is
    left. The result is a dictionary with:
    - parts: All of those parts described above
    - version: the entire version including any suffixes such as "2.79b"
    - number: the numeric part of the version such as "2.79"
    - suffix: any suffix that seems like part of the version (before
      a dot) such as "b".

    '''
    write1('  * running splitVersion("{}")...'.format(s))
    parts, version = splitVersion(s)
    write1('got ("{}", "{}")\n'.format(parts, version))
    write1('  * running splitVersion("{}", {})...'
           ''.format(version, True))
    if version is None:
        version = ""
        number = None
        suffix = None
    else:
        number, suffix = splitVersion(version, onlyNumeric=True)
    write1('got ({}, "{}")\n'.format(number, suffix))

    if number is not None:
        number = float(number)
    else:
        number = 0
    if suffix is None:
        suffix = ""
    return {
        'parts': parts,
        'version': version,
        'number': number,
        'suffix': suffix,
    }


def main():
    # tests = TestStringMethods()
    # tests.test_version()

    echo0("# [sortversion] is checking for data...")
    # if sys.stdin.isatty():
    # ^ https://stackoverflow.com/a/17735803/4541104 hangs on no input :(

    lines = []
    infos = []
    if select.select([sys.stdin,],[],[],0.0)[0]:
        # NOTE: ^ https://stackoverflow.com/a/3763257/4541104 only works on non-Windows
        for rawBytes in sys.stdin:
            rawL = str(rawBytes)
            line = rawL.rstrip()
            lines.append(line)
            infos.append(splitNestedVersion(line, verbose=is_verbose()))

        infos = sorted(infos, key=lambda line: line['version'])
        for info in infos:
            print("".join(info['parts']))

        echo0("# [sortversion] Done sorting")
    else:
        echo0("# [sortversion] nothing to sort")


if __name__ == "__main__":
    main()
