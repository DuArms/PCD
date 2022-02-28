import time

from corelib import *

udp_resend = 1

def connect_to_server_udp_stopandwait(address: str, port: int):
    print("connect_to_server_udp_stopandwait")
    my_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    file_size = os.path.getsize(f"{test_file}")
    print(f"I will send {file_size} bytes!")

    msg = f"{test_file}_{file_size}".encode()
    my_socket.sendto(len(msg).to_bytes(16, "big"), (address, port))
    my_socket.sendto(msg, (address, port))

    bar = tqdm(range(file_size  * udp_resend) , f"Sending data!")

    for _ in range(udp_resend):
        with open(test_file, "rb") as file:
            for i in range(file_size // message_default_size):
                buffer = file.read(message_default_size)

                x = bytearray(i.to_bytes(4,"big"))
                x.extend(buffer)
                my_socket.sendto(x, (address, port))
                bar.update(message_default_size)

                my_socket.recv(len(success_msg))

            if file_size % message_default_size != 0:
                buffer = file.read(file_size % message_default_size)

                x = bytearray((file_size // message_default_size).to_bytes(4, "big"))
                x.extend(buffer)
                my_socket.sendto(x, (address, port))
                bar.update(file_size % message_default_size)







    bar.clear()
    bar.close()
    my_socket.shutdown(socket.SHUT_RDWR)
    my_socket.close()

    print("Session closed!")


if __name__ == "__main__":
    connect_to_server_udp("127.0.0.1", 4200)
