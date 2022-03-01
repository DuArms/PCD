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
    out = ""
    while True:
        func = int.from_bytes(my_conn.recv(4), "big")

        if func == 6:
            out += test_file + ":\n"
            continue

        if func not in server_option.keys():
            break

        rez = server_option[func](server_address, server_port)

        for x in rez:
           out += str(x) + " "
        out += "\n"

        print()
        print(f" mode:\t{rez[0]} ")
        print(f" msg count:\t{rez[1]} ")
        print(f" byte count:\t{rez[2]} ")
        print(f" time:\t{rez[3]} ")
        print()

    conn.close()

    print(out)
    pass


while True:
    conn, addr = server_socket.accept()
    start_new_thread(th, (conn,))
