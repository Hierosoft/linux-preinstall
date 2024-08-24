# Based on hierosoft.sysdirs, but using a subclass
#  (eventually that should as well).
import os
import platform

from linuxpreinstall.readonlydict import ReadOnlyDict

from linuxpreinstall import (
    echo0,
)
# sysfiles = ReadOnlyDict()


class SystemPaths(ReadOnlyDict):
    def init_platform(self, os_name, home=None):
        self['PROFILES'] = "/home"
        if os_name == "Darwin":
            self['PROFILES'] = "/Users"
        elif os_name == "Windows":
            self['PROFILES'] = "C:\\Users"

        if os_name == "Windows":
            if not home:
                home = os.environ['USERPROFILE']
            self['HOME'] = home
            self['SYSLOG_CONF'] = \
                os.path.join(self['HOME'], 'syslog.conf')  # dummy entry
            self['LOCALAPPDATA'] = os.environ['LOCALAPPDATA']  # formerly local
            self['CACHES'] = os.path.join(self['LOCALAPPDATA'], "Caches")
            self['LOGS'] = os.path.join(self['LOCALAPPDATA'])  # , "logs")
        else:
            if not home:
                home = os.environ['HOME']
            self['HOME'] = home
            if os_name == "Darwin":
                # self['SYSLOG_CONF'] = \
                #     '/usr/local/etc/rsyslog.conf'  # from Homebrew
                self['SYSLOG_CONF'] = '/etc/rsyslog.conf'  # valid on macOS
                self['LOCALAPPDATA'] = os.path.join(self['HOME'], ".local",
                                                    "share")  # .net Core-like
                #  according to <https://www.eventsentry.com/kb/449-how-do-i-
                #  send-syslog-messages-from-macos-to-eventsentry>
                self['CACHES'] = os.path.join(self['HOME'], "Library",
                                              "Caches")  # .net Core-like
                self['LOGS'] = os.path.join(self['HOME'], "Library", "Logs")
                # ^ Ensure LOGS is ok to be written manually & unstructured
                #   since
                #   <https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/MacOSXDirectories/MacOSXDirectories.html>  # noqa: E501
                #   says, ". . . Users can also view these logs using the
                #   Console app."

            else:  # Linux-like
                self['LOCALAPPDATA'] = os.path.join(self['HOME'], ".local",
                                                    "share")  # .net-like
                self['CACHES'] = os.path.join(self['HOME'], ".cache")
                self['SYSLOG_CONF'] = '/etc/syslog.conf'
                if os.path.isfile('/etc/rsyslog.conf'):
                    self['SYSLOG_CONF'] = '/etc/rsyslog.conf'
                self['LOGS'] = os.path.join(self['HOME'], ".var", "log")

        _, self['USER_DIR_NAME'] = os.path.split(self['HOME'])
        # self['PROFILES'] = _
        # FIXME: ^ wrong in moreplatform since may be ['/', 'root'] !
        # ^ Also done by generate_exclude.py

    def sanity_check(self):
        pass

    def init_cloud(self):
        pass

    def check_cloud(self):
        pass


sysdirs = SystemPaths()  # Call .readonly() after vars are set below.
sysdirs.init_platform(platform.system())
echo0("Finished init_platform.")  # don't interfere with stdout such as whichicon
sysdirs.sanity_check()
sysdirs.init_cloud()
sysdirs.check_cloud()
sysdirs.readonly()

# sysfiles.readonly()
# echo0("Finished sysfiles.")