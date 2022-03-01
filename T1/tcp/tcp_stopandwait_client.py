import time

from corelib import *

def connect_to_server_tcp_stopandwait(address, port):
    global test_file
    print("connect_to_server_tcp_stopandwait")
    count_msg = 0
    count_bytes = 0

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((address, port))

    file_size = os.path.getsize(f"{test_file}")
    print(f"I will send {file_size} bytes!")

    msg = f"{test_file}_{file_size}".encode()
    my_socket.send(len(msg).to_bytes(16, "big"))
    my_socket.send(msg)

    bar = tqdm(range(file_size), f"Sending data!")

    transmission_start_tine = time.time_ns()
    with open(test_file, "rb") as file:
        for i in range(file_size // message_default_size):
            buffer = file.read(message_default_size)
            my_socket.send(buffer)

            my_socket.recv(len(success_msg))

            bar.update(message_default_size)
            count_msg += 1
            count_bytes += len(buffer)

        buffer = file.read(file_size % message_default_size)

        my_socket.send(buffer)

        count_msg += 1
        count_bytes += len(buffer)
        bar.update(file_size % message_default_size)

    transmission_end_time = time.time_ns()
    bar.clear()
    bar.close()
    my_socket.close()

    print("Session closed!")

    return ["tcp_stopandwait", count_msg , count_bytes, transmission_end_time - transmission_start_tine]

if __name__ == "__main__":
    connect_to_server_tcp_stopandwait("127.0.0.1", 4200)
