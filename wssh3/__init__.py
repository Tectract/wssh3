import gevent.monkey; gevent.monkey.patch_thread()
import sys
import threading
#if 'threading' in sys.modules:
#    raise Exception('threading module loaded before patching!')
#from urlparse import urlparse
from urllib.parse import urlparse
import argparse

from . import client
from . import server

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='URL', type=str,
            help='URL of a WebSocket endpoint with or without ws:// or wss://')
    parser.add_argument('-l', dest='listen', action='store_true', 
            help='start in listen mode, creating a server')
    parser.add_argument('-m', dest='text_mode', type=str, default='auto',
            choices=['text', 'binary', 'auto'],
            help='specify the message transmit mode (default: auto)')
    parser.add_argument('-n', dest='new_lines', action='store_true', 
            help='separate each received message with a newline')
    parser.add_argument('-q', dest='quit_on_eof', metavar='secs', type=int,
            help='quit after EOF on stdin and delay of secs (0 allowed)')
    parser.add_argument('-v', dest='verbosity', action='count',
            help='verbose (use up to 3 times to be more verbose)')
    args = parser.parse_args()

    url = args.url
    # Keep track of whether we are artificially assuming non-wss
    noscheme = False
    if not url.startswith("ws://") and not url.startswith("wss://"):
        noscheme = True
        url = "ws://{0}".format(url)
    url = urlparse(url)

    # If we added non-wss ourselves but the user picked port 443, they almost certainly wanted wss
    if noscheme and url.port == 443:
        url = urlparse("wss://{0}:443{1}".format(url.hostname, url.path))

    port = url.port
    # Apply an appropriate default port.
    if port == None:
        if url.scheme == "wss":
            port = 443
        else:
            port = 80

    # Translate an empty path to None, triggering the default behaviour for
    # both client and server (which differ in their treatment of the default
    # case).
    path = url.path
    if url.path == '':
        path = None
    elif url.query:
        path = "{0}?{1}".format(path, url.query)

    try:
        if args.listen:
            server.listen(args, port, path)
        else:
            client.connect(args, url.scheme, url.hostname, port, path)
    except KeyboardInterrupt:
        pass
