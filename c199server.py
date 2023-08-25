import socket
from threading import Thread

#1. addr family -is the family of addresses 
# that the socket can communicate with
#AF_INET represents IPv4 while AF_INET6 represents IPv6.
#2. socket type
#SOCK_STREAM. It is the default value (if not provided) 
# and it is used to create a TCP Socket.

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port=8000

server.bind((ip_address,port))
server.listen()

list_of_clients = []
print("Server is running...")

def clientthread(conn,addr):
    conn.send("Welcome to this chat room".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                print("<"+addr[0]+">"+message)
                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message_to_send, conn)
            
            else:
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
while True:
    #1. The socket object of the client that is trying to connect
    #2. Their IP Address and Port number in the form of a tuple
    conn , addr = server.accept()
    print(conn)
    print(addr)
    list_of_clients.append(conn)
    print(addr[0]+"connected")

    new_thread = Thread(target=clientthread , args=(conn,addr))
    new_thread.start()


