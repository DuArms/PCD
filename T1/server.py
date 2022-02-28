from corelib import *
from tcp.tcp_stopandwait_server import create_tcp_server_stopandwait
from tcp.tcp_stream_server import create_tcp_server_stream
from udp.udp_stopandwait_server import create_udp_server_stopandwait
from udp.udp_stream_server import create_udp_server_stream

from  _thread import start_new_thread
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_address, main_server_port))

server_socket.listen()
print("Main server is listening!")

server_option = {
    tcp_stop: create_tcp_server_stopandwait,
    tcp_stream: create_tcp_server_stream,
    udp_stop: create_udp_server_stopandwait,
    udp_stream: create_udp_server_stream
}


def th(my_conn):
    while True:
        func = int.from_bytes(my_conn.recv(4), "big")

        if func not in server_option.keys():
            break

        server_option[func](server_address, server_port)

    conn.close()
    pass


while True:
    conn, addr = server_socket.accept()
    start_new_thread(th, (conn,))
