import socket
import time
from datetime import datetime, timedelta
import pandas as pd


# Transform string to timedelta object
def get_offset(offset: str):
    # Transform string to timedelta
    res = pd.to_timedelta(offset)

    # Return timedelta object
    return res


# Run client node
def run_client(server_ip, server_port):
    # Open client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect socket to specific ip and port
    client.connect((server_ip, server_port))

    # Define zero offset
    offset = timedelta(seconds=0)

    try:
        while True:
            # Create string with current time
            msg = (datetime.now() + offset).strftime("%d/%m/%Y %H:%M:%S")

            # Send current time to server
            client.send(msg.encode("utf-8")[:1024])

            # Receive average offset time and transform it into timedelta object
            clock_time_string = client.recv(1024).decode("utf-8")

            # Check that client still here
            if clock_time_string == "":
                return

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
