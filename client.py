import socket

SERVER = "192.168.56.1"
PORT = 12000
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
EXIT_KEY = "exit"
NO_RESPONSE = "noresponse!@#"

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    message_len = len(message)
    send_len = str(message_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    clientSocket.send(send_len)
    clientSocket.send(message)

print("[CLIENT INFO] Type message and press enter to send. Type exit to disconnect\n")
connected = True
while connected:
    msg = input()
    send(msg)
    if msg == EXIT_KEY:
        connected = False
    pong = clientSocket.recv(HEADER).decode(FORMAT)
    if pong != NO_RESPONSE:
        print(pong)
        send(EXIT_KEY)

