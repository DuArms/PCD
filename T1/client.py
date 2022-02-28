import time

from statistic import  *

from corelib import *
from tcp.tcp_stopandwait_client import connect_to_server_tcp_stopandwait
from tcp.tcp_stream_client import connect_to_server_tcp_stream
from udp.udp_stopandwait_client import connect_to_server_udp_stopandwait
from udp.udp_stream_client import connect_to_server_udp_stream

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, main_server_port))

client_option = {
    tcp_stop: connect_to_server_tcp_stopandwait,
    tcp_stream: connect_to_server_tcp_stream,
    udp_stop: connect_to_server_udp_stopandwait,
    udp_stream: connect_to_server_udp_stream
}

while True:
    print("Pick 1")
    print(f" {tcp_stop} for tcp stop ")
    print(f" {tcp_stream} for tcp stream ")
    print(f" {udp_stop} for udo stop ")
    print(f" {udp_stream} for udp stream ")
    mode = int(input())

    client_socket.send(mode.to_bytes(4, "big"))

    if mode not in client_option.keys():
        break

    client_option[mode](server_address, server_port)

    check_integrity()
