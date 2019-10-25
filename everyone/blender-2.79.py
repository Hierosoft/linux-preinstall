#!/usr/bin/env python
import requests
import os
import tarfile
import sys

my_dir = os.path.dirname(os.path.realpath(__file__))
repo_dir = os.path.dirname(my_dir)
utilities_dir = os.path.join(repo_dir, "utilities")

# installer module:
im_path = os.path.join(utilities_dir, "install_any.py")
im_name = "install_any"

if not os.path.isfile(im_path):
    print("'{}' is missing.".format(im_path))
    exit(1)


# Did not work (no module named util):
# Sebastian Rittau's answer https://stackoverflow.com/a/67692 to
# <https://stackoverflow.com/questions/67631/\
# how-to-import-a-module-given-the-full-path>
# See Sebastian Rittau's answer https://stackoverflow.com/a/67692 to
# <https://stackoverflow.com/questions/67631/\
# how-to-import-a-module-given-the-full-path>
# try:
    # import importlib.util
    # spec = importlib.util.spec_from_file_location(im_name, im_path)
    # im = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(im)
    # im.MyClass()
# except ImportError:  # no module named util
    # try:
        # # For Python 3.3 and 3.4 use:
        # from importlib.machinery import SourceFileLoader
        # im = SourceFileLoader(im_name, im_path).load_module()
        # im.MyClass()
        # # (Although this has been deprecated in Python 3.4.)
    # except AttributeError:
        # # For Python 2 use:
        # import imp
        # im = imp.load_source(im_name, im_path)
        # im.MyClass()
# so instead:

# See Jacob Vlijm's answer https://askubuntu.com/a/471168 at
# <https://askubuntu.com/questions/470982/\
# how-to-add-a-python-module-to-syspath>
sys.path.insert(0, utilities_dir)
import install_any as im

remote_dir = "https://download.blender.org/release/Blender2.79/latest/"
file_name = "blender-2.79-e045fe53f1b0-linux-glibc217-x86_64.tar.bz2"
if "e045fe53f1b0" in file_name:
    print("* installing last 2.79 nightly build (has fixes from 2.80)")
extracted_name = "blender-2.79-e045fe53f1b0-linux-glibc217-x86_64"
url = remote_dir + file_name
downloads = os.path.join(os.environ["HOME"], "Downloads")
dl_path = os.path.join(downloads, file_name)


extracted_path = os.path.join(downloads, extracted_name)

if not os.path.isdir(extracted_path):
    if not os.path.isfile(dl_path):
        # see https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
        with open(dl_path, "wb") as f:
            print "Downloading %s" % dl_path
            response = requests.get(url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None: # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                    sys.stdout.flush()
    else:
        print("* using existing '{}'".format(dl_path))

    print("* extracting '{}'".format(dl_path))
    tar = tarfile.open(dl_path, "r:bz2")
    tar.extractall(downloads)
    tar.close()
    if not os.path.isdir(extracted_path):
        print(
            "ERROR: extracting '{}' did not result in '{}'".format(
                dl_path,
                extracted_path
            )
        )
        exit(1)
else:
    print("* using existing '{}'".format(extracted_path))

ext_bin_path = os.path.join(extracted_path, "blender")

print("* {} will now install '{}'...".format(im_name, ext_bin_path))

im.install_program_in_place(ext_bin_path, caption="Blender 2.79")
