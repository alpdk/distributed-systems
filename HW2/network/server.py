import json
import os
import pathlib
import socket
import threading
import time

clients = {}


class Server:
    def __init__(self, host="127.0.0.1", port=50000):
        self.host = host
        self.port = port

        self.connected_port = ()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

    def get_host_and_port(self, user_name):
        path_to_proj_dir = pathlib.Path().resolve().parent
        path_to_user = os.path.join(path_to_proj_dir, "users_data", user_name)

        if os.path.exists(path_to_user):
            path_to_user_info = os.path.join(path_to_user, "user_info.json")

            with open(path_to_user_info, 'r') as file:
                user_info = json.load(file)

            return user_info["host"], int(user_info["port"])

        return None

    def make_broad_cast_request(self, file_name, client_name):
        users_who_have_file = "No one"

        users = list(clients.keys())

        for user in users:
            if user == client_name:
                continue

            time.sleep(1)

            clients[user]["broadcast"].send(file_name[:1024].encode("utf-8"))

            time.sleep(1)

            have_file = clients[user]["broadcast"].recv(1024).decode("utf-8")

            if have_file == "1":
                if users_who_have_file == "No one":
                    users_who_have_file = clients[user]["host"] + ":" + str(clients[user]["port"])
                else:
                    users_who_have_file += " " + clients[user]["host"] + ":" + str(clients[user]["port"])

        return users_who_have_file

    def listen_requested_file(self, client_name):
        try:
            while True:
                requested_file = clients[client_name]["sock"].recv(1024).decode("utf-8")

                if requested_file == "":
                    print(f"Client '{client_name}' is disconnected", end="\n\n")
                    clients.pop(client_name)
                    return

                useful_users = self.make_broad_cast_request(requested_file, client_name)

                time.sleep(1)

                clients[client_name]["sock"].send(useful_users[:1024].encode("utf-8"))

                time.sleep(1)

        except Exception as e:
            print(f"Error listen...: {e}", end="\n\n")
        finally:
            clients[client_name]["sock"].close()

            if client_name in clients.keys():
                clients.pop(client_name)

    def accept_client(self):
        try:
            while True:
                client_socket, addr = self.sock.accept()

                client_name = client_socket.recv(1024).decode("utf-8")

                user_info = self.get_host_and_port(client_name)

                broadcast_client_socket, addr = self.sock.accept()

                clients[client_name] = {}
                clients[client_name]["sock"] = client_socket
                clients[client_name]["host"] = user_info[0]
                clients[client_name]["port"] = user_info[1]
                clients[client_name]["broadcast"] = broadcast_client_socket

                print(f"Accepted connection from user {client_name} with address {addr[0]}:{addr[1]}", end="\n\n")

                time.sleep(2)

                request_file_threads = threading.Thread(target=self.listen_requested_file,
                                                        args=(client_name,))
                request_file_threads.start()

        except Exception as e:
            print(f"Error accept_client: {e}", end="\n\n")
        finally:
            self.sock.close()

    def start(self):
        try:
            self.sock.listen(5)

            accept_threads = threading.Thread(target=self.accept_client, args=())
            accept_threads.start()
        except Exception as e:
            print(f"Error start: {e}", end="\n\n")
