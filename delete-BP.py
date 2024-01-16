from kamene.all import *

def process_packet(packet):
    # Remove the 'Raw' layer if it exists
    if packet.haslayer(Raw):
        del packet[Raw]
        
    # Recalculate the IP and UDP lengths
    if packet.haslayer(IP):
        packet[IP].len = len(packet[IP])
    if packet.haslayer(UDP):
        packet[UDP].len = len(packet[UDP])
        
    return packet

# File path for the input pcap file
pcap_file_path = 'pcap/bping_loopback.pcap'

# Read the pcap file
packets = rdpcap(pcap_file_path)

# Process each packet in the pcap file
processed_packets = [process_packet(packet) for packet in packets]

# Create a new pcap file with the processed packets
output_pcap_path = 'pcap/deleted_BP.pcap'
wrpcap(output_pcap_path, processed_packets)