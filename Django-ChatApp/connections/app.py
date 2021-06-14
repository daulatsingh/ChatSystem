import os
import tornado.web
from connections.ws_connection import EchoWebSocket


class Application(tornado.web.Application):


    def __init__(self):
        handlers = [
            (r'/ws/$', EchoWebSocket),

        ]

        tornado.web.Application.__init__(self, handlers)


app = Application()
