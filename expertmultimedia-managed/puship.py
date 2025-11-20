#!/usr/bin/env python3
"""
Send computer info to <http://expertmultimedia/ping.php>
to receive technical support.

Instead of this file, you can manually enter a hostname into
<http://expertmultimedia/whoami.php>.
"""
from __future__ import print_function

import json
import os
import socket
import sys
import urllib
# See <https://stackoverflow.com/questions/17822158/
#      how-to-get-an-utc-date-string-in-python>
# from datetime import datetime, timezone
# datetime.now(timezone.utc).strftime("%Y%m%d")
# from datetime import datetime

if sys.version_info.major >= 3:
    import urllib.request
    request = urllib.request
else:
    # Python 2
    import urllib2 as urllib  # type: ignore
    request = urllib

if sys.version_info.major >= 3:
    # from urllib.parse import urlparse
    from urllib.parse import urlencode
    # from urllib.parse import quote
    # from urllib.parse import unquote
else:
    # Python 2
    # from urlparse import urlparse
    from urllib import urlencode
    # from urllib import quote
    # from urllib import unquote

if __name__ == "__main__":
    MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, os.path.dirname(MODULE_DIR))

from linuxpreinstall.logging2 import (
    getLogger,
)

from linuxpreinstall.lplogging import (
    echo0,
)

logger = getLogger(__name__)

logger.warning(
    "Only use {} if you are a customer and want to share your IP!"
    .format(__name__))

ping_url = "http://expertmultimedia.com/ping.php"


def decode_safe(b):
    try:
        s = b.decode()
    except UnicodeDecodeError:
        s = b.decode('utf-8')
    return s


dt_fmt = "%Y-%m-%d %H:%M:%S"  # INFO: %z does nothing for some reason.


def main():
    params = {}
    # See <https://stackoverflow.com/questions/17822158/
    #      how-to-get-an-utc-date-string-in-python>
    # Works with Python 2 & 3:
    params["stated_hostname"] = socket.gethostname()

    # now_utc = datetime.utcnow()
    # - `params["stated_updated_utc"] = now_utc.strftime(dt_fmt)`
    # - wan_ip
    # - wan_host
    # ^ Instead, the server does the timestamp to ensure it is real

    params["stated_lan_ip"] = socket.gethostbyname(
        params["stated_hostname"]  # or socket.gethostname()
    )

    query_s = "{}?{}".format(ping_url, urlencode(params))
    # print(query_s)

    try:
        response = request.urlopen(query_s)
    except urllib.error.HTTPError as e:
        logger.error("The URL \"{}\" is not accessible.".format(query_s))
        logger.exception("")  # arg is custom msg for first line
        return None

    response_s = decode_safe(response.read())

    try:
        results = json.loads(response_s)
        print(results)
    except json.decoder.JSONDecodeError:
        logger.error("The server sent invalid JSON:")
        echo0(response_s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
