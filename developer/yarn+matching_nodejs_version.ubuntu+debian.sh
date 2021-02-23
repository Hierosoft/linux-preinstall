#!/bin/sh

# sudo apt-get install -y nodejs
# ^ version is only 8.10.0
apt -y remove nodejs
apt -y autoremove
# (originally based on
# <https://computingforgeeks.com/installing-node-js-10-lts-on-ubuntu-18-04-16-04-debian-9/>
# and https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-18-04
# but yarnpkg.com says agt installs node automatically on Debian/Ubuntu)
# apt update
# apt -y install curl dirmngr apt-transport-https lsb-release ca-certificates
# curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
# as per post-install instructions (it already ran apt update):
# sudo apt -y install gcc g++ make  # to allow installing native plugins
# sudo apt-get install -y nodejs

# NOTE: The above was done and works (along with commands below).

# sudo apt-get install -y nodejs-dev node-gyp
# sudo apt-get install -y npm
# has error: "npm : Depends: node-gyp (>= 0.10.9) but it is not going to be installed"
# solution (below is from): https://askubuntu.com/questions/1088662/npm-depends-node-gyp-0-10-9-but-it-is-not-going-to-be-installed
# apt-get install nodejs-dev node-gyp libssl1.0-dev
# sudo apt-get install -y npm
apt -y remove nodejs-dev node-gyp libssl1.0-dev
apt -y remove npm
apg -y remove yarn
apt -y autoremove

# As per <https://classic.yarnpkg.com/en/docs/install/#debian-stable>:
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
apt update && sudo apt install yarn

sudo apt update && sudo apt install yarn

cat << END

"On Ubuntu 16.04 or below and Debian Stable, you will also need to
configure the [NodeSource repository](https://github.com/nodesource/distributions/blob/master/README.md#deb)
to get a new enough version of Node.js."

-<https://classic.yarnpkg.com/en/docs/install/#debian-stable>

END
