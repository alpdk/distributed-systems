import socket
import threading
import time
from datetime import datetime, timedelta

# def handle_client(client_socket, addr):
#     try:
#         while True:
#             # receive and print client messages
#             request = client_socket.recv(1024).decode("utf-8")
#             if request.lower() == "close":
#                 client_socket.send("closed".encode("utf-8"))
#                 break
#             print(f"Received: {request}")
#             # convert and send accept response to the client
#             response = "accepted"
#             client_socket.send(response.encode("utf-8"))
#     except Exception as e:
#         print(f"Error when handling client: {e}")
#     finally:
#         client_socket.close()
#         print(f"Connection to client ({addr[0]}:{addr[1]}) closed")
#
# def run_server(server_ip, port):
#     try:
#         server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         # bind the socket to the host and port
#         server.bind((server_ip, port))
#         # listen for incoming connections
#         server.listen()
#         print(f"Listening on {server_ip}:{port}")
#
#         while True:
#             # accept a client connection
#             client_socket, addr = server.accept()
#             print(f"Accepted connection from {addr[0]}:{addr[1]}")
#             # start a new thread to handle the client
#             thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
#             thread.start()
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         server.close()

client_data = {}

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

def get_average_offset():
    time_difference_list = list(client['time_difference']
                                for client_addr, client
                                in client_data.items())

    sum_of_clock_difference = sum(time_difference_list, timedelta(0, 0))

    average_clock_difference = 0

    if len(client_data) != 0:
        average_clock_difference = sum_of_clock_difference / len(client_data)

    return average_clock_difference

def start_change_time():
    try:
        while True:
            average_offset = get_average_offset()

            print("Average offset: ", average_offset, end="\n\n")

            for client in client_data:
                synchronized_time = datetime.now() + average_offset

                client_data[client]['connector'].send(str(synchronized_time).encode("utf-8")[:1024])

                print(f"Send update time for {client[0]}:{client[1]}", end="\n\n")

            time.sleep(5)
    except Exception as e:
        print(f"Error: {e}", end="\n\n")


def run_server(server_ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to the host and port
    server.bind((server_ip, port))
    # listen for incoming connections
    server.listen()
    print(f"Listening on {server_ip}:{port}", end="\n\n")

    accept_threads = threading.Thread(target=accept_client, args=(server, ))
    accept_threads.start()

    throw_threads = threading.Thread(target=start_change_time, args=())
    throw_threads.start()


if __name__ == '__main__':
    run_server('127.0.0.1', 8080)
