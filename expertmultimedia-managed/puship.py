#!/usr/bin/env python3
"""
This file sends computer info to <http://expertmultimedia/ping.php>.

Instead of this file, you can manually enter a hostname into
<http://expertmultimedia/whoami.php>.
"""
import socket

try:
    import urllib.request
    request = urllib.request
except ImportError:
    # python2
    python_mr = 2
    import urllib2 as urllib
    request = urllib

try:
    from urllib.parse import urlparse
    from urllib.parse import urlencode
    from urllib.parse import quote
    from urllib.parse import unquote
except ImportError:
    # python2
    from urlparse import urlparse
    from urllib import urlencode
    from urllib import quote
    from urllib import unquote

import urllib
import json

# See <https://stackoverflow.com/questions/17822158/how-to-get-an-utc-date-string-in-python>
# from datetime import datetime, timezone
# datetime.now(timezone.utc).strftime("%Y%m%d")
from datetime import datetime


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
    now_utc = datetime.utcnow()
    params["stated_hostname"] = socket.gethostname()
    # The server does:
    # - `params["updated_utc"] = now_utc.strftime(dt_fmt)`
    # - wan_ip
    # - wan_host
    params["stated_lan_ip"] = socket.gethostbyname(
        params["stated_hostname"]  # or socket.gethostname()
    )

    query_s = "{}?{}".format(ping_url, urlencode(params))
    # print(query_s)

    try:
        response = request.urlopen(query_s)
    except urllib.error.HTTPError as e:
        print("The URL \"{}\" is not accessible.".format(query_s))
        print(str(e))
        return None

    response_s = decode_safe(response.read())

    try:
        results = json.loads(response_s)
        print(results)
    except json.decoder.JSONDecodeError:
        print("The server sent invalid JSON:")
        print(response_s)

if __name__ == "__main__":
    main()
