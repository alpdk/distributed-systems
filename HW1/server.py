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
            clock_time_string = client_socket.recv(1024).decode("utf-8")

            if clock_time_string == "":
                print(f"Client from {addr[0]}:{addr[1]} is closed", end="\n\n")
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
        client_socket.close()


# Connect client node to server
def accept_client(server):
    try:
        while True:
            client_socket, addr = server.accept()

            print(f"Accepted connection from {addr[0]}:{addr[1]}", end="\n\n")

            time_threads = threading.Thread(target=client_time, args=(client_socket, addr))
            time_threads.start()
    except Exception as e:
        print(f"Error: {e}", end="\n\n")
    finally:
        server.close()


# Calculate averager offset time for client nodes
def get_average_offset():
    time_difference_list = list(client['time_difference']
                                for client_addr, client
                                in client_data.items())

    sum_of_clock_difference = sum(time_difference_list, timedelta(0, 0))

    average_clock_difference = 0

    if len(client_data) != 0:
        average_clock_difference = sum_of_clock_difference / len(client_data)

    return average_clock_difference


# Send average offset to client nodes
def start_change_time():
    try:
        while True:
            average_offset = get_average_offset()

            print("Average offset: ", average_offset, end="\n\n")
            print(datetime.now())

            for client in client_data:
                client_data[client]['connector'].send(str(average_offset).encode("utf-8")[:1024])

                print(f"Send update time for {client[0]}:{client[1]}", end="\n\n")

            time.sleep(5)
    except Exception as e:
        print(f"Error: {e}", end="\n\n")


# Run server node
def run_server(server_ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to the host and port
    server.bind((server_ip, port))
    # listen for incoming connections
    server.listen()
    print(f"Listening on {server_ip}:{port}", end="\n\n")

    accept_threads = threading.Thread(target=accept_client, args=(server,))
    accept_threads.start()

    throw_threads = threading.Thread(target=start_change_time, args=())
    throw_threads.start()


if __name__ == '__main__':
    run_server('127.0.0.1', 8080)
