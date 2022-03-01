from corelib import *


def check_integrity(test_file):
    client_data = open(test_file, "rb").read()
    server_data = open("server_"+test_file, "rb").read()

    cd_hash = int.from_bytes(sha256(client_data).digest(), "big")
    sd_hash = int.from_bytes(sha256(server_data).digest(), "big")

    print(f"Client data hash: {hex(cd_hash)}")
    print(f"Server data hash: {hex(sd_hash)}")

    print(f"Client data size: {len(client_data)}")
    print(f"Server data size: {len(server_data)}")

    if len(client_data) == len(server_data) and cd_hash != sd_hash:
        for i, (cd, sd) in enumerate(zip(client_data, server_data)):
            if cd != sd:
                print(f"{i}: {cd} != {sd}")

    print("Done!")


if __name__ == "__main__":
    check_integrity()