# Author: Handy Pan
# Date: Feb 6, 2022
# Note: Retrieved from the textbook 'Computer Networking：A Top-Down Approach, 8th Edition' with detailed comments given

# use the 'socket' module
from socket import *

# configure the server port
serverPort = 12000

# create the server's TCP socket
serverSocket = socket(AF_INET,SOCK_STREAM)

# bind the port number to the server's socket
# this specified socket will be the welcoming socket
serverSocket.bind(('',serverPort))

# after establishing the welcoming socket, wait and listen for TCP connection requests from the client
# the argument of listen() specifies the maximum number of queued connections (at least 1)
serverSocket.listen(1)

print('The TCP server is ready to receive')

# the server will receive and process packets from clients indefinitely
while True:
    # when a client requests TCP connection
    # accept() creates a new socket in the server named 'connectionSocket', which is dedicated to the particular client
    connectionSocket, addr = serverSocket.accept()

    # receive the packets from the client, the buffer size is 2048 bytes
    # convert the bytes to string 
    sentence = connectionSocket.recv(1024).decode()

    # capitalize the string
    capitalizedSentence = sentence.upper()

    # send the capitalized sentence through the server's socket and into the TCP connection
    connectionSocket.send(capitalizedSentence.encode()) 

    # close the connection socket
    connectionSocket.close()