import time

from corelib import *
from tqdm import tqdm
# 1 GIGABYTES = 1073741824 BYTES

print(1073741824 // 512)

# bar = tqdm(range(10_000), f"Receiving DA", unit="B", unit_scale=True, unit_divisor=10)
# for i in range(10_000):
#     bar.update(1)
#     time.sleep(1)


def connect_to_server_tcp(address, port):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((address, port))


    size: int = 512
    #file_size = size * 100
    #file_size = 1048576 * 500  # ~ 500 MB
    file_size = 1073741824   # ~ 1 Gb

    size_as_bytes = file_size.to_bytes(byteorder="big", length=16)
    print(f"I will send {file_size} bytes!")

    my_socket.send(size_as_bytes)

    buffer = [0] * file_size

    for i in range(file_size):
        buffer[i] = i & 0xFF

    buffer = bytearray(buffer)

    for i in range(file_size // size):
        my_socket.send(buffer[i * size: (i + 1) * size])

    # my_socket.send(buffer)

    my_socket.close()
    print_result(buffer)


def connect_to_server_udp(address: str, port: int):
    msgFromClient = "Hello UDP Server"
    bytesToSend = str.encode(msgFromClient)


    my_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket

    my_socket.sendto(bytesToSend, (address, port))



connect_to_server_udp("127.0.0.1", 4200)



