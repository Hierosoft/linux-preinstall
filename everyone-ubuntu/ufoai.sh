#!/bin/sh
wget -q -O - http://archive.getdeb.net/getdeb-archive.key | sudo apt-key add -
sudo sh -c 'echo "deb http://archive.getdeb.net/ubuntu trusty-getdeb games" >> /etc/apt/sources.list.d/getdeb.list'
sudo apt-get update
sudo apt-get install ufoai
