import socket
import pickle
import os

__author__ = 'christopherwildsmith'
__version__ = '0.0.1'

CLIENT_CONNECTION_PORT = 5003
CLIENT_DATA_PORT = 5004
SERVER_CONNECTION_PORT = 6003
SERVER_DATA_PORT = 6004
BROADCAST_ADDRESS = '255.255.255.255'

class Client:

    def __init__(self):
        self.clientIpAddr = self.get_device_ip_address()  # Get the IP Address of the Pi
        self.serverIPAddress = '255.255.255.255'  # Default to broadcast address

        self.connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create the socket
        self.connectionSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable reuse of the socket
        self.connectionSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable broadcast messages
        self.connectionSocket.bind((self.clientIpAddr, CLIENT_CONNECTION_PORT))  # Bind the socket to the system IP address and port

        self.dataSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create the socket
        self.dataSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable reuse of the socket
        self.dataSocket.bind((self.clientIpAddr, CLIENT_DATA_PORT))  # Bind the socket to the system IP address and port
        # self.dataSocket.bind(('', DATA_PORT))  # Bind the socket to the system IP address and port

    def get_device_ip_address(self):
        gw = os.popen("hostname -I").read().split()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((gw[0], 0))
        ipaddr = s.getsockname()[0]
        print("Client IP Address: ", ipaddr)
        return ipaddr

    def connect(self, sTeamName):
        #print("Data Sent: " + str(data))
        data = pickle.dumps([self.clientIpAddr, sTeamName])  # Pack the data to send
        addr = (BROADCAST_ADDRESS, SERVER_CONNECTION_PORT)
        self.connectionSocket.sendto(data, addr)  # Send the data

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
        addr = (self.serverIPAddress, SERVER_DATA_PORT)
        self.dataSocket.sendto(dataIn, addr)

    def receive_data(self):
        data, ip_addr = self.dataSocket.recvfrom(4096)
        data = pickle.loads(data)
        #print("Data Received: " + str(data) + " from: " + str(ip_addr))
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