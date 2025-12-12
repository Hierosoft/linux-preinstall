#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hmm, only works if browser is user agent (?):
Running this just shows 403: Forbidden


"""
from __future__ import print_function

import glob
import json
import os
import shutil
import subprocess
import sys

# Python 2/3 compatibility for urllib imports
if sys.version_info.major >= 3:
    import urllib.request
    request = urllib.request
    from urllib.error import HTTPError, URLError
    from html.parser import HTMLParser
    from urllib.parse import urlparse, parse_qs
    from urllib.parse import quote as urllib_quote
    from urllib.parse import quote_plus as urllib_quote_plus
    from urllib.parse import urlencode
else:
    import urllib2 as urllib  # Python 2
    request = urllib
    from urllib2 import HTTPError, URLError
    from HTMLParser import HTMLParser  # noqa: F401
    from urlparse import urlparse, parse_qs
    from urllib import quote as urllib_quote
    from urllib import quote_plus as urllib_quote_plus
    from urllib import urlencode

# import tkinter as tk
# from tkinter import messagebox

try:
    # Find first version ([0]) of Tcl/Tk folders (based on workaround at
    #   <https://github.com/python/cpython/issues/111754>).
    os.environ["TCL_LIBRARY"] = os.path.dirname(glob.glob(
        os.path.join(sys.base_prefix, "tcl", "tcl*", "init.tcl")
    )[0])
    os.environ["TK_LIBRARY"] = os.path.dirname(glob.glob(
        os.path.join(sys.base_prefix, "tcl", "tk*", "pkgIndex.tcl")
    )[0])
    os.environ["TIX_LIBRARY"] = os.path.dirname(glob.glob(
        os.path.join(sys.base_prefix, "tcl", "tix*", "pkgIndex.tcl")
    )[0])
except IndexError:
    # no match
    pass
except AttributeError:
    # "AttributeError: 'module' object has no attribute 'base_prefix'"
    #   in Python 2
    pass

if sys.version_info.major >= 3:  # try:
    from tkinter import messagebox
    from tkinter import filedialog
    # from tkinter import simpledialog
    import tkinter as tk
    import tkinter.font as tkFont
    from tkinter import ttk
    # from tkinter import tix
    raw_input = input
    print("Warning: Python>=3 is being used, so str is not bytes.")
else:  # except ImportError:
    # Python 2
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
    # import tkSimpleDialog as simpledialog
    import Tkinter as tk
    import tkFont
    import ttk
    # import Tix as tix
    input = raw_input  # noqa: F821 # type:ignore

ENABLE_PSUTIL = False

try:
    import psutil
    ENABLE_PSUTIL = True
except ImportError:
    pass

CRT_DIR = '/etc/cups/ssl'

def main():
    if os.getuid() != 0:
        print("Relaunching with sudo...")
        subprocess.call(['sudo', sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
        sys.exit(0)

    if not os.path.exists(CRT_DIR):
        messagebox.showerror("Error", "Directory not found: " + CRT_DIR)
        sys.exit(1)

    try:
        files = [f for f in os.listdir(CRT_DIR) if f.endswith('.crt')]
    except Exception as e:
        messagebox.showerror("Error", str(e))
        sys.exit(1)

    root = tk.Tk()
    root.title("Certificate Update")

    label = tk.Label(root, text="Clear:")
    label.pack()

    def delete_cert(filename):
        cert_path = os.path.join(CRT_DIR, filename)
        try:
            os.remove(cert_path)
            messagebox.showinfo("Success", "Deleted " + filename)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    for filename in files:
        btn = tk.Button(root, text=filename, command=lambda f=filename: delete_cert(f))
        btn.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
