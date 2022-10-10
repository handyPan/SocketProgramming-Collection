# Author: Handy Pan
# Date: Feb 6, 2022
# Note: Retrieved from the textbook 'Computer Networking：A Top-Down Approach, 8th Edition' with detailed comments given

# use the 'socket' module
from socket import *

# configure the server name and port, 'hostname' of the server might be not recognized, in that case, use IP address instead
serverName = '192.168.1.5'  # use the LAN IP 
serverPort = 12000

# create the client's socket, 'AF_INET' is the address family that indicates the underlying network is using IPv4; 'SOCK_DGRAM' indicates that the socket is a UDP type
clientSocket = socket(AF_INET, SOCK_DGRAM)

# for user to input message from keyboard
message = input('Input lowercase sentence:')

# send the message to the server; 
# the message is converted from string type to byte type by encode();
# sendto() attaches the destination address (serverName, serverPort) to the message and sends the resulting packet into the client process's socket
# the Internet will deliver the packet to the server address
clientSocket.sendto(message.encode(),(serverName, serverPort))

# receive the packets from the server, the buffer size is 2048 bytes
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# convert the received message from bytes to string and print out
print('From UDP Server: ', modifiedMessage.decode())

# close the socket
clientSocket.close()
