#!/bin/bash

# allow Xfce pulseaudio plugin to work:
sudo usermod -a -G audio $USER
sudo usermod -a -G pulse $USER
sudo usermod -a -G pulse-access $USER

