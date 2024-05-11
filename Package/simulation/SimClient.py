import sys
import xmlrpc.client


# sys.path.append(r'C:\Users\82105\Dropbox\working\code_temp\SOFA_RL\Package/..')
# from Package.scene import SOFA, SaveImage

class Client():
    def __init__(self):
        self.port_rpc = None
    def connect(self, port_rpc):
        self.port_rpc = port_rpc
        # Register the instance to the manager
        self.server = xmlrpc.client.ServerProxy('http://localhost:' + port_rpc)
        print("Connected")
    def dataput(self, item):
        # Send data to server.
        return self.server.clientput(item)
    def dataget(self):
        # Get data from server.
        return self.server.serverget()


# This is run by runclient() in SimServer.
if __name__ == "__main__":
    print("Start SimClient.py")
    if len(sys.argv) != 2:
        print("SYNTAX: python client.py port_rpc")
        sys.exit(-1)
    port_rpc = sys.argv[1]

    client = Client()
    client.connect(port_rpc)



    # sofa = SOFA()
    # for i in range(50):
    #     sofa.action(translation=1,rotation=0.1)
    #     sofa.step(realtime=False)
    #     image = sofa.GetImage()
    #     SaveImage(image, f'image/screen{i%50}.jpg')



    import time
    command = None
    while command != 'exit':
        # Get data from server.
        data = client.dataget()
        command = data['command']
        print('server -> client :',data, time.time())

        # Send data to server.
        data = {'state': time.time()}
        client.dataput(data)
    print("Exit")