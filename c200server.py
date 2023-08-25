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
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []

print("Server has started...")

def clientthread(conn, nickname):
    conn.send("Welcome to this chatroom!".encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                print(message)
                broadcast(message, conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)


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
    conn, addr = server.accept()
    
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    print (addr[0] + " connected")

    nicknames.append(nickname)
    message = '{} joined!'.format(nickname)
    print(message)
    broadcast(message,conn)
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()