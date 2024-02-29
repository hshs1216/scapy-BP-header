import socket
import struct
import threading
from bp_header import BP_header

def create_bp_header():
    header = b''
    for key, value in BP_header.items():
        header += value["value"].to_bytes(value["digits"] // 2, byteorder='big')
    return header

BP_HEADER =  b'\x06\x81\x10\x11\x04\x02\x02\x02\x02\x02\x00\x00\x82\xea\xfd\xaa\x6e\x01\xFF\x2c\x00\x05\x10\x08\x69\x70\x6e\x00\x32\x2e\x30\x00\x14\x01\x01\x00\x01\x09\x03\x03\x47\x6f'

def add_bp_header(data):
    return BP_HEADER + data

def remove_bp_header(data):
    return data[len(BP_HEADER):]

def handle_client(client_socket, address, interface):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        if interface == 'enp0s8':
            # Remove BP header and send to 192.168.1.1:4556
            new_data = remove_bp_header(data)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind(('192.168.1.254', 12345))
                s.sendto(new_data, ('192.168.1.1', 4556))
        elif interface == 'enp0s9':
            # Add BP header and send to 172.16.1.2:4556
            new_data = add_bp_header(data)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind(('172.16.1.1', 12345))
                s.sendto(new_data, ('172.16.1.2', 4556))

    client_socket.close()

def start_server(ip, port, interface):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, interface.encode())
    server_socket.bind((ip, port))
    print(f"Server listening on {ip}:{port} via {interface}")

    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f"Received data from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(server_socket, addr, interface))
        client_thread.start()

if __name__ == "__main__":
    threading.Thread(target=start_server, args=('172.16.1.1', 4556, 'enp0s8')).start()
    threading.Thread(target=start_server, args=('192.168.1.254', 4556, 'enp0s9')).start()
