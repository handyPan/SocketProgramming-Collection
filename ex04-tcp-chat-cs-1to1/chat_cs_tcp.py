# Author: Handy Pan
# Date: Feb 7, 2022

from socket import *
from threading import *
import os


print("\n---------- Chat program based on TCP ----------\n")

local_server_port = input("Please assign a port for local machine to work as Server:")

welcome_socket = socket(AF_INET, SOCK_STREAM)
welcome_socket.bind(('',int(local_server_port)))
welcome_socket.listen(1)
print("Welcome socket connection established, start listening!" if welcome_socket.fileno()!=-1 else "Welcome socket connection failed!")

name = input("ENTER YOUR NAME : ")
print("Note: Type 'bye' to exit.")

target_server_ip, target_server_port = input("Enter IP address and Port number of the target Server machine: ").split()

# for TCP connection
try:
    local_client_socket = socket(AF_INET, SOCK_STREAM)
    local_client_socket.connect((target_server_ip, int(target_server_port)))
    print("Local client socket connection established!" if local_client_socket.fileno()!=-1 else "Local client socket connection failed!")
except:
    print("Local client socket connection failed!Make sure the target machine is run as a server as well.")

def send():
    while True:
        try:
            # the code to send messages, shutdown connection if "bye" is typed in
            msg_s = input(">> ")
            if msg_s == "bye":
                local_client_socket.close()
                print("Local client socket connection failed!")
                os._exit(1)
            msg_s = "{}  : {}".format(name,msg_s)
            local_client_socket.send(msg_s.encode())
        except:
            print("Connection failed!")
            local_client_socket.close()
            print("Local client socket connection failed!")
            os._exit(1)
    

def receive():   
    connection_socket, addr = welcome_socket.accept()
    while True:
        try:
            # the code to receive messages, shutdown if receive nothing
            msg_r = connection_socket.recvfrom(1024)
            if msg_r[0]==b'':
                connection_socket.close()
                welcome_socket.close()
                print("Connection failed!Connection socket and welcome socket closed!Exit Program!")
                os._exit(1)
            print("\t\t\t\t >> " +  msg_r[0].decode() + "\n>> ",end='')
        except:
            print("Connection failed!")
            connection_socket.close()
            welcome_socket.close()
            print("Connection failed!Connection socket and welcome socket closed!Exit Program!")
            os._exit(1)

th1 = Thread(target=send)
th2 = Thread(target=receive)

th1.start()
th2.start()
