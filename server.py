import socket
import re

HOST = ''
PORT = 80

server = socket.socket()
server.bind((HOST, PORT))

valid_request_regex_pattern = re.compile(r"^GET\s+(\/[^\s]*)\s+HTTP\/(1\.[01]|2\.[0-9])$")
while True:
    server.listen()
    client_socket, address = server.accept()

    packet = client_socket.recv(4096).decode()
    request_line = packet.split('\r\n')[0]

    if (valid_request_regex_pattern.match(request_line)):
        print("OK")
        file_name_regex_pattern = re.compile(r"GET\s\/([^\s]*)")
        file_name_match = file_name_regex_pattern.search(packet)
        if (file_name_match is not None):
            file_name = file_name_match.group(1)
            client_socket.send(file_name.encode())
    else:
        print("NOT OK")
        client_socket.close()

