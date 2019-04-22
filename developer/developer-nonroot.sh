#!/bin/sh
git config --global credential.helper libsecret
# automatically edits:
# echo > ~/.gitconfig <<END
# [credential]
# helper = libsecret
# END
