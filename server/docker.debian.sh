#!/bin/bash
# See <https://docs.docker.com/engine/install/debian/>:
if [ "@$1" = "@--uninstall" ]; then
    apt-get remove -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    exit $?
fi
apt-get remove -y docker
apt-get remove -y docker.io
apt-get remove -y containerd
apt-get remove -y runc
apt-get remove -y docker-engine
# ^ Not on Devuan 4 Chimera (based on Debian 11 Bullseye)
apt-get update
apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# "Use the following command to set up the stable repository. To add
# the nightly or test repository, add the word nightly or test (or both)
# after the word stable in the commands below. Learn about nightly and
# test channels."

lsb_release_name="$(lsb_release -cs)"
if [ "@$lsb_release_name" = "@chimera" ]; then
    # Devuan 4 Chimera is based on Debian 11 Bullseye
    lsb_release_name=bullseye
fi

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
   $lsb_release_name stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
if [ $? -ne 0 ]; then
    # "Your default umask may not be set correctly, causing the
    # public key file for the repo to not be detected. Run the following
    # command and then try to update your repo again:"
    chmod a+r /usr/share/keyrings/docker-archive-keyring.gpg
fi
apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
# "Install a specific version using the version string from the second
# column, for example, 5:18.09.1~3-0~debian-stretch .
# sudo apt-get install docker-ce=<VERSION_STRING> docker-ce-cli=<VERSION_STRING> containerd.io docker-compose-plugin
docker run hello-world
