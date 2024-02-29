import socket
import struct
import threading

BP_HEADER = b'\x06\x81\x10\x11\x04\x02\x02\x02\x02\x02\x00\x00\x82\xea\xfd\xaa\x6e\x01\xFF\x2c\x00\x05\x10'

def add_bp_header(data):
    return BP_HEADER + data

def remove_bp_header(data):
    return data[len(BP_HEADER):]

def handle_client(client_socket, address):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        if address[0] == '172.16.1.1':
            # Remove BP header and send to 192.168.1.1:4556
            new_data = remove_bp_header(data)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(new_data, ('192.168.1.1', 4556))
        elif address[0] == '192.168.1.254':
            # Add BP header and send to 172.16.1.2:4556
            new_data = add_bp_header(data)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(new_data, ('172.16.1.2', 4556))

    client_socket.close()

def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    print(f"Server listening on {ip}:{port}")

    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f"Received data from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(server_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    threading.Thread(target=start_server, args=('172.16.1.1', 4556)).start()
    threading.Thread(target=start_server, args=('192.168.1.254', 4556)).start()
