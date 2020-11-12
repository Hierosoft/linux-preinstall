#!/usr/bin/env python
from __future__ import division

import sys

# As per help.ubuntu.com:
# > n, 1, 2, n-1, n-2, 3, 4, n-3, n-4, 5, 6, n-5, n-6, 7, 8, n-7, n-8,
# > 9, 10, n-9, n-10, 11, 12, n-11
# > Examples:
# > 4 page booklet: Type 4,1,2,3
# > 8 page booklet: Type 8,1,2,7,6,3,4,5
# > 20 page booklet: Type 20,1,2,19,18,3,4,17,16,5,6,15,14,7,8,13,12,9,10,11
#
# -<https://help.ubuntu.com/stable/ubuntu-help/
# printing-booklet-duplex.html.en>

"""After using the booklet_order function, you must set the printer's
duplex setting to "Flip on Short Side" and the "Pages" option (may be
under "Range and Copies" depending on your desktop environment) to the
booklet_order. Pages per sheet: 2. Multiple pages per sheet order: Left
to Right, then down.
"""

# n,
# 1, 2,
# n-1, n-2,
# 3, 4,
# n-3, n-4,
# 5, 6,
# n-5, n-6,
# 7, 8,
# n-7, n-8,
# 9, 10,
# n-9, n-10,
# 11, 12,
# n-11


# or:

# n, 1,  # b
# 2, n-1,  # f

# n-2, 3,  # b
# 4, n-3,  # f

# n-4, 5,  # b
# 6, n-5,  # f

# n-6, 7,  # b
# 8, n-7,  # f

# n-8, 9,  # b
# 10, n-9,  # f

# n-10, 11,  # b
# 12, n-11  # f


def booklet_order(n):
    """
    Provide a list of page numbers for printing a booklet with a duplex
    printer.

    Sequential arguments:
    n -- The total page count. You must provide an even number, so if
    the document has an odd number of pages, make it so (makes either
    front or back blank--unless you put a blank page before the back
    or after the front).
    """
    n = int(n)
    allow_any = False
    if (n%2 != 0) and (not allow_any):

        raise ValueError("You must provide an even number of pages."
                         " Add a blank page if the document does not"
                         " have an even number, otherwise the necessary"
                         " page order for printing a booklet will"
                         " differ.")
    ret = []
    x = 0  # 0 is left, 1 is right (relative to front or back)
    # back = 1  # print on the back twice in a row
    p = 1
    offset = 2
    # for i in range(n//2):
    while p <= n:
        for back in range(2):
            for x in range(2):
                if back == 0:
                    if x == 0:
                        ret.append(n - (offset - 2))
                    else:
                        ret.append(offset - 1)
                else:
                    if x == 0:
                        ret.append(offset)
                    else:
                        ret.append(n - (offset - 1))
                p += 1
        offset += 2
    return ret


def main():
    if len(sys.argv) < 2:  # 0 is script
        print("You must provide a page count to create booklet"
              " page order.")
        exit(1)
    print(booklet_order(sys.argv[1]))
    pass


if __name__ == "__main__":
    main()
