#!/bin/bash
dnf -y install dnf-plugins-core
dnf -y config-manager --add-repo https://brave-browser-rpm-release.s3.brave.com/x86_64/
rpm --import https://brave-browser-rpm-release.s3.brave.com/brave-core.asc
dnf -y install brave-keyring brave-browser
