#!/bin/sh

# which says to do (I added --refresh & -y & changed from yum to dnf):

## Your system appears to already have Node.js installed from an alternative source.
# Run `sudo yum remove -y nodejs npm` to remove these first.
sudo dnf remove -y nodejs npm

## Run `sudo yum install -y nodejs` to install Node.js 12.x and npm.
sudo dnf install -y nodejs --refresh
## You may also need development tools to build native addons:
     sudo dnf install -y gcc-c++ make
## To install the Yarn package manager, run:
     curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | sudo tee /etc/yum.repos.d/yarn.repo
     sudo dnf install -y yarn
