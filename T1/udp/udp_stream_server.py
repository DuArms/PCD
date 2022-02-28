from corelib import *


def create_udp_server_stream(address: str, port: int):
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
    try:
        while recived_data < file_size:
            data, __ = my_socket.recvfrom(size + 4)
            fragment_number = int.from_bytes(data[:4],"big")
            data = data[4:]

            if not data:
                print("Error happened!")
                break

            if fragment_number not in files_dict.keys():
                files_dict[fragment_number] = data
                bar.update(len(data))
                recived_data += len(data)


    except Exception as e:
        print(e)
        pass

    files = bytearray()
    for i in range(file_size // size + 1):
        try:
            files.extend(files_dict[i])
        except:
            pass

    with open(f"server_{file_name}", "wb") as file:
        file.write(files)



if __name__ == "__main__":
    create_udp_server_stream("127.0.0.1", 4200)
