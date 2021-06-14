import tornado.httpserver
import tornado.options
import tornado.ioloop
from tornado.options import options, define
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))
from connections.app import app

define(
    "port",
    default="9001",
    help="Default app port is 9001",
    type=int
)
define(
    "host",
    default="0.0.0.0",
    help="Default app host 0.0.0.0",
    type=str
)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_Server = tornado.httpserver.HTTPServer(
        app
    )
    http_Server.listen(
        options.port,options.host
    )
    tornado.ioloop.IOLoop.instance().start()
