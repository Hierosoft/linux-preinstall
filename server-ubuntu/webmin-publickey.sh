#!/bin/sh
sudo su -
wget -q http://www.webmin.com/jcameron-key.asc -O- | apt-key add -
