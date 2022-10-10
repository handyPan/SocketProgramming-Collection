# Author: Handy Pan
# Date: Feb 6, 2022
# Note: Retrieved from the textbook 'Computer Networking：A Top-Down Approach, 8th Edition' with detailed comments given


# use the 'socket' module
from socket import *

# configure the server port
serverPort = 12000

# create the server's UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# bind the port number to the server's socket
# the packets to this specified port will be directed to this socket
serverSocket.bind(('', serverPort))

print('The UDP server is ready to receive')

# the server will receive and process packets from clients indefinitely
while True:
    # receive the packets from the client, the buffer size is 2048 bytes
    message, clientAddress = serverSocket.recvfrom(2048)

    # convert the message from bytes to string and capitalize it
    modifiedMessage = message.decode().upper()

    # send the message to the server process's socket;
    # the Internet will deliver the packet to the client address;
    serverSocket.sendto(modifiedMessage.encode(),
    clientAddress)
