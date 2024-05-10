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
import queue
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

    
class DataQueue():
    def __init__(self):
        self.server = queue.Queue() # server -> client
        self.client = queue.Queue() # client -> server
    def serverget(self):
        # print('serverget')
        return self.server.get()
    def serverput(self,data):
        # print('serverput')
        # assert self.server.empty()
        self.server.put(data)
        return 0
    def clientget(self):
        # print('clientget')
        return self.client.get()
    def clientput(self,data):
        # print('clientput')
        # assert self.client.empty()
        self.client.put(data)
        return 0


# Main function
def main():
    # Find a free port to connect a server.
    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]
        print('free_port :',free_port)
    port_rpc = free_port
    

    # Register functions
    dataqueue = DataQueue()
    def dispatch(port_rpc, dataqueue):
        with SimpleThreadedXMLRPCServer(('localhost', port_rpc), requestHandler=RequestHandler) as s:
            s.register_instance(dataqueue)
            s.serve_forever()
    # Starts the server thread with the context.
    server_thread = threading.Thread(target=dispatch, args=(port_rpc,dataqueue))
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
        time.sleep(1)

        command = None
        while command != 'exit':
            if random.random() < 0.8: command = 'run'
            else: command = 'exit'
            i += 1
            print('i',i)
            # Send some data to the client
            data = {'command':command,'time':time.time(), 'i':i}
            dataqueue.serverput(data)

            # Get some data from the client
            data = dataqueue.clientget()
            print('client -> server :',data, time.time())

        # exit command sent
        first_worker_thread.join() # Wait until client.py be finished.

        
        
if __name__ == "__main__":
    main()