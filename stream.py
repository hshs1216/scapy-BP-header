import socket
import struct
import threading
from bp_header import BP_header

def create_bp_header():
    # バイト列を構築するためのフォーマット文字列を作成
    format_str = ">BBHHHHHHHHHQBHHH6s32s32s"
    values = [BP_header[field]["value"] for field in BP_header]
    packed_data = struct.pack(format_str, *values)
    # バイト列として直接取得
    print(packed_data)
    return header

BP_HEADER = create_bp_header()

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
