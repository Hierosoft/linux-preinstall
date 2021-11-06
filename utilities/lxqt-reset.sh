#!/bin/bash
echo "This script attempts to fix the problem where the lxqt-panel has disappeared."
echo "In this condition, lxqt-panel may still appear in ps -a though it is not visible."
echo "See [lxqt-panel disappeared mysteriously [SOLVED]](https://bbs.archlinux.org/viewtopic.php?id=194560)"
rm ~/.config/lxqt/panel.conf
rm ~/.config/lxqt/panel.conf.lock
rm ~/.config/lxqt/panel.conf.*
