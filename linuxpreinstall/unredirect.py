#!/usr/bin/env python3
'''
The unredirect module is part of linux-preinstall
by Jake "Poikilos" Gustafson

Purpose:
For each captioned hyperlink in Markdown format ("[...](...)"), check
for an implicit redirect (a query param has an encoded URL, that is,
any value in the query starting with http:// or https:// even if encoded
such as
`q=https%3A%2F%2Fblendermarket.com%2Fproducts%2FNatureClicker`)
or explicit redirect (302 error) and replace it with the final real
(direct) URL.

Usage:
  unredirect_md <markdown_path>
  # (If the destination isn't specified after that,
  # {no_redirects} will be added to the new filename).

Example:
  unredirect_md yt_video_description.md
  # ^ generates a new file with an automatically-generated name
  unredirect_md yt_video_description.md yt_video_description-no_re.md
  # ^ generates a new file called yt_video_description-no_re.md
'''

# The try/except clauses are from enissue.py except:
# - Added urlsplit

from __future__ import print_function
import sys
import os
python_mr = sys.version_info.major
'''
import json
import platform
import copy
from datetime import datetime, timedelta

if python_mr > 2:  # try:
    import urllib.request
    request = urllib.request
else:  # except ImportError:
    # Python 2
    print("* detected Python " + str(python_mr))
    import urllib2 as urllib
    request = urllib
'''



if python_mr > 2:
    from urllib.parse import urlparse
    from urllib.parse import urlsplit
    # from urllib.parse import quote_plus
    from urllib.parse import urlencode
    from urllib.parse import quote
    from urllib.parse import unquote  # this is the decode function
    from urllib.error import HTTPError

    try:
        import requests
    except ImportError:
        sys.stderr.write("If you try to use a token, you must have the"
                         " requests package for python3 such as via:\n"
                         "    sudo apt-get install python3-requests")
        sys.stderr.flush()
    from urllib.parse import parse_qs
else:
    # Python 2
    # See <https://docs.python.org/2/howto/urllib2.html>
    from urlparse import urlparse
    from urlparse import urlsplit
    # from urlparse import quote_plus
    from urllib import urlencode
    from urllib import quote
    from urllib import unquote  # this is the decode function
    from urllib2 import HTTPError
    # ^ urllib.error.HTTPError doesn't exist in Python 2
    try:
        import requests
    except ImportError:
        sys.stderr.write("If you try to use a token, you must have the"
                         " requests package for python2 such as via:\n"
                         "    sudo apt-get install python-requests")
        sys.stderr.flush()
    from urlparse import parse_qs


import requests

no_redirects = "-no_redirects"


def echo0(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# Based on <https://stackoverflow.com/a/20475639/4541104>:
def unredirect(url):
    '''
    Check for an explicit redirect (302 error) and return the real URL.

    Sequential arguments:
    url -- This URL may be direct (response 200) or a redirect (response
        302).
    '''
    r = requests.get(url)
    return r.url


def startsWithAny(haystack, needles):
    for needle in needles:
        if haystack.startswith(needle):
            return True
    return False


def unredirect_file(path, dest):
    '''
    For each captioned hyperlink in Markdown format ("[...](...)"),
    check for an implicit redirect (a query param has an encoded URL,
    that is, any value in the query starting with http:// or https://)
    or explicit redirect (302 error) and replace it with the final real
    (direct) URL.

    Sequential arguments:
    path -- the markdown file path that has redirects
    dest -- the markdown file path to write without redirects
    '''
    # opener2Plus = "&q=https%3A%2F%2"
    # opener2 = "&q="
    # closer2 = "&"
    # encOpeners = ["https%3A%2F%2", "http%3A%2F%2"]
    # ^ not necessary since urlsplit DOES DECODE the values
    decOpeners = ["https://", "http://"]
    opener = "]("
    openerPlus = "](http"
    closer = ")"
    with open(dest, 'w') as outs:
        with open(path, 'r') as ins:
            for rawL in ins:
                line = rawL.rstrip("\n\r")
                # ^ only strip newlines, since 2+ spaces at the end of a
                #   line in Markdown can mean a continuation in some
                #   flavor(s) or Markdown
                #   (https://stackoverflow.com/a/58465541/4541104).
                openI = line.find(openerPlus)
                closeI = -1
                if openI > -1:
                    closeI = line.find(closer, openI+len(openerPlus))
                if closeI > -1:
                    rawLink = line[openI+len(opener):closeI]
                    echo0("* processing {}".format(rawLink))
                    # pr = urlsplit(rawLink)  # get SplitResult

                    # See <https://stackoverflow.com/a/43628262/4541104>
                    query = urlsplit(rawLink).query
                    params = parse_qs(query)
                    # encLink = None
                    decLink = None
                    for k, values in params.items():
                        for v in values:
                            if startsWithAny(v, decOpeners):
                                decLink = v
                                '''
                                Why this is a list: probably since
                                The key may appear more than once, but
                                The answer isn't documented directly at
                                in the documentation:
                                <https://pd.codechef.com/docs/py/2.7.9/
                                library/urlparse.html>
                                nor <https://docs.python.org/3/
                                library/urllib.parse.html>
                                '''
                                # decLink = unquote(encLink)
                                # It is already decoded by urlsplit!
                                break
                            elif k == 'q':
                                msg = ("{} doesn't start with any of {}"
                                       "".format(v, encOpeners))
                                raise NotImplementedError(msg)
                    # if len(pr.query) > 0:
                    #     echo0(pr)
                    method = None
                    if decLink is None:
                        method = "unredirect"
                        url = unredirect(rawLink)
                        pass
                        # else:
                        #     echo0("  * unredirect: no change")
                    else:
                        method = "decoded"
                        url = decLink
                        # echo0("  * decoded: {}".format(url))
                    if url is not None:
                        line = (line[:openI+len(opener)] + url
                                + line[closeI:])
                        if url != rawLink:
                            echo0("  * {}: {}".format(method, url))

                outs.write(line + "\n")


def usage():
    echo0(__doc__.format(no_redirects=no_redirects))


def main():
    inFile = None
    if len(sys.argv) == 2:
        inFile = sys.argv[1]
    if len(sys.argv) == 3:
        inFile = sys.argv[1]
        outFile = sys.argv[2]

    if inFile is None:
        usage()
        echo0("Error: You must at least specify a Markdown file.")
    elif os.path.isfile(inFile):
        echo0('* reading "{}"'.format(inFile))
        fBase, fDotExt = os.path.splitext(inFile)
        if outFile is None:
            outFile = "{}{}{}".format(fBase, no_redirects, fDotExt)
        unredirect_file(inFile, outFile)
        echo0('* wrote "{}"'.format(outFile))
    else:
        usage()
        echo0('Error: "{}" does not exist'.format(inFile))


if __name__ == "__main__":
    main()
