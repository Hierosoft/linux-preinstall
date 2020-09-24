#!/bin/sh
# from https://www.cyberciti.biz/faq/how-to-find-my-public-ip-address-from-command-line-on-a-linux/
echo "WAN address (in a common home, your router is visible to the internet from this address):"
dig +short myip.opendns.com @resolver1.opendns.com
# dig TXT +short o-o.myaddr.l.google.com @ns1.google.com
