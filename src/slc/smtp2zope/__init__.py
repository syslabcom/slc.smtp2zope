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
import http.client
import socket
from optparse import OptionParser


def main():

    parser = OptionParser()
    parser.add_option(
        "-z",
        "--zope",
        help="Zope host name and port to submit email to, eg: localhost:8080",
    )
    parser.add_option(
        "-u", "--url", help="URL to submit email to, eg: /Plone/@@mailrouter-inject"
    )
    parser.add_option(
        "-v", "--verbose", default=0, action="count", help="Increase verbosity"
    )

    (options, args) = parser.parse_args()

    # Check required options
    for option in (options.zope, options.url):
        if option is None:
            parser.print_help()
            sys.exit(1)

    # Configure logging
    # level works out at 30 (WARNING) if no -v given. For one -v, it drops
    # to 20 (INFO).
    logging.basicConfig(
        level=max(3 - options.verbose, 1) * 10,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    message = sys.stdin.read()
    try:
        h = http.client.HTTPConnection(options.zope)
        h.request("POST", options.url, message)
        response = h.getresponse()
    except http.client.BadStatusLine as bsl:
        logging.info("BadStatusLine: %s" % bsl)
        sys.exit(78)  # EX_CONFIG
    except (socket.error, socket.timeout, http.client.HTTPException) as e:
        logging.error(e)
        sys.exit(75)  # EX_TEMPFAIL
    status = response.status
    response = response.read()

    # By default, exim will treat EX_TEMPFAIL (75) as a temporary error.
    # Postfix also treats 75 as temporary.
    # All other exit status' are permanent errors. This can be changed of
    # course. We shall therefore exit with status 75 if we want the MTA to
    # defer.

    # If a 2xx is returned, we exit status 0, delivery done.
    if status / 100 == 2:
        logging.info(response)
        sys.exit(0)

    # If status is not 200, the response should hold an error message
    logging.error(response)
    # If not found, permanent error
    if status == 401:
        sys.exit(77)  # EX_NOPERM
    if status == 404:
        sys.exit(67)  # EX_NOUSER
    if status / 100 == 4:
        sys.exit(78)  # EX_CONFIG

    # Otherwise, defer it, try again later.
    sys.exit(75)  # EX_TEMPFAIL
