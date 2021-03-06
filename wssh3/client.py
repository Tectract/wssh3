import sys

import gevent
from gevent.event import Event

from ws4py.exc import HandshakeError
from ws4py.client.geventclient import WebSocketClient

from . import common

# Handles the WebSocket once it has been upgraded by the HTTP layer.
class StdioPipedWebSocketClient(WebSocketClient):

    def __init__(self, scheme, host, port, path, opts):
        url = "{0}://{1}:{2}{3}".format(scheme, host, port, path)
        WebSocketClient.__init__(self, url)

        self.path = path
        self.shutdown_cond = Event()
        self.opts = opts
        self.iohelper = common.StdioPipedWebSocketHelper(self.shutdown_cond, opts)

    def received_message(self, m):
        self.iohelper.received_message(self, m)

    def opened(self):
#        print(self.opts)
#        if self.opts.verbosity >= 1:
#            peername, peerport = self.sock.getpeername()
#            print("[%s] %d open for path '%s'" % (peername, peerport, self.path))
        self.iohelper.opened(self)

    def closed(self, code, reason):
        self.shutdown_cond.set()

    def connect_and_wait(self):
        self.connect()
        self.shutdown_cond.wait()

def connect(args, scheme, host, port, path):
    if path == None:
        path = '/'
    client = StdioPipedWebSocketClient(scheme, host, port, path, args)
    try:
        client.connect_and_wait()
    except (IOError, HandshakeError) as e:
        print(e)
