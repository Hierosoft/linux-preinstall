#!/bin/sh
# See also: ./email-test.sh
FROM_NAME=$USER
TO_NAME=$USER
PORT=25
# STATED_HOST=`hostname`@`hostname -d`
STATED_HOST=`hostname --fqdn`
# ^ such as computer1.home.local or whatever you set during distro setup
#   or using `hostnamectl set-hostname`.
NET_HOST=`hostname --all-fqdns`
# ^ such as computer1.fios-router.home
echo "STATED_HOST=$STATED_HOST"
echo "NET_HOST=$STATED_HOST"
if [ "x$STATED_HOST" != "x$NET_HOST" ]; then
    cat <<END
Warning: STATED_HOST (defined by this computer) and NET_HOST (defined
  by router or other DNS) differ. the STATED_HOST will be used to avoid
  "Recipient address rejected: User unknown in local recipient table"
  (this probably doesn't matter).
END
fi
FROM_HOST=$STATED_HOST
TO_HOST=$STATED_HOST
FROM_ADDR=$USER@$pgs.home.local
TO_ADDR=$USER@pgs.home.local>
telnet $FROM_HOST $PORT <<END
EHLO localhost
MAIL FROM: <$FROM_ADDR>
RCPT TO: <$TO_ADDR>
DATA
From: "$FROM_NAME" <$FROM_ADDR>
To: "$TO_NAME" <$TO_ADDR>
Subject: test message sent from manual telnet session
Date: `date "+%a, %d %b %Y %k:%M:%S %z"`

Test message
from owner


.

QUIT

END
code=$?

# [enter].[enter] (actually CRLF.CRLF, even on linux, telnet says) ends the body.

if [ $code -eq 0 ]; then
    echo "Success"
else
    echo "Failed with code $?"
fi
