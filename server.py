import socket
import re
import os

HOST = ''
PORT = 80

server = socket.socket()
server.bind((HOST, PORT))

def check_request(packet):
    valid_request_regex_pattern = re.compile(r"^GET\s+(\/[^\s]*)\s+HTTP\/(1\.[01]|2\.[0-9])$")
    request_line = packet.split('\r\n')[0]

    return valid_request_regex_pattern.match(request_line)

def is_filename_valid(packet):
    file_name_regex_pattern = re.compile(r"GET\s\/([^\s]*)")
    file_name_match = file_name_regex_pattern.search(packet)
    return file_name_match


def send_requested_file(client_socket, regex_match):
    file_name = regex_match.group(1)
    file_path = r"C:\\Users\\User\Documents\\HTTP Server\webroot\webroot\\"+file_name
    if (os.path.isfile(file_path)):
        with open(file_path, "rb") as file_to_send:
            file_data = file_to_send.read()
            client_socket.send(file_data)
    else:
        client_socket.close()

while True:
    server.listen()
    client_socket, address = server.accept()

    packet = client_socket.recv(4096).decode()

    if (check_request(packet)):
        print("OK")
        file_name_match = is_filename_valid(packet)
        if (file_name_match is not None):
            send_requested_file(client_socket, file_name_match)
    else:
        print("NOT OK")
        client_socket.close()

