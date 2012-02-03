import tornado.ioloop
import tornado.web
from tornado.options import define, options

define("port", default=8888, help="port number for web serve")
define("text", default="Hellow world", help="This text will be put by server")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(options.text + "\n")

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(int(options.port))
    tornado.ioloop.IOLoop.instance().start()

    
