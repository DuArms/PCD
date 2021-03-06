from corelib import *



def create_tcp_server_stream(address: str, port: int):
    print("create_tcp_server_stream")

    count_msg = 0
    count_bytes = 0

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((address, port))
    print(f"Server running at {address}:{port}")

    my_socket.listen(1)
    print("Server listening!")

    (connection, address) = my_socket.accept()

    data = connection.recv(int.from_bytes(connection.recv(16), "big")).decode("utf-8")
    file_name, file_size = data.split("_")
    file_size = int(file_size)

    print(f"I have to read {file_size} bytes!")

    files = bytearray()
    bar = tqdm(range(file_size), f"Receiving data!")

    transmission_start_tine = time.time_ns()
    for _ in range(file_size // message_default_size):
        data = connection.recv(message_default_size)

        data = bytearray(data)
        while len(data) != message_default_size:
            temp_data = connection.recv(message_default_size - len(data))
            data.extend(temp_data)
            count_msg += 1

        count_msg += 1
        count_bytes += len(data)

        if len(data) - message_default_size != 0:
            print(len(data) - message_default_size)
        # print(len(data))

        files.extend(data)
        bar.update(len(data))

    if len(files) != file_size:
        data = connection.recv(file_size % message_default_size)
        files.extend(data)
        bar.update(len(data))

        count_msg += 1
        count_bytes += len(data)

    transmission_end_time = time.time_ns()

    with open(f"server_{file_name}", "wb") as file:
        file.write(files)

    connection.close()
    bar.clear()
    bar.close()

    print("Session closed!")
    return ["tcp_stream", count_msg, count_bytes, transmission_end_time - transmission_start_tine, file_name]

if __name__ == "__main__":
    create_tcp_server_stream("127.0.0.1", 4200)
