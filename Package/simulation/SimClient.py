import sys
import xmlrpc.client
import pickle
import time
import os
import platform

# <GuidewireNavRL>/Package/simulation/../../
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+"/../../")
from Package.utils import mkdir, root_dir
from Package.simulation.scene import SOFA

class Client():
    def __init__(self):
        self.port_rpc = None
    def connect(self, port_rpc):
        self.port_rpc = port_rpc
        # Register the instance to the manager
        if platform.system().lower() == 'windows':
            self.server = xmlrpc.client.ServerProxy('http://127.0.0.1:' + port_rpc)
        else:
            self.server = xmlrpc.client.ServerProxy('http://localhost:' + port_rpc)
        print("[SimClient.py] Connected")
    def dataput(self, item):
        # Send data to the server.
        return self.server.clientput(item)
    def dataget(self):
        # Get data from the server.
        return self.server.serverget()
    def datasave(self, item, filename):
        mkdir(filename=filename)
        with open(filename, 'wb') as f:
            pickle.dump(item, f)


# This is run by runclient() in SimServer.
if __name__ == "__main__":
    print("[SimClient.py] Start SimClient.py")
    if len(sys.argv) != 2:
        print("[SimClient.py] SYNTAX: python client.py port_rpc")
        sys.exit(-1)
    port_rpc = sys.argv[1]

    client = Client()
    client.connect(port_rpc)

    # Initialize sofa
    sofa = SOFA()
    sofa.step(realtime=False)

    # Work as the order from the server.
    close = False
    while not close:
        # Get order from the server.
        order = client.dataget()
        # order = {'ordername': str(), # in str
        #          'info': dict()}     # in dict
        response = {'data': dict(),}   # in dict
        if order['ordername'] == 'close':
            close = True
        elif order['ordername'] == 'action':
            translation = order['info'].get('translation', 0)
            rotation    = order['info'].get('rotation',    0)
            sofa.action(translation=translation, rotation=rotation)
        elif order['ordername'] == 'step':
            realtime = order['info'].get('realtime', True)
            sofa.step(realtime=realtime)
        elif order['ordername'] == 'GetImage':
            image = sofa.GetImage()
            filename = root_dir + f'/delete/image_{time.time()}.pkl'
            client.datasave(item=image, filename=filename)
            response['data'] = {'filename': filename}
        # Put response to the server.
        client.dataput(response)
    print("[SimClient.py] Close the simulation.")

