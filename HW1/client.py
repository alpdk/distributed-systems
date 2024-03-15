import socket
import time
from datetime import datetime


def run_client(server_ip, server_port):
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # establish connection with server
    client.connect((server_ip, server_port))

    try:
        while True:
            msg = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            client.send(msg.encode("utf-8")[:1024])

            clock_time_string = client.recv(1024).decode("utf-8")

            if clock_time_string == "":
                print(f"Server from {server_port[0]}:{server_port[1]} is closed", end="\n\n")
                return

            print("Received new time: " + clock_time_string + "\nCurrent time:     ", datetime.now(), end="\n\n")

            time.sleep(5)
    except Exception as e:
        print(f"Error: {e}", end="\n\n")
    finally:
        # close client socket (connection to the server)
        client.close()
        print("Connection to server closed", end="\n\n")

if __name__ == '__main__':
    run_client('127.0.0.1', 8080)