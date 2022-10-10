# Author: Handy Pan
# Date: Feb 6, 2022
# Note: Retrieved from the textbook 'Computer Networking：A Top-Down Approach, 8th Edition' with detailed comments given

# use the 'socket' module
from socket import *

# configure the server name and port, 'hostname' of the server might be not recognized, in that case, use IP address instead
serverName = '192.168.1.5'
serverPort = 12000

# create the client's socket, 'AF_INET' is the address family that indicates the underlying network is using IPv4; 'SOCK_STREAM' indicates that the socket is a TCP type
clientSocket = socket(AF_INET, SOCK_STREAM)

# initiate the TCP connection between the client and server
# the three-way handshake will be performed
clientSocket.connect((serverName,serverPort))

# for user to input message from keyboard
sentence = input('Input lowercase sentence:')

# send the sentence through the client's socket and into the TCP connection
# the program does not explicitly create a packet and attach the destination address to the packet
clientSocket.send(sentence.encode())

# receive the packets from the server, the buffer size is 2048 bytes
modifiedSentence = clientSocket.recv(1024)

# convert the received sentence from bytes to string and print out
print('From TCP Server: ', modifiedSentence.decode()) 

# close the socket
clientSocket.close()