import json
import os
import pathlib
import socket
import threading
import time

clients = {}


class Server:
    def __init__(self, host="127.0.0.1", port=5000):
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
        users_who_have_file = ""

        users = list(clients.keys())
        users.remove(client_name)

        for user in users:
            clients[user]["ask_sock"].send(file_name.encode("utf-8"))

            have_file = self.sock.recv(1024).decode("utf-8")

            if have_file == "1":
                users_who_have_file += user

        return users_who_have_file

    def listen_requested_file(self, client_socket, addr, client_name):
        try:
            while True:
                requested_file = client_socket.recv(1024).decode("utf-8")

                if requested_file == "":
                    print(f"Client '{client_name}' from {addr[0]}:{addr[1]} is disconnected", end="\n\n")
                    clients.pop(client_name)
                    return

                useful_users = self.make_broad_cast_request(requested_file, client_name)

                clients[client_name]["ask_sock"].send(useful_users[:1024].encode("utf-8"))

        except Exception as e:
            print(f"Error: {e}", end="\n\n")
        finally:
            if client_name in clients.keys():
                clients.pop(client_name)
            client_socket.close()

    def accept_client(self):
        try:
            while True:
                client_socket, addr = self.sock.accept()

                client_name = client_socket.recv(1024).decode("utf-8")

                user_info = self.get_host_and_port(client_name)

                clients[client_name] = {}
                clients[client_name]["sock"] = client_socket
                clients[client_name]["host"] = user_info[0]
                clients[client_name]["port"] = user_info[1]

                print(f"Accepted connection from user {client_name} with address {addr[0]}:{addr[1]}", end="\n\n")

                time.sleep(2)

                clients[client_name]["ask_sock"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clients[client_name]["ask_sock"].connect((clients[client_name]["host"], clients[client_name]["port"]))

                request_file_threads = threading.Thread(target=self.listen_requested_file,
                                                        args=(client_socket, addr, client_name))
                request_file_threads.start()

        except Exception as e:
            print(f"Error: {e}", end="\n\n")
        finally:
            self.sock.close()

    def start(self):
        try:
            self.sock.listen(5)

            accept_threads = threading.Thread(target=self.accept_client, args=())
            accept_threads.start()
        except Exception as e:
            print(f"Error: {e}", end="\n\n")
