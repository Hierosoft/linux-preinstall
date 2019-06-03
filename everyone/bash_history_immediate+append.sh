#!/bin/sh
echo "Special thanks: https://web.archive.org/web/20090815205011/http://www.cuberick.com/2008/11/update-bash-history-in-realtime.html"
touch ~/.bash_profile
echo "shopt -s histappend" >> ~/.bash_profile
echo 'PROMPT_COMMAND="history -a;$PROMPT_COMMAND"' >> ~/.bash_profile
echo "Done."
