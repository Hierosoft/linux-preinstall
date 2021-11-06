#!/bin/sh
# see brx75x's shell-only alternative on https://www.commandlinefu.com/commands/view/11336/create-a-continuous-digital-clock-in-linux-terminal
while [ 1 ] ; do echo -en "$(date +%T)\r" ; sleep 1; done
