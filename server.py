import socket

HOST = ''
PORT = 80

server = socket.socket()
server.bind((HOST, PORT))

while True:
    server.listen()
    client_socket, address = server.accept()

    packet = client_socket.recv(4096).decode()
    print(packet)

