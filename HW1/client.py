import socket
import time
from datetime import datetime, timedelta


# Transform string to timedelta object
def get_offset(offset: str):
    datetime_obj = datetime.strptime(offset, "%H:%M:%S.%f")
    total_microsec = datetime_obj.hour + datetime_obj.minute + datetime_obj.second + datetime_obj.microsecond
    return timedelta(microseconds=total_microsec)


# Run client node
def run_client(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((server_ip, server_port))

    offset = timedelta(seconds=0)

    try:
        while True:
            msg = (datetime.now() + offset).strftime("%d/%m/%Y %H:%M:%S")

            client.send(msg.encode("utf-8")[:1024])

            clock_time_string = client.recv(1024).decode("utf-8")
            offset = get_offset(clock_time_string)

            if clock_time_string == "":
                print(f"Server from {server_port[0]}:{server_port[1]} is closed", end="\n\n")
                return

            print("Received offset time:", str(offset),
                  "\nCurrent time:        ", datetime.now() + offset, end="\n\n")

            time.sleep(5)
    except Exception as e:
        print(f"Error: {e}", end="\n\n")
    finally:
        client.close()
        print("Connection to server closed", end="\n\n")


if __name__ == '__main__':
    run_client('127.0.0.1', 8080)
