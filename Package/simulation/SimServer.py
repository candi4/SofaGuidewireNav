import subprocess
import os
import sys
import socketserver
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
import queue
import time

class Server():
    def __init__(self, timeout=None):
        self.port_rpc = None
        self.clientfile = os.path.dirname(os.path.abspath(__file__)) + '/SimClient.py'
        self.timeout = timeout
    def start(self):
        self.setport()
        self.data = Server.Data(timeout=self.timeout)
        self.startthread()
    def setport(self):
        # Find a free port to connect a server.
        with socketserver.TCPServer(("localhost", 0), None) as s:
            free_port = s.server_address[1]
            print('free_port :',free_port)
        self.port_rpc = free_port

    class CustomQueue(queue.Queue):
        def __init__(self):
            queue.Queue.__init__(self)
            self.len = 0
        def put(self, item, timeout=None):
            queue.Queue.put(self, item, timeout=timeout)
            self.len += 1
        def get(self, timeout=None):
            res = queue.Queue.get(self, timeout=timeout)
            self.len -= 1
            return res
        def __len__(self):
            return self.len

    class Data():
        def __init__(self, timeout=None):
            self.timeout = timeout
            self.serverdata = Server.CustomQueue() # server -> client
            self.clientdata = Server.CustomQueue() # client -> server
        def serverget(self):
            res = self.serverdata.get(timeout=self.timeout)
            assert len(self.serverdata) == 0
            return res
        def serverput(self,item):
            self.serverdata.put(item, timeout=self.timeout)
            assert len(self.serverdata) == 1
            return 0
        def clientget(self):
            res = self.clientdata.get(timeout=self.timeout)
            assert len(self.clientdata) == 0
            return res
        def clientput(self,item):
            self.clientdata.put(item, timeout=self.timeout)
            assert len(self.clientdata) == 1
            return 0
    def dataput(self, item):
        # Send some data to the client.
        return self.data.serverput(item)
    def dataget(self):
        # Get some data from the client.
        return self.data.clientget()
    
    class SimpleThreadedXMLRPCServer(SimpleXMLRPCServer):
        pass
    # Restrict to a particular path.
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)
        def log_message(self, format, *args):
            pass
    def startthread(self):
        # Register functions
        def dispatch(port_rpc, dataqueue):
            with self.SimpleThreadedXMLRPCServer(('localhost', port_rpc), requestHandler=self.RequestHandler) as s:
                s.register_instance(dataqueue)
                s.serve_forever()
        # Starts the server thread with the context.
        server_thread = threading.Thread(target=dispatch, args=(self.port_rpc,self.data))
        server_thread.daemon = True
        server_thread.start()
    def runclient(self):
        # Run the client
        def deferredStart(path, port_rpc):
            subprocess.run([sys.executable, path, str(port_rpc)],
                            check=True)
        self.first_worker_thread = threading.Thread(target=deferredStart, args=(self.clientfile, self.port_rpc))
        self.first_worker_thread.daemon = True
        self.first_worker_thread.start()
        time.sleep(1)
    def waitclientclose(self):
        # exit command was aleady sent
        self.first_worker_thread.join() # Wait until client.py be finished.
        



# For test.
if __name__ == "__main__":
    import time
    import random

    server = Server(timeout=10)
    server.start()

    
    i = -1
    while True:
        server.runclient()

        command = None
        while command != 'exit':
            if random.random() < 0.8: command = 'run'
            else: command = 'exit'
            i += 1
            print('i',i)
            
            # Get some data from the client.
            data = server.dataget()
            print('client -> server :',data, time.time())
            
            # Send some data to the client.
            data = {'command':command,'time':time.time(), 'i':i}
            server.dataput(data)

        # Close client. Closing client is decided by server.
        pass

        server.waitclientclose()