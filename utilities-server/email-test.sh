#!/bin/sh
# See also: ./postfix-local_telnet_test.sh
if [ ! -f "`command -v mail`" ]; then
    echo "You must first install the mailutils package."
    exit 1
fi
# HOST=`hostname`
# LOCAL_DOMAIN=`hostname -d`
HOST_DOT_LOCAL_DOMAIN=`hostname --fqdn`
code=$?
if [ $code -ne 0 ]; then
    exit $code
fi
# --fqdn: same as $HOST.$LOCAL_DOMAIN
echo "Test mail from postfix" | mail -s "Test Postfix" $USER@$HOST_DOT_LOCAL_DOMAIN
