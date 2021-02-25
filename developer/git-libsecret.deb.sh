#!/bin/sh
# See https://itectec.com/ubuntu/ubuntu-the-correct-way-to-use-git-with-gnome-keyring-and-https-repos/
apt-get install libsecret-1-0 libsecret-1-dev
# ls /usr/share/doc/git/contrib/credential/libsecret
# "git-credential-libsecret.c  Makefile"
sudo make --directory=/usr/share/doc/git/contrib/credential/libsecret
# ls /usr/share/doc/git/contrib/credential/libsecret
# "git-credential-libsecret    git-credential-libsecret.o
# git-credential-libsecret.c  Makefile"
git config --global credential.helper \
   /usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret
