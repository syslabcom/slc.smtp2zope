# > POST /Plone/mailrouter-inject HTTP/1.1
# > Authorization: Basic YWRtaW46YWRtaW4=
# > User-Agent: curl/7.19.7 (i486-pc-linux-gnu) libcurl/7.19.7 OpenSSL/0.9.8k zlib/1.2.3.3 libidn/1.15
# > Host: localhost:8080
# > Accept: */*
# > Content-Length: 197364
# > Content-Type: application/x-www-form-urlencoded
# > Expect: 100-continue

import sys
import logging
import httplib
from optparse import OptionParser

def main():

    parser = OptionParser()
    parser.add_option("-z", "--zope",
        help="Zope host name and port to submit email to, eg: localhost:8080")
    parser.add_option("-u", "--url",
        help="URL to submit email to, eg: /Plone/@@mailrouter-inject")
    parser.add_option("-v", "--verbose", default=0,
        action="count", help="Increase verbosity")

    (options, args) = parser.parse_args()

    # Check required options
    for option in (options.zope, options.url):
        if option is None:
            parser.print_help()
            sys.exit(1)

    # Configure logging
    # level works out at 30 (WARNING) if no -v given. For one -v, it drops
    # to 20 (INFO).
    logging.basicConfig(level=max(3-options.verbose,1)*10,
        format='%(asctime)s %(levelname)s %(message)s')

    message = sys.stdin.read()
    h = httplib.HTTPConnection(options.zope)
    h.request('POST', options.url, message)
    response = h.getresponse()
    status = response.status
    response = response.read()

    logging.info(response)

    # By default, exim will treat EX_TEMPFAIL (75) as a temporary error.
    # Postfix also treats 75 as temporary.
    # All other exit status' are permanent errors. This can be changed of
    # course. We shall therefore exit with status 75 if we want the MTA to
    # defer.

    # If a 2xx is returned, we exit status 0, delivery done.
    if status / 100 == 2:
        sys.exit(0)

    # If not found, permanent error
    if status == 404:
        sys.exit(1)

    # Otherwise, defer it, try again later.
    sys.exit(75)

if __name__ == "__main__":
    main()
