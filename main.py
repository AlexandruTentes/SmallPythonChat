import socket
import threading
import time
import os

data_size = 1024
server_IP = 'localhost'
server_PORT = 22000
sockets_connected_list = {}

TCP_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    #makes sure to re-use the freshly closed ports
    #still might throw the error
    TCP_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #simply bind the server to the ip and port
    #and start listening
    TCP_server_socket.bind((server_IP, server_PORT))
    TCP_server_socket.listen(1)

except:
    print("Error at starting the server. Check the IP and PORT!")
    os.exit(1)

def each_connection_handler(connection, address):
    while True:
        try:
            socket_data = connection.recv(data_size)
            print(socket_data)
            for (key, conn) in sockets_connected_list.items():
                if key[0] == connection:
                    continue
                key[0].send(bytes(socket_data))
                
        except Exception as e:
            
                #only occurs if the package fails to be sent back to the client
                #which made the request to receive the package
                #=============#
                print("Connection with the IP ", address[0],"abnormally intrerupted")
                print(str(address[0]), ' : ', str(address[1]), " --- disconnected")
                del sockets_connected_list[(connection, address)]
                print("users left: " + str(len(sockets_connected_list)))
                print(e)
                connection.close()
                break

def run_server():
    while True:
        connection_socket, connection_socket_address_IP = TCP_server_socket.accept()

        sockets_connected_list[(connection_socket, connection_socket_address_IP)] = [False, 0, "", "", "", 0]
        print(str(connection_socket_address_IP[0]), ' : ', str(connection_socket_address_IP[1]), " --- connected")

        connection_thread = threading.Thread(target=each_connection_handler, args=(connection_socket, connection_socket_address_IP))
        connection_thread.daemon = True
        connection_thread.start()

run_server()
