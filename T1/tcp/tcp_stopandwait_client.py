from corelib import *

def connect_to_server_tcp_stopandwait(address, port):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((address, port))

    file_size = os.path.getsize(f"{test_file}")
    print(f"I will send {file_size} bytes!")

    msg = f"{test_file}_{file_size}".encode()
    my_socket.send(len(msg).to_bytes(16, "big"))
    my_socket.send(msg)

    bar = tqdm(range(file_size), f"Sending data!")

    with open(test_file, "rb") as file:
        for i in range(file_size // size):
            buffer = file.read(size)
            my_socket.send(buffer)

            my_socket.recv(len(success_msg))

            bar.update(size)

        buffer = file.read(file_size % size)

        my_socket.send(buffer)
        bar.update(file_size % size)

    bar.clear()
    bar.close()
    my_socket.close()

    print("Session closed!")


if __name__ == "__main__":
    connect_to_server_tcp_stopandwait("127.0.0.1", 4200)
