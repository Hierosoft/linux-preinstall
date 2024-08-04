
class ReadOnlyDict(dict):
    """Dictionary that becomes Read-only after calling readonly.
    Based on sysdirs.py in hierosoft.

    based on https://stackoverflow.com/a/19023331/4541104
    """

    # "$" and "%" are *mixed intentionally* since the blnk file may have
    #   come from another OS:

    def __init__(self):
        dict.__init__(self)
        self.__readonly = False
        self._substitutions = {
            "$CLOUD": None,
            "%CLOUD%": None,
        }  # ^ CLOUD values are set in check_cloud.

    def readonly(self, readonly=True):
        """Allow or deny modifying dictionary"""
        if readonly is None:
            readonly = False
        elif readonly not in (True, False):
            raise TypeError("readonly shoul be True or False (got {})"
                            "".format(readonly))
        self.__readonly = readonly

    def __setitem__(self, key, value):
        if self.__readonly:
            raise TypeError("__setitem__ is not supported")
        return dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        if self.__readonly:
            raise TypeError("__delitem__ is not supported")
        return dict.__delitem__(self, key)
