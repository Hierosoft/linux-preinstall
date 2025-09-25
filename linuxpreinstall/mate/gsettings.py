#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Get or set any dconf setting using the Gio module in a similar way
as using the gsettings command.

by Sergiy Kolodyazhnyy
answered Aug 5, 2018 at 19:23
edited Jan 21, 2020 at 8:48
on <https://askubuntu.com/a/1062671>

Example:
gsettings_set('com.canonical.Unity.Launcher', 'launcher-position',
              'Bottom')

'''

from __future__ import print_function

import sys
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
# from subprocess import Popen


def echo0(*args, **kwargs):
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)
    return True


class GSettings:
    def __init__(self, schema):
        self.SCHEMA = schema
        self.settings = None
        self.settings_path = None

    def _init_settings(self, path):
        schema = self.SCHEMA
        if self.settings_path != path:
            if self.settings is not None:
                pass
                # echo0("* reinitializing settings path {} to {}"
                #       "".format(self.settings_path, path))
            self.settings = None
        if self.settings is None:
            if path is not None:
                self.settings = Gio.Settings.new_with_path(schema, path)
            else:
                self.settings = Gio.Settings.new(schema)
            self.settings_path = path

    def get_has_unapplied(self, path, key):
        self._init_settings(path)
        # if self.settings is None:
        #     logger.error("settings is not initialized. GSettings is"
        #           " not a subclass of Gio.Settings")
        #     return False
        return self.settings.get_has_unapplied()

    def _get(self, path, key):
        """Get value of gsettings schema"""
        self._init_settings(path)
        return self.settings.get_value(key)

    def _set(self, path, key, value):
        """Set value of gsettings schema"""
        self._init_settings(path)
        if isinstance(value, list):
            return self.settings.set_strv(key, value)
        if isinstance(value, int):
            return self.settings.set_int(key, value)
