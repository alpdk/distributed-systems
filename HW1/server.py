import socket
import threading
import time
from datetime import datetime, timedelta

# Clients data for sending average offset time
client_data = {}


# Collecting information from client nodes
def client_time(client_socket, addr):
    try:
        while True:
            # Receive time from client
            clock_time_string = client_socket.recv(1024).decode("utf-8")

            # Check that client still here
            if clock_time_string == "":
                print(f"Client from {addr[0]}:{addr[1]} is closed", end="\n\n")
                client_data.pop(addr)
                return

            clock_time = datetime.strptime(clock_time_string, "%d/%m/%Y %H:%M:%S")
            clock_time_diff = datetime.now() - clock_time

            client_data[addr] = {
                "clock_time": clock_time,
                "time_difference": clock_time_diff,
                "connector": client_socket
            }

            print("Client Data updated with: " + str(addr), end="\n\n")
            time.sleep(5)
    except Exception as e:
        print(f"Error when handling client: {e}", end="\n\n")
    finally:
        if addr in client_data.keys():
            client_data.pop(addr)
        client_socket.close()


# Connect client node to server
def accept_client(server):
    try:
        while True:
            # Accept client node with parameters: client_socket and addr
            client_socket, addr = server.accept()

            print(f"Accepted connection from {addr[0]}:{addr[1]}", end="\n\n")

            # Start asking time from client node
            time_threads = threading.Thread(target=client_time, args=(client_socket, addr))
            time_threads.start()
    except Exception as e:
        print(f"Error: {e}", end="\n\n")
    finally:
        server.close()


# Calculate averager offset time for client nodes
def get_average_offset():
    # Take a list of time_difference from
    time_difference_list = list(client['time_difference']
                                for _, client
                                in client_data.items())

    # Summarize time_difference from every client
    sum_of_clock_difference = sum(time_difference_list, timedelta(0, 0))

    # Define average_clock_difference
    average_clock_difference = timedelta(0, 0)

    # Divide sum_of_clock_difference by count of client nodes
    if len(client_data) != 0:
        average_clock_difference = sum_of_clock_difference / len(client_data)

    return average_clock_difference


# Send average offset to client nodes
def start_change_time():
    try:
        while True:
            # Get average offset
            average_offset = get_average_offset()

            print("Average offset: ", average_offset, end="\n\n")
            print(datetime.now())

            for client in client_data:
                # Send average offset to client nodes as a string
                client_data[client]['connector'].send(str(average_offset).encode("utf-8")[:1024])

                print(f"Send update time for {client[0]}:{client[1]}", end="\n\n")

            time.sleep(5)
    except Exception as e:
        print(f"Error: {e}", end="\n\n")


# Run server node
def run_server(server_ip, server_port):
    # Open server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect socket to specific ip and port
    server.bind((server_ip, server_port))

    # Server start listening
    server.listen()
    print(f"Listening on {server_ip}:{server_port}", end="\n\n")

    # Accepting new client nodes
    accept_threads = threading.Thread(target=accept_client, args=(server,))
    accept_threads.start()

    # Send offset to client nodes
    throw_threads = threading.Thread(target=start_change_time, args=())
    throw_threads.start()


if __name__ == '__main__':
    run_server('127.0.0.1', 8080)
