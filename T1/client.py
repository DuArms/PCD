import time

from statistic import  *

from corelib import *

from tcp.tcp_stopandwait_client import connect_to_server_tcp_stopandwait
from tcp.tcp_stream_client import connect_to_server_tcp_stream
from udp.udp_stopandwait_client import connect_to_server_udp_stopandwait
from udp.udp_stream_client import connect_to_server_udp_stream

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(5)
print("Connecting...")

#client_socket.connect((server_address, main_server_port))


server_address = "127.0.0.1"
client_socket.connect((server_address, main_server_port))
print("Connected!")

client_option = {
    tcp_stop: connect_to_server_tcp_stopandwait,
    tcp_stream: connect_to_server_tcp_stream,
    udp_stop: connect_to_server_udp_stopandwait,
    udp_stream: connect_to_server_udp_stream
}
files = {
    1 : "poza.jpg",
    2 : "mb.txt",
    3 : "gb.txt"
}

def user_interface():
    while True:
        print("Pick 1")
        print(f" {tcp_stop} for tcp stop ")
        print(f" {tcp_stream} for tcp stream ")
        print(f" {udp_stop} for udp stop ")
        print(f" {udp_stream} for udp stream ")
        mode = int(input())

        print("Pick 1")
        print(f" {1} for photo ")
        print(f" {2} for 500 mb")
        print(f" {3} for 1 gb ")

        test_file = files[int(input())]

        client_socket.send(mode.to_bytes(4, "big"))

        if mode not in client_option.keys():
            break

        rez = client_option[mode](server_address, server_port, test_file)

        print()
        print(f" mode:\t{rez[0]} ")
        print(f" msg count:\t{rez[1]} ")
        print(f" byte count:\t{rez[2]} ")
        print(f" time:\t{rez[3]} ")
        print()

        check_integrity(test_file)

def auto_test():
    out = ""
    for test_file in files.values():
        out += test_file + ":\n"


        for mode in range(1,5):
            client_socket.send(mode.to_bytes(4, "big"))

            rez = client_option[mode](server_address, server_port, test_file)
            for x in rez:
               out += str(x) + " "
            out += "\n"

            time.sleep(5)


    client_socket.send((5).to_bytes(4, "big"))
    print(out)

if __name__ == "__main__":
    if int(input("Pres 0 for auto test!")):
        user_interface()
    else:
        auto_test()

