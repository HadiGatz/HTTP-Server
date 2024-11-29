import socket
import re
import os

HOST = ''
PORT = 80

forbidden_files = [r"C:\\Users\\User\Documents\\HTTP Server\webroot\webroot\\test.html",
                   r"C:\\Users\\User\Documents\\HTTP Server\webroot\webroot\\secret.html"]

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


def send_requested_file(client_socket, http_response):
    client_socket.send(http_response)

def get_requested_file_name(packet):
    file_name_regex_pattern = re.compile(r"GET\s\/([^\s]*)")
    file_name_match = file_name_regex_pattern.search(packet)
    if file_name_match:
        return file_name_match.group(1)
    return None

def get_file_type(file_path):
    if (file_path.endswith('.html')):
        return "Content-Type: text/html; charset=utf-8"
    elif (file_path.endswith('.jpg')):
        return "Content-Type: image/jpeg"
    elif (file_path.endswith('.js')):
        return "Content-Type: application/javascript; charset=utf-8"
    elif (file_path.endswith('.css')):
        return "Content-Type: text/css"

def generate_http_response(file_name):
    base_path = r"C:\\Users\\User\Documents\\HTTP Server\webroot\webroot\\"
    file_path = base_path+file_name

    if os.path.isfile(file_path):
        file_size = os.path.getsize(file_path)
        with open(file_path, "rb") as file_to_send:
            file_data = file_to_send.read()
        
        if file_path not in forbidden_files:
            response = (
                "HTTP/1.0 200 OK\r\n"
                f"Content-Length: {file_size}\r\n"
                f"{get_file_type(file_path)}\r\n\r\n"  
            ).encode() + file_data
        else:
            response = (
                "HTTP/1.0 403 Forbidden\r\n"
                "Content-Type: text/plain\r\n\r\n"
                "403 - Forbidden".encode()
            )
    else:
        response = (
            "HTTP/1.0 404 Not Found\r\n"
            "Content-Type: text/plain\r\n\r\n"
            "404 - File Not Found"
        ).encode()
    
    return response


while True:
    server.listen()
    client_socket, address = server.accept()

    packet = client_socket.recv(4096).decode()

    if check_request(packet):
        print("Valid request received.")
        file_name = get_requested_file_name(packet)
        if file_name is not None:
            http_response = generate_http_response(file_name)
            send_requested_file(client_socket, http_response)
    else:
        print("NOT OK")
        response = ("HTTP/1.0 500 Invalid Request\r\n"
            "Content-Type: text/plain\r\n\r\n"
            "500 - Invalid Request").encode()

