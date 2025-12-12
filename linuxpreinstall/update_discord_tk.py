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

# Conditional `which` function for Python 2 compatibility
if sys.version_info.major >= 3:
    from shutil import which
else:
    # Define `which` function for Python 2
    def which(name):
        for path in os.environ['PATH'].split(os.pathsep):
            full_path = os.path.join(path, name)
            if os.path.isfile(full_path):
                return full_path
        return None

class UpdateState:
    def __init__(self):
        # Load local machine information
        config_path = os.path.expanduser("~/.config/nopackage/local_machine.json")
        with open(config_path, 'r') as f:
            self.local_machine = json.load(f)

        # Initialize tkinter window
        self.root = tk.Tk()
        self.root.title("Updater")
        self.progress = tk.DoubleVar()

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress, maximum=100)
        self.progress_bar.pack(pady=20, padx=50)

        self.was_running = False
        self.program_name = None
        self.program_version = None
        self.set_program('discord')

    def set_program(self, name):
        self.program_name = name
        self.programs = self.local_machine.get('programs')
        if self.programs:
            self.program = self.programs.get(self.program_name)
            if self.program:
                self.program_version = self.program.get('version')

    def load_url(self):
        download_url = 'https://discord.com/api/download?platform=linux&format=tar.gz'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        # Get the final filename from the server response
        req = request.Request(download_url, headers=headers)
        try:
            response = request.urlopen(req)
        except (HTTPError, URLError) as e:
            messagebox.showerror("Error", "Failed to download %s: %s"
                                 % (download_url, e))
            sys.exit(1)

        filename = os.path.basename(urlparse(response.geturl()).path)
        version = filename.replace('.tar.gz', '').split('-')[-1]

        # Check version
        if version == self.program_version:
            messagebox.showinfo("Updater", "Version %s is already installed." % version)
            return 0

        # Ask user to confirm download
        if not messagebox.askokcancel("Updater", "New version %s available. Download?" % version):
            sys.exit(0)

        # Terminate running instances if any
        self.terminate_running_program()

        # Download and show progress
        download_path = os.path.join("/tmp", filename)
        self.download_file(response, download_path)

        # Install downloaded program
        self.install_program(download_path)

        # Run program again if needed
        if self.was_running:
            self.run_program_async()

        # Exit when done
        self.root.quit()

    def terminate_running_program_psutil(self):
        running_procs = [p for p in psutil.process_iter(['name']) if p.info['name'] == self.program_name]
        if running_procs:
            self.was_running = True
            if not messagebox.askokcancel("Updater", "%s is running. Terminate it?" % self.program_name):
                sys.exit(0)

            for proc in running_procs:
                proc.terminate()
                proc.wait()

    def terminate_running_program(self):
        if ENABLE_PSUTIL:
            return self.terminate_running_program_psutil()
        # Use subprocess to check if program is running (pgrep command)
        try:
            result = subprocess.check_output(["pgrep", self.program_name], stderr=subprocess.STDOUT)
            pids = result.decode('utf-8').splitlines()
        except subprocess.CalledProcessError:
            # No process is running
            return

        if pids:
            self.was_running = True
            if not messagebox.askokcancel(
                "Updater",
                "%s is running. Terminate it?" % self.program_name
            ):
                sys.exit(0)

            # Terminate the processes using pkill or kill
            for pid in pids:
                subprocess.call(["kill", pid])

    def download_file(self, response, download_path):
        total_size = int(response.headers.get('Content-Length', 0))
        chunk_size = 8192
        bytes_downloaded = 0

        with open(download_path, 'wb') as f:
            while True:
                data = response.read(chunk_size)
                if not data:
                    break
                f.write(data)
                bytes_downloaded += len(data)
                self.progress.set((bytes_downloaded / float(total_size)) * 100)
                self.root.update()

    def install_program(self, download_path):
        if self.program:
            subprocess.call(["nopackage", "remove", self.program_name])
        subprocess.call(["nopackage", "install", download_path])

    def run_program_async(self):
        subprocess.Popen([self.program_name], close_fds=True)

def main():
    updater = UpdateState()
    updater.load_url()

if __name__ == '__main__':
    main()
