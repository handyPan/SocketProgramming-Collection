# Author: Handy Pan
# Date: Feb 7, 2022
# Note: Modified based on https://developer-shubham-rasal.medium.com/create-simple-chat-app-using-udp-protocol-in-python-4539cdbb1ae1

# include the libraries to use
from socket import *
from threading import *
import os

# define the UDP socket, the local machine is run as both a server and a client using the same UDP socket
socket_client_server = socket(AF_INET, SOCK_DGRAM)

# bind the port for the local machine to run as UDP server
server_port = input("Please assign a port for local machine to work as Server:")
socket_client_server.bind(('',int(server_port)))

print("---------- Chat program based on UDP ----------")

# enter the name of the local person
name = input("ENTER YOUR NAME : ")
print("\nNote: Type 'bye' to exit.")

# enter the IP and port of the target machine, if to take the local machine as a UDP server, it will be our client
# fro the perspective of its own side on the other machine, it runs as a UDP server and the remote machine is the client
client_ip, client_port = input("Enter IP address and Port number of the target/Client machine: ").split()

# for the local machine to act as a client of the remote machine, sending messages
def send():
    while True:
        try:
            msg_s = input(">> ")
            if msg_s == "bye":
                msg_s = ''
                socket_client_server.sendto(msg_s.encode() , (client_ip,int(client_port)))
                socket_client_server.close()
                os._exit(1)
            msg_s = "{}  : {}".format(name,msg_s)
            socket_client_server.sendto(msg_s.encode() , (client_ip,int(client_port)))
        except:
            print("Error happens, quitted!")
            socket_client_server.close()
            os._exit(1)


# for the local machine to act as a server of the remote machine, receiving messages
def receive():
    while True:
        try:
            msg_r = socket_client_server.recvfrom(1024)
            if msg_r[0]==b'':
                socket_client_server.close()
                os._exit(1)
            print("\t\t\t\t >> " +  msg_r[0].decode() + "\n>> ",end='')
        except:
            print("Error happens, quitted!")
            socket_client_server.close()
            os._exit(1)

# create two threads, one will run as client (send) and another will run as server (receive)
th1 = Thread(target=send)
th2 = Thread(target=receive)

# start the threads
th1.start()
th2.start()
