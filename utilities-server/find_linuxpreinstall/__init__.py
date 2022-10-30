from __future__ import print_function
try:
    import linuxpreinstall
    from linuxpreinstall import echo0
except ImportError as ex:
    # Python 3 ModuleNotFoundError is a subclass of ImportError (2 or 3)
    if "No module named 'linuxpreinstall'" in str(ex):
        import os
        import sys
        MY_FILE = os.path.realpath(__file__)
        MY_DIR = os.path.dirname(MY_FILE)
        UTILITIES_DIR = os.path.dirname(MY_DIR)
        REPO_DIR = os.path.dirname(UTILITIES_DIR)
        sys.path.insert(0, REPO_DIR)
        # print('* looking for linuxpreinstall in "{}"'.format(REPO_DIR),
        #       file=sys.stderr)
        from linuxpreinstall import echo0
        import linuxpreinstall
    else:
        print('Error: commands in {} should be either installed using'
              ' "pip install linux-preinstall", "setup.py" or {} must'
              ' be in a utilities* directory that is in'
              ' the same directory as linuxpreinstall.'
              ''.format(MY_DIR, MY_DIR, REPO_DIR),
               file=sys.stderr)
        exit(1)



