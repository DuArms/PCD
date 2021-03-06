import time

from corelib import *


def create_udp_server_stopandwait(address: str, port: int):
    count_msg = 0
    count_bytes = 0

    print("create_udp_server_stopandwait")
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.bind((address, port))
    print(f"Server running at {address}:{port}")

    (data, address) = my_socket.recvfrom(16)
    (data, address) = my_socket.recvfrom( int.from_bytes(data, "big") )

    file_name, file_size = data.decode("utf-8").split("_")
    file_size = int(file_size)

    print(f"I have to read {file_size} bytes!")


    bar = tqdm(range(file_size), f"Receiving data!")

    files_dict = dict()
    my_socket.settimeout(10)
    recived_data = 0

    transmission_start_tine = time.time_ns()
    try:
        while recived_data < file_size:
            data, address = my_socket.recvfrom(message_default_size + 4)
            fragment_number = int.from_bytes(data[:4],"big")
            data = data[4:]

            count_msg += 1
            count_bytes += len(data)

            if fragment_number not in files_dict.keys():
                files_dict[fragment_number] = data
                bar.update(len(data))
                recived_data += len(data)

            my_socket.sendto(success_msg ,address)


    except Exception as e:
        print(e)
        pass

    files = bytearray()
    for i in range(file_size // message_default_size + 1):
        try:
            files.extend(files_dict[i])
        except:
            pass

    transmission_end_time = time.time_ns()

    with open(f"server_{file_name}", "wb") as file:
        file.write(files)

    return ["udp__stopandwait", count_msg, count_bytes, transmission_end_time - transmission_start_tine, file_name]



if __name__ == "__main__":
    create_udp_server_stream("127.0.0.1", 4200)
