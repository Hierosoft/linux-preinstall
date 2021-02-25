#!/bin/sh

# See https://itectec.com/ubuntu/ubuntu-the-correct-way-to-use-git-with-gnome-keyring-and-https-repos/
git config --global credential.helper \
   /usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret

# Also, the following seems to work:
# git config --global credential.helper libsecret
