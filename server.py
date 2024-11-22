import socket
import re

HOST = ''
PORT = 80

server = socket.socket()
server.bind((HOST, PORT))

regex_pattern = re.compile(r"^GET\s+(\/[^\s]*)\s+HTTP\/(1\.[01]|2\.[0-9])$")
while True:
    server.listen()
    client_socket, address = server.accept()

    packet = client_socket.recv(4096).decode()
    request_line = packet.split('\r\n')[0]

    if (regex_pattern.match(request_line)):
        print(packet)
    else:
        client_socket.close()

