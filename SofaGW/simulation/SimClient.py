import sys
import xmlrpc.client
import pickle
import time
import os
import platform

# <SofaGuidewireNav>/SofaGW/simulation/../../
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+"/../../")
from SofaGW.utils import mkdir, root_dir, clear_folder, datasave, dataload
from SofaGW.simulation.scene import SOFA

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

class SimManager():
    def __init__(self, port_rpc, vessel_filename):
        # communication
        self.vessel_filename = vessel_filename
        self.port_rpc = port_rpc
        self.client = Client()
        self.client.connect(port_rpc)
        self.orderdict = None
        self.response = None
        # prepare directory used for communication
        self.commu_dir = root_dir + '/_cache_'
        # sofa
        self.sofa = SOFA(vessel_filename=vessel_filename)
    def getorder(self):
        """Get order from the server.
        orderdict = {'order': str(), # in str
                 'info': dict()}     # in dict
        """
        self.orderdict = self.client.dataget()
        self.response = {'data': dict(),}
    def execute(self):
        """Do proper process for order
        """
        order = self.orderdict.get('order', None)
        filename = self.commu_dir + f'/{self.port_rpc}_{str(time.time())[7:]}.pkl'
        self.response['data'] = {'filename': filename}
        close = False
        if order == 'close':
            close = True
        elif order == 'action':
            translation = self.orderdict['info'].get('translation', 0)
            rotation    = self.orderdict['info'].get('rotation',    0)
            self.sofa.action(translation=translation, rotation=rotation)
        elif order == 'step':
            realtime = self.orderdict['info'].get('realtime', True)
            errclose = self.sofa.step(realtime=realtime)
            self.response['data'] = {'errclose': errclose}
            close = errclose
        elif order == 'GetImage':
            image = self.sofa.GetImage()
            datasave(item=image, filename=filename)

        elif order == 'get_GW_position':
            GW_position = self.sofa.get_GW_position()
            datasave(item=GW_position, filename=filename)
        elif order == 'get_GW_velocity':
            GW_velocity = self.sofa.get_GW_velocity()
            datasave(item=GW_velocity, filename=filename)
        
        elif order == 'move_camera':
            filename = self.orderdict['info']['filename']
            data = dataload(filename=filename)
            position = data.get('position', None)
            lookAt = data.get('lookAt', None)
            orientation = data.get('orientation', None)
            self.sofa.move_camera(position=position,
                                  lookAt=lookAt,
                                  orientation=orientation,
                                  )
            

        else:
            raise Exception(f"Improper order. self.orderdict = {self.orderdict}")
        return close
    def respond(self):
        """Put response to the server.
        """
        self.client.dataput(self.response)


# This is run by runclient() in SimServer.
if __name__ == "__main__":
    print("[SimClient.py] Start SimClient.py")
    if len(sys.argv) != 3:
        print("[SimClient.py] SYNTAX: python client.py port_rpc vessel_filename")
        sys.exit(-1)
    port_rpc = sys.argv[1]
    vessel_filename = sys.argv[2]
    simmanager = SimManager(port_rpc=port_rpc, vessel_filename=vessel_filename)
    
    # Work as the order from the server.
    close = False
    while not close:
        # Get order from the server.
        simmanager.getorder()
        close = simmanager.execute()
        simmanager.respond()
    print("[SimClient.py] Close the simulation.")

