# client.py
import sys
import xmlrpc.client


if __name__ == "__main__":
    print("Start client.py")
    if len(sys.argv) != 2:
        print("SYNTAX: python client.py port_rpc")
        sys.exit(-1)
    port_rpc = sys.argv[1]

    # Register the instance to the manager
    s = xmlrpc.client.ServerProxy('http://localhost:' + port_rpc)
    print("Connected")


    command = None
    while command != 'exit':
        # Get data from server
        print('before')
        data = s.getdata4client()
        print('after')
        command = data['command']
        print('server -> client :',data)

        # Send data to server
        data = {'state': 1}
        s.setdata4server(data)
    print("Exit")