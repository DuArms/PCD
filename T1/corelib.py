import socket
from hashlib import sha256

server_address = "127.0.0.1"
server_port = 4200

size = 512

def print_result(buff: bytearray):
    print(f"Length: {len(buff)}")
    # print(f"Content: \n{buff}")

    for i in range(len(buff)):
       if buff[i] != i & 0xFF:
           print(i)

    digest = [hex(x) for x in sha256(buff).digest()]
    print(f"Digest : {digest}")





