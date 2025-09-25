# -*- coding: utf-8 -*-
"""
hierosoft submodule relicensed by same author for linux-preinstall

This submodule mimics Python 3 logging.
There is no logging class/object because
- The methods such as `warning` directly in the module just call
  logging2.root's methods.

See also:
> [Original Python logging package](https://old.red-dove.com/python_logging.html)
> This is the original source for the logging package. The version of the
> package available from this site is suitable for use with Python 1.5.2,
> 2.1.x and 2.2.x, which do not include the logging package in the
> standard library.
-<https://docs.python.org/3/library/logging.html>

However, basicConfig has changed as follows:
> Changed in version 3.2: The style argument was added.
> Changed in version 3.3: The handlers argument was added. Additional checks were added to catch situations where incompatible arguments are specified (e.g. handlers together with stream or filename, or stream together with filename).
> Changed in version 3.8: The force argument was added.
> Changed in version 3.9: The encoding and errors arguments were added.
-<https://docs.python.org/3/library/logging.html>

getLevelName changed as follows:
> Changed in version 3.4: In Python versions earlier than 3.4, this
> function could also be passed a text level, and would return the
> corresponding numeric value of the level. This undocumented behavior
> was considered a mistake, and was removed in Python 3.4, but
> reinstated in 3.4.2 due to retain backward compatibility.
-<https://docs.python.org/3/library/logging.html>

Other Changes:
> logging.disable(level=CRITICAL):
> Changed in version 3.7: The level parameter was defaulted to level CRITICAL. See bpo-28524 for more information about this change.
>
> logging.getLogRecordFactory():
> Added in version 3.2: This function has been provided, along with setLogRecordFactory(), to allow developers more control over how the LogRecord representing a logging event is constructed.
>
> logging.setLogRecordFactory(factory):
> Added in version 3.2: This function has been provided, along with getLogRecordFactory(), to allow developers more control over how the LogRecord representing a logging event is constructed.
>
> logging.lastResort:
> "handler of last resort"
> Added in version 3.2
>
> Added in 3.11:
> getLevelNamesMapping
>
> Added in 3.12:
> getHandlerByName, getHandlerNames

-<https://docs.python.org/3/library/logging.html> accessed 2024-08-04
"""
from __future__ import print_function
from __future__ import division
import sys

# mimic logging._startTime
from datetime import datetime

try:
    from datetime import timezone
    # from datetime import UTC
    # later python versions use datetime.UTC
    # _startTime = datetime.datetime.now(datetime.UTC)
    # UTC is from the datetime module! Not datetime.datetime.
    # Also, it appears to be missing in Python 3.10.
    # Documentation says "Alias for the UTC time zone singleton
    # datetime.timezone.utc." so:

    def utcnow():
        return datetime.now(timezone.utc)
except ImportError:
    def utcnow():
        return datetime.utcnow()


FATAL = 50  # same as CRITICAL
CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
NOTSET = 0

_startTime = utcnow()

# mimic logging._nameToLevel:

_nameToLevel = {'FATAL': 50, 'CRITICAL': 50, 'ERROR': 40, 'WARNING': 30,
                'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}
# mimic logging.getLevelName:
_level_names = {50: "CRITICAL", 40: "ERROR", 30: "WARNING", 20: "INFO",
                10: "DEBUG", 0: "NOTSET"}  # manually set due to overlap!


def getLevelName(level):
    """mimic logging.getLevelName"""
    name = _level_names.get(level)
    if not name:
        return "Level {}".format(level)
    return name


def _conditional_message(*args, **kwargs):
    if '__level__' not in kwargs:
        raise ValueError("Expected '__level__'")
    if '__threshold__' not in kwargs:
        raise ValueError("Expected '__level__'")
    if '__name__' not in kwargs:
        raise ValueError("Expected '__name__'")
    level = get_effective_level(kwargs['__level__'])
    name = kwargs.get('__name__')
    threshold = get_effective_level(kwargs['__threshold__'])
    del kwargs['__level__']
    del kwargs['__name__']
    del kwargs['__threshold__']

    if threshold > level:
        return
    if name:
        sys.stderr.write("[{}] ".format(name))
    sys.stderr.write("[{}] ".format(_level_names[level]))
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)


FORMAT_STYLES = ['%', '{', '$']


def get_effective_level(level):
    if level >= CRITICAL:
        return CRITICAL
    if level >= ERROR:
        return ERROR
    if level >= WARNING:
        return WARNING
    if level >= INFO:
        return INFO
    if level >= DEBUG:
        return DEBUG
    if not level:
        # Mimic behavior of logging.Logger
        # (0 behaves as WARNING)
        return WARNING
    return NOTSET


class Formatter:
    def __init__(self, fmt=None, datefmt=None, style='%',
                 validate=True, defaults=None):
        # FIXME  validate=True, *, defaults=None):  what? (upstream code)
        if fmt is None:
            fmt = '%(message)s'
        self.fmt = fmt
        if style not in FORMAT_STYLES:
            raise ValueError(
                "style was %s but should be one in %s"
                % (style, FORMAT_STYLES))
        self.style = style
        self.t = None
        if style == "$":
            import string
            self.t = string.Template(fmt)
        # region attributes in upstream not implemented here yet
        self.datefmt = datefmt
        self.validate = validate
        self.defaults = defaults
        # endregion attributes in upstream not implemented here yet

    def format(self, message):
        if self.style == "%":
            return self.fmt % {'message': message}
        elif self.style == "{":
            return self.fmt.format(message=message)
        elif self.style == "$":
            # such as "Error: $message in some method"
            return self.t.substitute(message=message)
        else:
            raise ValueError(
                "style was %s but should be one in %s"
                % (self.style, FORMAT_STYLES))


default_formatter = Formatter()


class Logger:
    """A logger to mimic Python's logging.Logger
    Usually obtained via logging.getLogger(__name__)

    Args:
        name (str): The name of the logger (Required, like in
            Python 3's logging.Logger).
    """
    def __init__(self, name):
        self.name = name
        self.level = 0  # allowed to be 0 but 30 if 0
        # region attributes in upstream not implemented here yet
        # (via logger = logging.getLogger(); dir(logger)
        #   in Python 3.11 on Windows)
        # self._cache = None
        self._log = sys.stderr
        self.disabled = False
        # self.filter
        # self.filters
        self.handlers = []
        # self.hasHandlers
        # self.manager
        # self.parent
        # self.propagate = True
        # ^ if propagate, pass events to higher level handlers too
        # self.root
        # endregion attributes in upstream not implemented here yet

    def _message(self, *args, **kwargs):
        if '__level__' not in kwargs:
            raise ValueError("Expected '__level__'")
        kwargs['__threshold__'] = self.level
        kwargs['__name__'] = self.name
        # caller must set kwargs['__level__']
        _conditional_message(*args, **kwargs)

    # region methods in upstream not implemented here yet
    # def addFilter(self, ):
    # def addHandler(self, ):
    # def callHandlers(self, ):
    # def findCaller(self, ):
    # def getChild(self, ):
    # def log(self, ):
    # def makeRecord(self, ):
    # def removeFilter(self, ):
    # def removeHandler(self, ):
    # endregion methods in upstream not implemented here yet

    def isEnabledFor(self, level):  # noqa: N802
        return False if level < self.level else True

    def handle(self, record):
        # TODO: make a record class??
        for handler in self.handlers:
            handler.format(record)
            handler.emit(record)
        # TODO: check own formatter instead of code below
        print(default_formatter.format(record), file=self._log)

    def getEffectiveLevel(self):  # noqa: N802
        if self.level == 0:
            return root.level
        return max(get_effective_level(self.level), root.level)

    def critical(self, *args):
        self._message(*args, __level__=CRITICAL)

    def debug(self, *args):
        self._message(*args, __level__=DEBUG)

    def error(self, *args):
        self._message(*args, __level__=ERROR)

    def exception(self, ex):
        self.fatal("{}: {}".format(type(ex).__name__, ex))

    def fatal(self, *args):
        # NOTE: sys.maxint only in Python 2 (deprecated)
        #   and Python ints are unbounded, so maxsize is based
        #   on the system's word size (such as int64 on 64-bit (?))
        self._message(*args, __level__=sys.maxsize)

    def info(self, *args):
        self._message(*args, __level__=INFO)

    def setLevel(self, level):  # noqa: N802
        self.level = level

    def warn(self, msg):
        print(
            "<stdin>:1: DeprecationWarning:"
            " The 'warn' method is deprecated, use 'warning' instead",
            file=sys.stderr)
        self.warning(msg)

    def warning(self, *args):
        self._message(*args, __level__=WARNING)


class Handler:
    def __init__(self, level=NOTSET):
        raise NotImplementedError("Handler")


loggers = {}


class RootLogger(Logger):
    def __init__(self, level):
        Logger.__init__(self, 'root')
        self.level = level


root = RootLogger(WARNING)  # mimic logging


def critical(*args):
    root._message(*args, __level__=CRITICAL)


def debug(*args):
    root._message(*args, __level__=DEBUG)


def error(*args):
    root._message(*args, __level__=ERROR)


def exception(ex):
    root.fatal("{}: {}".format(type(ex).__name__, ex))


def fatal(*args):
    # NOTE: sys.maxint only in Python 2 (deprecated)
    #   and Python ints are unbounded, so maxsize is based
    #   on the system's word size (such as int64 on 64-bit (?))
    root._message(*args, __level__=sys.maxsize)


def info(*args):
    root._message(*args, __level__=INFO)


def warn(*args):
    root._message(*args, __level__=WARNING)


def warning(*args):
    root._message(*args, __level__=WARNING)


# class Logging(Logger):
#     self.__init__(self):
#         Logger.__init__('root')


def getLogger(self, name=None):  # noqa: N802
    logger = loggers.get(name)  # None is allowed (root of hierarchy)
    if logger is not None:
        return logger
    return Logger(name)


filename = None
encoding = 'utf-8'


def basicConfig(**kwargs):  # noqa: N802
    global filename
    global encoding
    string_keys = ['filename', 'encoding']
    for key, value in kwargs.items():
        if key in string_keys:
            if type(value).__name__ not in ("str", "unicode"):
                # ^ Do not use isinstance, since unicode is not in Python 3
                #   (every str is unicode)
                raise TypeError("Expected str/unicode for %s but got %s %s"
                                % (key, type(value).__name__, value))
        if key == "filename":
            filename = value
        elif key == "encoding":
            encoding = value
        elif key == "level":
            root.setLevel(value)
            # NOTE: *Not* same as root's level (50 default somehow)
            # NOTE: getEffectiveLevel is max(root.level, self.level),
            #   and level stays at 0 unless setLevel is called
        else:
            print(
                "[hierosoft.logging2] Warning: {} is not implemented."
                .format(key),
                file=sys.stderr)
