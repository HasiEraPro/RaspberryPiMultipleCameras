from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
import os

def on_file_received(self, file):
    # do something when a file has been received
    print("File recived")

authorizer = DummyAuthorizer()
authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
authorizer.add_anonymous(os.getcwd())
handler = FTPHandler
handler.on_file_received = on_file_received
handler.authorizer = authorizer

address = ('127.0.0.1', 2121)
server = FTPServer(address, handler)




server.serve_forever()