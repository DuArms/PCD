import time

from corelib import *

udp_resend = 1

def connect_to_server_udp_stopandwait(address: str, port: int,test_file):
    print("connect_to_server_udp_stopandwait")
    my_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    count_msg = 0
    count_bytes = 0

    file_size = os.path.getsize(f"{test_file}")
    print(f"I will send {file_size} bytes!")

    msg = f"{test_file}_{file_size}".encode()
    my_socket.sendto(len(msg).to_bytes(16, "big"), (address, port))
    my_socket.sendto(msg, (address, port))

    bar = tqdm(range(file_size  * udp_resend) , f"Sending data!")
    transmission_start_tine = time.time_ns()
    for _ in range(udp_resend):
        with open(test_file, "rb") as file:
            for i in range(file_size // message_default_size):
                buffer = file.read(message_default_size)

                x = bytearray(i.to_bytes(4,"big"))
                x.extend(buffer)
                my_socket.sendto(x, (address, port))

                my_socket.recv(len(success_msg))

                bar.update(message_default_size)
                count_msg += 1
                count_bytes += len(buffer)

            if file_size % message_default_size != 0:
                buffer = file.read(file_size % message_default_size)

                x = bytearray((file_size // message_default_size).to_bytes(4, "big"))
                x.extend(buffer)
                my_socket.sendto(x, (address, port))
                bar.update(file_size % message_default_size)

                count_msg += 1
                count_bytes += len(buffer)

    transmission_end_time = time.time_ns()
    bar.clear()
    bar.close()
    my_socket.shutdown(socket.SHUT_RDWR)
    my_socket.close()

    print("Session closed!")
    return ["udp_stopandwait", count_msg, count_bytes, transmission_end_time - transmission_start_tine]

if __name__ == "__main__":
    connect_to_server_udp_stopandwait("127.0.0.1", 4200)
