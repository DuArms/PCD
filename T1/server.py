from corelib import *


def create_tcp_server(address: str, port: int):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((address, port))
    print(f"Server running at {address}:{port}")

    my_socket.listen(1)
    (connection, address) = my_socket.accept()

    file_size = int.from_bytes(connection.recv(16), "big")
    print(f"I have to read {file_size} bytes!")

    files = bytearray()

    for _ in range(file_size // size):
        data = connection.recv(size)
        if not data:
            print(" Problem boy!")
            break

        files.extend(data)

    connection.close()

    print_result(files)

    print("Server closed!")


def create_udp_server(address: str, port: int):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.bind((address, port))

    print(f"Server running at {address}:{port}")

    (message, address) = my_socket.recvfrom(size)

    clientMsg = f"Message from Client:{message}"
    clientIP = f"Client IP Address:{address}"

    print(clientMsg)
    print(clientIP)


create_udp_server("127.0.0.1", 4200)














