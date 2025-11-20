#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Sort the list of favorites using this command. Import this module to manually
instantiate BriskMenuSettings and get or set the list.
'''
from __future__ import print_function
import sys
import os
# if sys.version_info.major >= 3:
#     import functools  # Python 3
# import sys
import gi
gi.require_version("Gtk", "3.0")
# ^ MATE is now GTK 3
from gi.repository import (
    Gio,
    GLib,
)
from subprocess import Popen
# See <https://www.micahcarrick.com/gsettings-python-gnome-3.html>

if __name__ == "__main__":
    SUBMODULE_DIR = os.path.dirname(os.path.realpath(__file__))
    MODULE_DIR = os.path.dirname(os.path.dirname(SUBMODULE_DIR))
    sys.path.insert(0, os.path.dirname(MODULE_DIR))

from linuxpreinstall.lplogging import (
    echo0,
)

digits = "1234567890"


def my_func(instance, param):
    # See
    # <https://pygobject.readthedocs.io/en/latest/guide/api/properties.html>
    echo0("New value %r" % instance.get_property(param.name))


def sc_fn_to_name(sc_fn, to_lowercase=True):
    '''
    Get a sortable substring of a desktop filename.
    Examples:
    - org.minetest.minetest-logged.desktop becomes minetest-logged
    - appimagekit_1f378f83322537003449bd70bfb60a2e-Telegram_Desktop.desktop
      becomes Telegram_Desktop
    - net.scribus.Scribus.desktop becomes scribus
    Sequential arguments:
    sc_fn -- is a filename of a desktop file.
    '''
    sc_fn_raw = sc_fn
    sc_fn = os.path.split(sc_fn)[1]  # Get filename.
    sc_fn_lower = sc_fn.lower()
    if sc_fn_lower.endswith(".desktop"):
        # sc_fn_lower = os.path.splitext(sc_fn_lower)[0]
        sc_fn = os.path.splitext(sc_fn)[0]
    if sc_fn_lower.startswith("appimagekit_"):
        parts = sc_fn.split("-")
        if len(parts) > 1:
            sc_fn = parts[1]
        else:
            raise NotImplementedError(
                "The format is not recognized: {}"
                "".format(sc_fn_raw)
            )
    parts = sc_fn.split(".")
    fqn = sc_fn
    # ^ fully-qualified name including org (but not "flatpak_..." and not
    #   ".desktop").
    sc_fn = parts[-1]
    if len(parts) > 1:
        # otherwise it may be ok to start with a number, such as in
        # 4kvideodownloader
        if sc_fn[0] in digits:
            sc_fn = fqn
            # ^ Keep fqn since may be something like
            #   "blender-2.92"
    if to_lowercase:
        sc_fn = sc_fn.lower()
    # echo0("got {} from {}".format(sc_fn, sc_fn_raw))
    return sc_fn


def compare_sc_fn(item1, item2):
    item1 = sc_fn_to_name(item1)
    item2 = sc_fn_to_name(item2)
    if item1 < item2:
        return -1
    elif item1 > item2:
        return 1
    return 0


class BriskMenuSettings(Gio.Settings):
    '''
    A Gio.Settings handler implements dconf-settings.

    Example:
    <https://github.com/bilelmoussaoui/Authenticator>
    '''
    instance = None
    SCHEMA = "com.solus-project.brisk-menu"

    def __init__(self):
        Gio.Settings.__init__(self)

    @staticmethod
    def new():
        g_settings = Gio.Settings.new(BriskMenuSettings.SCHEMA)
        g_settings.__class__ = BriskMenuSettings
        return g_settings

    @staticmethod
    def get_default():
        if BriskMenuSettings.instance is None:
            BriskMenuSettings.instance = BriskMenuSettings.new()
        return BriskMenuSettings.instance

    @property
    def favs(self):
        return tuple(self.get_value('favourites'))

    @favs.setter
    def favs(self, favs):
        var = GLib.Variant('as', list(favs))
        # ^ a: array
        # ^ s: string
        self.set_value('favourites', var)

    def sort_favs(self):
        # if sys.version_info.major >= 3:
        #     self.favs = sorted(self.favs,
        #                        key=functools.cmp_to_key(compare_sc_fn))
        # else:
        self.favs = sorted(self.favs, key=sc_fn_to_name)


def main():
    settings = BriskMenuSettings.get_default()
    settings.sort_favs()
    favs = settings.favs
    # ^ gets the desktop filenames
    # print("favs: {}".format(favs))
    fav_names = [sc_fn_to_name(a) for a in favs]
    print("fav_names: {}".format(fav_names))
    echo0("Restarting mate-panel to complete the process...")
    _ = Popen(['mate-panel', '--replace'])
    return 0


if __name__ == "__main__":
    sys.exit(main())
