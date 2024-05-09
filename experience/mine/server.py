# server.py
import subprocess
import time
import os
import sys
import pickle
import socketserver
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn
import threading
import random

path = os.path.dirname(os.path.abspath(__file__)) + '/'
port_rpc = None

# class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
#     pass
class SimpleThreadedXMLRPCServer(SimpleXMLRPCServer):
    pass


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
    def log_message(self, format, *args):
        pass

class Server():
    def __init__(self):
        self.reset()
    def reset(self):
        self.data = None
        self.server2client = False
        self.client2server = False
    def setdata4client(self, data):
        self.data = data
        self.server2client = True
        self.client2server = False
    def setdata4server(self, data):
        self.data = data
        self.server2client = False
        self.client2server = True
    def getdata4client(self):
        self.wait4server()
        assert self.server2client == True
        data = self.data
        self.reset()
        return data
    def getdata4server(self):
        self.wait4client()
        assert self.client2server == True
        data = self.data
        self.reset()
        return data
    def wait4server(self):
        while not self.server2client:
            # print('wait4server')
            pass
    def wait4client(self):
        while not self.client2server:
            # print('wait4client')
            pass
    
# import queue
# class Server():
#     def __init__(self):
#         self.data_queue = queue.Queue()

#     def setdata4client(self, data):
#         self.data_queue.put(data)

#     def getdata4server(self):
#         return self.data_queue.get()

# Main function
def main():
    # Find a free port to connect a server.
    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]
        print('free_port :',free_port)
    port_rpc = free_port
    

    # Register functions
    server = Server()
    def dispatch(port_rpc, server):
        with SimpleThreadedXMLRPCServer(('localhost', port_rpc), requestHandler=RequestHandler) as s:
            s.register_instance(server)
            s.serve_forever()
    # Starts the server thread with the context.
    server_thread = threading.Thread(target=dispatch, args=(port_rpc,server))
    server_thread.daemon = True
    server_thread.start()

    
    
    i = -1
    while True:
        # Run the client
        def deferredStart():
            subprocess.run([sys.executable, path+"client.py", str(port_rpc)],
                            check=True)
        first_worker_thread = threading.Thread(target=deferredStart)
        first_worker_thread.daemon = True
        first_worker_thread.start()

        while random.random() < 0.8:
            i += 1
            print('i',i)
            # Send some data to the client
            data = {'command':'run','time':time.time(), 'i':i}
            server.setdata4client(data)

            # Get some data from the client
            data = server.getdata4server()
            print('client -> server :',data)

        # Send exit command
        data = {'command':'exit','time':time.time(), 'i':i}
        server.setdata4client(data)

        
        
if __name__ == "__main__":
    main()