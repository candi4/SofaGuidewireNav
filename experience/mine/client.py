# client.py
import sys
import xmlrpc.client
import time

if __name__ == "__main__":
    print("Start client.py")
    if len(sys.argv) != 2:
        print("SYNTAX: python client.py port_rpc")
        sys.exit(-1)
    port_rpc = sys.argv[1]

    # Register the instance to the manager
    s = xmlrpc.client.ServerProxy('http://localhost:' + port_rpc)
    print("Connected")


    # import sys
    # sys.path.append(r'C:\Users\82105\Dropbox\working\code_temp\SOFA_RL\Package/..')
    # from Package.scene import SOFA, SaveImage
    # sofa = SOFA()


    # for i in range(50):
    #     sofa.action(translation=1,rotation=0.1)
    #     sofa.step(realtime=False)
    #     image = sofa.GetImage()
    #     SaveImage(image, f'image/screen{i%50}.jpg')




    command = None
    while command != 'exit':
        # Get data from server
        data = s.serverget()
        command = data['command']
        print('server -> client :',data, time.time())

        # Send data to server
        data = {'state': time.time()}
        s.clientput(data)
    print("Exit")