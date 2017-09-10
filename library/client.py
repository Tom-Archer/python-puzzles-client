import socket
import pickle
import os

__author__ = 'christopherwildsmith'
__version__ = '0.0.1'

CONNECTION_PORT = 5003
DATA_PORT = 5004
BROADCAST_ADDRESS = '255.255.255.255'

class Client:

    def __init__(self):
        # self.addr = (BROADCAST_ADDRESS, self.port)
        self.clientIpAddr = self.get_device_ip_address()  # Get the IP Address of the Pi
        self.serverIPAddress = '255.255.255.255'  # Default to broadcast address

        self.connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create the socket
        self.connectionSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable reuse of the socket
        self.connectionSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcast messages
        self.connectionSocket.bind((self.clientIpAddr, CONNECTION_PORT))  # Bind the socket to the system IP address and port

        self.dataSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create the socket
        self.dataSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable reuse of the socket
        self.dataSocket.bind((self.clientIpAddr, DATA_PORT))  # Bind the socket to the system IP address and port
        # self.dataSocket.bind(('', DATA_PORT))  # Bind the socket to the system IP address and port

    def get_device_ip_address(self):
        gw = os.popen("hostname -I").read().split()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((gw[0], 0))
        ipaddr = s.getsockname()[0]
        print("Client IP Address: ", ipaddr)
        return ipaddr

    def connect(self, sTeamName):
        data = pickle.dumps([self.clientIpAddr, sTeamName])  # Pack the data to send
        addr = (BROADCAST_ADDRESS, CONNECTION_PORT)
        self.connectionSocket.sendto(data, addr)  # Send the data
        #print("Data Sent: " + str(data))

        bConnConf = False
        while not bConnConf:
            data, addr = self.connectionSocket.recvfrom(1024)
            sourceIPAddr, connStatus = pickle.loads(data)
            if connStatus == "Connection Confirmed":
                self.serverIPAddress = sourceIPAddr
                print("Connection Confirmed from: " + str(sourceIPAddr))
                bConnConf = True

    def send_data(self, dataIn):
        dataIn = pickle.dumps(dataIn)
        addr = (self.serverIPAddress, DATA_PORT)
        self.dataSocket.sendto(dataIn, addr)

    def receive_data(self):
        data, ip_addr = self.dataSocket.recvfrom(2048) # buffer size is 2048 bytes.
        #print("Data Received: " + str(data) + " from: " + str(ip_addr))
        data = pickle.loads(data)
        return data

    def __del__(self):
        self.connectionSocket.close()
        self.dataSocket.close()


if __name__ == "__main__":
    Client = Client()
    Client.connect("Team 1")
    data = Client.receive_data()
    data.sort()
    Client.send_data(data)