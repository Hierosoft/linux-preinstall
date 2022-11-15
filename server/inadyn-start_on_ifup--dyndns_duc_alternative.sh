#!/bin/bash

INADYN="`command -v inadyn`"
if [ ! -f "$INADYN" ]; then
    >&2 echo "Error: inadyn must be installed first."
    exit 1
fi

ETC_CONF=/etc/inadyn.conf
OPT_CONF=/opt/inadyn.conf
THIS_SERVICE=inadynsvc
THIS_UP=/etc/network/if-up.d/$THIS_SERVICE
THIS_DOWN=/etc/network/if-post-down.d/$THIS_SERVICE
THIS_CONF="$ETC_CONF"
if [ -f "$OPT_CONF" ]; then
    echo "* detected $OPT_CONF so using that instead of $OPT_CONF. To use a different one, change that path in the following files:"
    echo "  - $THIS_UP"
    echo "  - $THIS_DOWN"
    THIS_CONF="$OPT_CONF"
fi

# Based on Simos Xenitellis (simosx)' 2007-09-27 answer on
#   <https://answers.launchpad.net/ubuntu/+question/13218>:

cat > $THIS_UP <<END
#!/bin/sh

if [ ! -x $INADYN ]; then
        exit 0
fi

if [ ! -r $THIS_CONF ]; then
        exit 0
fi

if [ "$METHOD" = loopback ]; then
        exit 0
fi

# Terminate any existing inadyn services running.
/usr/bin/killall -TERM inadyn

$INADYN --input_file $THIS_CONF &
# ^ without &, it causes a timeout and the networking service doesn't start!

exit $?
END

cat > $THIS_DOWN <<END
#!/bin/sh

if [ ! -x "$INADYN" ]; then
        exit 0
fi

if [ ! -r "$THIS_CONF" ]; then
        exit 0
fi

if [ "$METHOD" = loopback ]; then
        exit 0
fi

# Terminate any existing inadyn services running.
/usr/bin/killall -TERM inadyn

exit 0
END

if [
