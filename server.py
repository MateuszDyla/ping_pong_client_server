import socket

import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 12000
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
EXIT_KEY = "exit"
NO_RESPONSE = "noresponse!@#"


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #protocol ipv4, TCP
serverSocket.bind(ADDR) #binds socket to address

def handle_client(connection, address):
    connected = True
    print(f"[NEW CONNECTION] New connection from: {address}")
    while connected:
        msg_len = connection.recv(HEADER).decode(FORMAT) #receive 64 bytes information about the message length
        if msg_len:
            msg_len = int(msg_len)
            msg = connection.recv(msg_len).decode(FORMAT) #receive message
            print(f"[NEW MESSAGE] message (length: {msg_len}) from {address}: {msg}")
            if msg.lower() == "ping":
                connection.send("PONG".encode(FORMAT))
            else:
                connection.send(NO_RESPONSE.encode(FORMAT))
            if msg == EXIT_KEY:
                connection.close()
                connected = False



def start():
    print(f"[SERVER INFO] Server is starting on {SERVER}\n")
    serverSocket.listen() #listens for new connections
    while True:
        connectionSocket, addr = serverSocket.accept() #accepts connection, returns connectionSocket to communicate, and informations about the connection
        thread = threading.Thread(target=handle_client, args=(connectionSocket, addr)) #each connection in a new thread
        thread.start()
        print(f"[SERVER INFO] Active connections: {threading.activeCount() -1}")



start()