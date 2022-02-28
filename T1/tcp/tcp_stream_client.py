from corelib import *


def connect_to_server_tcp_stream(address, port):
    print("connect_to_server_tcp_stream")
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((address, port))

    file_size = os.path.getsize(f"{test_file}")
    print(f"I will send {file_size} bytes!")

    msg = f"{test_file}_{file_size}".encode()
    my_socket.send(len(msg).to_bytes(16, "big"))
    my_socket.send(msg)

    bar = tqdm(range(file_size), f"Sending data!")

    with open(test_file, "rb") as file:
        for i in range(file_size // message_default_size):
            buffer = file.read(message_default_size)
            bytes_sent = my_socket.send(buffer)

            while bytes_sent < message_default_size:
                bytes_sent += my_socket.send(buffer[bytes_sent:])


            bar.update(message_default_size)

        buffer = file.read(file_size % message_default_size)
        total = my_socket.send(buffer)


        bar.update(file_size % message_default_size)

    bar.clear()
    bar.close()
    my_socket.close()

    print("Session closed!")


if __name__ == "__main__":
    connect_to_server_tcp_stream("127.0.0.1", 4200)
