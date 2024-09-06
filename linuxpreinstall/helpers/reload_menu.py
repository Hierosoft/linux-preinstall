#!/usr/bin/env python3
from __future__ import print_function

import psutil
import sys


def detect_desktop_environment():
    """Detect the running Desktop Environment and return a dictionary with DE name and message."""
    if is_process_running("cinnamon"):
        return {
            'de': 'Cinnamon',
            'msg': 'You may have to restart your DE such as via Alt+F2, cinnamon --replace.'
        }
    elif is_process_running("mate-panel"):
        return {
            'de': 'MATE',
            'msg': 'You may need to restart your DE such as via Alt+F2, mate-panel --replace.'
        }
    elif is_process_running("plasmashell"):
        return {
            'de': 'KDE',
            'msg': 'You may need to restart your DE such as via Alt+F2, kquitapp5 plasmashell && kstart5 plasmashell.'
        }
    elif is_process_running("gnome-shell"):
        return {
            'de': 'GNOME',
            'msg': 'You may need to restart your DE such as via Alt+F2, r.'
        }
    return {'error': 'No recognized Desktop Environment detected'}


def is_process_running(process_name):
    """Check if a process with the given name is running."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False


def main():
    result = detect_desktop_environment()
    if 'error' in result:
        print(result['error'])
        return 1
    else:
        print("{} detected.".format(result['de']))
        print(result['msg'])
        return 0


if __name__ == "__main__":
    sys.exit(main())
