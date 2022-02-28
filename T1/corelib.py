import socket
from hashlib import sha256
from tqdm import tqdm
import  time
import os

server_address = "127.0.0.1"
server_port = 4200

size = 1024
test_file = "poza.jpg"

success_msg = b"SUCCESS"
stop_msg = b"X" * size


def print_result(buff: bytearray):
    print(f"Length: {len(buff)}")
    # print(f"Content: \n{buff}")

    for i in range(len(buff)):
       if buff[i] != i & 0xFF:
           print(i)

    digest = [hex(x) for x in sha256(buff).digest()]
    print(f"Digest : {digest}")

def prepare_file(name: str, file_size: int):
    with open(name,"wb") as file:

        buffer = [0] * file_size
        for i in range(file_size):
            buffer[i] = i & 0xFF
        buffer = bytearray(buffer)

        file.write(buffer)





if __name__ == "__main__":
    # file_size = size * 100 + size - 1
    # file_size = 1048576 * 500  # ~ 500 MB
    #file_size = 1073741824  # ~ 1 Gb

    pass





