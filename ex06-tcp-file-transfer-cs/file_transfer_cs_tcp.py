# Author: Handy Pan
# Date: Feb 27, 2022

# libraries
import socket
import os

class FileTransfer():
    '''
        a class for File Transfer: download and upload
    '''

    def __init__(self):
        pass

    # server
    def server():
        server_host = ''
        server_port = input('Enter the port of the server: ')

        welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        welcome_socket.bind((server_host, int(server_port)))
        print('Welcome socket {} established at {}:{}.'.format(welcome_socket, welcome_socket.getsockname()[0], welcome_socket.getsockname()[1]))
        print('Welcome socket {} bound to {}:{}.'.format(welcome_socket, server_host, server_port))

        welcome_socket.listen(1)
        print('Start listening 1 client.')

        # return from welcome_socket.accept() to monitor the Ctrl + c KeyboardInterrupt
        welcome_socket.settimeout(0.5)

        # make sure connection_socket is None
        connection_socket = None
        verbose = True

        try:
            while True:
                try:
                    if verbose:
                        print("Waiting for client request...")
                    
                    connection_socket, client_addr = welcome_socket.accept()
                    print("Connection socket {} established by {}:{}".format(connection_socket, client_addr[0], client_addr[1]))
                    
                    # set timeout for connection_socket
                    connection_socket.settimeout(20)

                    # receive the request type
                    req_type = connection_socket.recv(1024).decode()

                    # inform the client to proceed request
                    server_ready = 'true'
                    connection_socket.sendall(server_ready.encode())
                    
                    if req_type == 'download':
                        # receive the requested file name to download    
                        req_file = connection_socket.recv(1024).decode()
                        req_file_path = os.path.join(os.getcwd(), req_file)
                        print("To be downloaded: {}".format(req_file_path))

                        # if the requested file does not exist
                        if not os.path.exists(req_file_path):
                            file_exist = "false"
                            connection_socket.sendall(file_exist.encode())
                            connection_socket.close()
                            print("{} closed.".format(connection_socket))
                            connection_socket = None
                            print("File does not exist: {}. Connection socket terminated!".format(req_file_path))
                            verbose = True
                            continue
                        else:
                            file_exist = "yes"
                            connection_socket.sendall(file_exist.encode())

                        # if the requested file exists    
                        with open(req_file_path, 'rb') as file_to_send:
                            for data in file_to_send:
                                connection_socket.sendall(data)
                        connection_socket.close()
                        print("{} closed.".format(connection_socket))
                        connection_socket = None
                        print("File {} transfer completed!Connection socket terminated!".format(req_file_path))      

                        verbose = True

                    elif req_type == 'upload':
                        # receive the requested file directory to upload to
                        req_file_direc = connection_socket.recv(1024).decode()
                
                        # file does not exist on the client side, receive '' on the server, the client socket has already been terminated
                        if req_file_direc == '':
                            print("Connection terminated by the client!")
                            verbose = True
                            continue
                        
                        # if '.' or other folder name is received
                        req_file_direc = os.getcwd() if req_file_direc == '.' else os.path.join(os.getcwd(), req_file_direc)

                        # if the requested file directory does not exist, create the folder on the server current path
                        if not os.path.exists(req_file_direc):
                            os.makedirs(req_file_direc)
                            print("{} does not exist, created successfully!".format(req_file_direc))
                        
                        # if the requested file directory exist
                        req_file_direc_ready = "true"
                        connection_socket.send(req_file_direc_ready.encode())
                        
                        # receive the requested file name to upload from the client
                        file_to_upload = connection_socket.recv(1024).decode()
                        
                        # save the file data to the specified directory
                        with open(os.path.join(req_file_direc, file_to_upload), 'wb') as file_to_write:
                            while True:
                                data = connection_socket.recv(1024)
                                if not data:
                                    break
                                file_to_write.write(data)
                            file_to_write.close()
                        
                        connection_socket.close()
                        print("{} closed.".format(connection_socket))
                        connection_socket = None
                        print("File saved to {}".format(os.path.join(req_file_direc, file_to_upload)))  
                    
                        verbose = True   

                except socket.timeout:
                    # pass

                    # if the connection_socket is not None and timeout
                    if connection_socket is not None:
                        connection_socket.close()
                        print("{} closed.".format(connection_socket))
                        connection_socket = None
                        verbose = True
                        print("Connection socket timeout! Connection socket terminated!")
                        continue
                    # if it's the welcome_socket timeout
                    else:    
                        verbose = False
            
        except KeyboardInterrupt:
            if connection_socket is not None:
                connection_socket.close()
                print("{} closed.".format(connection_socket))
                connection_socket = None
            welcome_socket.close()    
            print("{} closed by KeyboardInterrupt (Ctrl + c)!".format(welcome_socket)) 
            welcome_socket = None

    # client
    def client():
        server_host, server_port = input('Enter the hostname/IP and port of the fileserver: ').split()

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.settimeout(5)

        try:
            client_socket.connect((server_host, int(server_port)))
            print("Try to connect to server {}:{}".format(server_host, server_port))
        except socket.error as msg:
            print("Fail to connect to server {}:{}. Error: {}".format(server_host, server_port, msg))
            os._exit(1)
        else:
            print("Connected to the server {}:{}".format(server_host, server_port))

        # download
        req_type = input('Enter the type of the file transfer: download (d) or upload (u): ')
        if req_type == 'download' or req_type == 'd':
            req_type = 'download'
        elif req_type == 'upload' or req_type == 'u':
            req_type = 'upload'
        else:
            print("Input error! Quit the program")
            os._exit(1)

        try:
            # inform the server of the request type
            client_socket.sendall(req_type.encode())

            # receive the server_ready signal
            server_ready = client_socket.recv(1024).decode()

            if server_ready == 'true':
                # proceed the file transfer
                if req_type == 'download':
                    file_to_download = input('Enter the name of the file to download: ')
                    download_to_direc = input('Enter the folder to save the file: (Input . to save to the current path) ')
                    download_to_direc = os.getcwd() if download_to_direc == '.' else os.path.join(os.getcwd(), download_to_direc)

                    client_socket.send(file_to_download.encode())

                    # receive 'file_exist' from the server
                    file_exist = client_socket.recv(1024).decode()
                    if file_exist == "false":
                        print("{} does not exist on the server! Terminate the connection!".format(file_to_download))
                        client_socket.close()
                        os._exit(1)

                    if not os.path.exists(download_to_direc):
                        os.makedirs(download_to_direc)
                        print("{} does not exist, created successfully!".format(download_to_direc))

                    with open(os.path.join(download_to_direc, file_to_download), 'wb') as file_to_write:
                        while True:
                            data = client_socket.recv(1024)
                            if not data:
                                break
                            file_to_write.write(data)
                        file_to_write.close()
                        print("File saved to {}".format(os.path.join(download_to_direc, file_to_download)))

                elif req_type == 'upload': 
                    file_to_upload = input('Enter the name of the file to upload: ')
                    upload_from_direc = input('Enter the folder to upload the file from: (Input . to upload from the current path) ')
                    upload_from_direc = os.getcwd() if upload_from_direc == '.' else os.path.join(os.getcwd(), upload_from_direc)
                    req_file_path = os.path.join(upload_from_direc, file_to_upload)

                    if not os.path.exists(req_file_path):
                        print("{} does not exist on the client! Terminate the connection!".format(req_file_path))
                        client_socket.close()
                        os._exit(1)

                    # check whether the directory exists on the server
                    upload_to_direc = input('Enter the folder to upload the file to: (Input . to upload to the default path) ')

                    client_socket.send(upload_to_direc.encode())

                    # receive 'req_file_direc_ready' from the server
                    req_file_direc_ready = client_socket.recv(1024).decode()
                    if req_file_direc_ready == "true":
                        client_socket.send(file_to_upload.encode())

                        with open(req_file_path, 'rb') as file_to_send:
                            for data in file_to_send:
                                client_socket.sendall(data)    
                        client_socket.close()
                        print("File {} transfer completed!Client socket terminated!".format(req_file_path))
                    
        except socket.timeout:
            print("Client socket timeout! Quit the program!")
            client_socket.close()
            os._exit(1)

        except socket.error as msg:
            print("Fail to connect to server {}:{}. Error: {}".format(server_host, server_port, msg))
            client_socket.close()
            os._exit(1)

        except KeyboardInterrupt:
            if client_socket is not None:
                client_socket.close()
            print("Client closed by KeyboardInterrupt (Ctrl + c)!") 

# main program
role = input("Please assign the role of the local machine: server (s) or client (c): ")
if role == 'server' or role == 's':
    FileTransfer.server()
elif role == 'client' or role == 'c':
    FileTransfer.client()
else:
    print("Input error! Quit the program!")
    os._exit(1)


