from corelib import *


def create_udp_server_stream(address: str, port: int):
    print("create_udp_server_stream")

    count_msg = 0
    count_bytes = 0

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

    while recived_data < file_size:
        try:
            data, __ = my_socket.recvfrom(message_default_size + 4)
        except:
            continue
        fragment_number = int.from_bytes(data[:4],"big")
        data = data[4:]

        count_msg += 1
        count_bytes += len(data)

        if fragment_number not in files_dict.keys():
            files_dict[fragment_number] = data
            bar.update(len(data))
            recived_data += len(data)




    files = bytearray()
    for i in range(file_size // message_default_size + 1):
        try:
            files.extend(files_dict[i])
        except:
            pass

    transmission_end_time = time.time_ns()

    with open(f"server_{file_name}", "wb") as file:
        file.write(files)

    return ["udp_stream", count_msg, count_bytes, transmission_end_time - transmission_start_tine]



if __name__ == "__main__":
    create_udp_server_stream("127.0.0.1", 4200)
