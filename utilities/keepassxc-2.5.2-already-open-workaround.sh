#!/bin/sh
# See [Startup fails with error message "Another instance of KeePassXC is already running" #893](https://github.com/keepassxreboot/keepassxc/issues/893)
# Resolved in 2.5.3: [Correct latent single instance lock file preventing launch](https://github.com/keepassxreboot/keepassxc/commit/9ebe0b61ebf238b112a8d587dda06a1d8071a07f)
# TODO: ensure that the socket is actually dead before deleting the socket and lock files.
rm /tmp/keepassxc-$USER.*
