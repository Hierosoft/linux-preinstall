#!/usr/bin/env python
#from utilities.install_any import PackageInfo
import sys
import os

def toPythonLiteral(v):
    '''
    [copied from pycodetools.parsing by author]
    '''
    if v is None:
        return None
    elif v is False:
        return "False"
    elif v is True:
        return "True"
    elif ((type(v) == int) or (type(v) == float)):
        return str(v)
    elif (type(v) == tuple) or (type(v) == list):
        enclosures = '()'
        if type(v) == list:
            enclosures = '[]'
        s = enclosures[0]
        for val in v:
            s += toPythonLiteral(val) + ", "
            # ^ Ending with an extra comma has no effect on length.
        s += enclosures[1]
        return s
    return "'{}'".format(
        v.replace("'", "\\'").replace("\r", "\\r").replace("\n", "\\n")
    )


def assertEqual(v1, v2, tbs=None):
    '''
    [copied from pycodetools.parsing by author]
    Show the values if they differ before the assertion error stops the
    program.

    Keyword arguments:
    tbs -- traceback string (either caller or some sort of message to
           show to describe what data produced the arguments if they're
           derived from something else)
    '''
    if ((v1 is True) or (v2 is True) or (v1 is False) or (v2 is False)
            or (v1 is None) or (v2 is None)):
        if v1 is not v2:
            print("")
            print("{} is not {}".format(toPythonLiteral(v1),
                                        toPythonLiteral(v2)))
            if tbs is not None:
                print("for {}".format(tbs))
        assert(v1 is v2)
    else:
        if v1 != v2:
            print("")
            print("{} != {}".format(toPythonLiteral(v1),
                                    toPythonLiteral(v2)))
            if tbs is not None:
                print("for {}".format(tbs))
        assert(v1 == v2)


def assertAllEqual(list1, list2, tbs=None):
    '''
    [copied from pycodetools.parsing by author]
    '''
    if len(list1) != len(list2):
        print("The lists are not the same length: list1={}"
              " and list2={}".format(list1, list2))
        assertEqual(len(list1), len(list2))
    for i in range(len(list1)):
        assertEqual(list1[i], list2[i], tbs=tbs)


sys.path.append("utilities")
# import ...

print("")
print("There are no tests.")
print("")
