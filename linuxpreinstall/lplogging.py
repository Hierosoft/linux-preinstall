#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
import sys

from linuxpreinstall.logging2 import (  # noqa: E402
    getLogger,
)

logger = getLogger(__name__)

# region hierosoft.morelogging relicensed by same author for linux-preinstall

to_log_level = {
    3: 10,
    2: 20,
    1: 30,
    0: 40,
}

verbosity_levels = [False, True, 0, 1, 2, 3]

verbosity = 0
for argI in range(1, len(sys.argv)):
    arg = sys.argv[argI]
    if arg.startswith("--"):
        if arg == "--verbose":
            verbosity = 1
        elif arg == "--debug":
            verbosity = 2


def is_enclosed(value, start, end):
    if len(value) < len(start) + len(end):
        return False
    return value.startswith(start) and value.endswith(end)


def is_str_like(value):
    return type(value).__name__ in ("str", "bytes", "bytearray", "unicode")


def write0(arg):
    sys.stderr.write(arg)
    sys.stderr.flush()
    return True


def echo0(*args, **kwargs):
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)
    return True


KIBI = 1024
MEBI = 1024 * 1024
GIBI = 1024 * 1024 * 1024
TEBI = 1024 * 1024 * 1024 * 1024
PEBI = 1024 * 1024 * 1024 * 1024 * 1024


def human_readable(byte_count, places=2):
    """Make a human-readable file size.
    Examples: 1024 becomes "1K".  1024*1024 becomes "1M". 1000000
    actually becomes "976.56K", since computers generally deal in
    Kibibytes, Mebibytes, etc actually, which are multiples of 1024, not
    1000 like when buying drives :(.

    A removed 5 rounds *down*--kept digit doesn't change: using banker's
    rounding as Python does by default, which should usually be used
    since it is demonstrably more numerically stable
    (<https://stackoverflow.com/a/45245802/4541104>) than:

    from decimal import Decimal, ROUND_HALF_UP
    Decimal(1.5).quantize(0, ROUND_HALF_UP)
    # This also works for rounding to the integer part:
    Decimal(1.5).to_integral_value(rounding=ROUND_HALF_UP)

    Args:
        byte_count (int): Number of bytes.
        places (int, optional): Number of places to keep for rounding.
            Defaults to 2.

    Returns:
        str: A human-readable size.
    """
    suffix = ""
    count = byte_count
    if byte_count > PEBI:
        count = byte_count / PEBI
        suffix = "P"
    elif byte_count > TEBI:
        count = byte_count / TEBI
        suffix = "T"
    elif byte_count > GIBI:
        count = byte_count / GIBI
        suffix = "G"
    elif byte_count > MEBI:
        count = byte_count / MEBI
        suffix = "M"
    elif byte_count > KIBI:
        count = byte_count / KIBI
        suffix = "K"
    return "{}{}".format(round(count, places), suffix)


def get_verbosity():
    return verbosity


def set_verbosity(verbosity_level):
    global verbosity
    if verbosity_level not in verbosity_levels:
        vMsg = verbosity_levels
        if isinstance(vMsg, str):
            vMsg = '"{}"'.format(vMsg)
        raise ValueError(
            "verbosity_levels must be one of {} not {}."
            "".format(verbosity_levels, vMsg)
        )
    verbosity = verbosity_level
# endregion hierosoft.morelogging relicensed by author for linux-preinstall
