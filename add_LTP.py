from kamene.all import *
import ipaddress
from BP_header import BP_header
from LTP_header import LTP_header

# Define the networks and their corresponding outputs in a dictionary
networks = {
    ipaddress.ip_network('127.0.0.1/32'): 1,
    # ipaddress.ip_network('192.168.0.0/16'): 2
}

def match_ip(ip):
    # Convert the input IP to an IP address object
    ip_addr = ipaddress.ip_address(ip)

    # Check if the IP matches any of the networks
    for network, output in networks.items():
        if ip_addr in network:
            return output

    # If no match is found, return 1
    return 1

def process_packet(packet):
    
    if packet.haslayer(UDP):
        # First, Create BP header
        Joined_BP_header = "".join([format(value["value"], '0' + str(value["digits"]) + 'x') for value in BP_header.values()])
        # Second, Create LTP header
        packet[UDP].dport = 1113 # The UDP port number 1113 with the name "ltp-deepspace" has been reserved for LTP deployments.
        LTP_header["Length"]["value"] = len(bytes.fromhex(Joined_BP_header))
        Joined_LTP_header = "".join([format(value["value"], '0' + str(value["digits"]) + 'x') for value in LTP_header.values()])
        # Finally, Convert the given string to bytes
        data_to_add = bytes.fromhex(Joined_LTP_header)
        data_to_add += bytes.fromhex(Joined_BP_header)
    
    # Add the data to the packet
    if packet.haslayer(Raw):
        packet[Raw].load += data_to_add
    else:
        packet = packet / Raw(load=data_to_add)
        # Recalculate the IP and UDP lengths
    if packet.haslayer(IP):
        packet[IP].len = len(packet[IP])
    if packet.haslayer(UDP):
        packet[UDP].len = len(packet[UDP])
    return packet

    


# File path for the input pcap file
pcap_file_path = 'pcap/deleted_BP.pcap'

# Read the pcap file
packets = rdpcap(pcap_file_path)

# Process each packet in the pcap file
processed_packet = process_packet(packets[0])

# Create a new pcap file with the processed packets
output_pcap_path = 'pcap/LTP_add.pcap'
wrpcap(output_pcap_path, processed_packet)

print(ls(UDP))