import json
import os
import pathlib
import socket
import threading
import time


class Peer:
    def __init__(self, user_name, server_host="127.0.0.1", server_port=5000):
        host_and_port = self.get_host_and_port(user_name)

        if host_and_port == None:
            raise Exception("This user does not exist!!!")

        self.user_name = user_name

        self.host = host_and_port[0]
        self.port = host_and_port[1]

        self.server_host = server_host
        self.server_port = server_port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind((self.host, self.port))

        self.request_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.request_server_sock.connect((self.server_host, self.server_port))

        time.sleep(1)

        self.request_server_sock.send(self.user_name.encode("utf-8")[:1024])

        time.sleep(1)

        self.broadcast_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.broadcast_server_sock.connect((self.server_host, self.server_port))

    def get_host_and_port(self, user_name):
        path_to_proj_dir = pathlib.Path().resolve().parent
        path_to_user = os.path.join(path_to_proj_dir, "users_data", user_name)

        if os.path.exists(path_to_user):
            path_to_user_info = os.path.join(path_to_user, "user_info.json")

            with open(path_to_user_info, 'r') as file:
                user_info = json.load(file)

            return user_info["host"], int(user_info["port"])

        return None

    def request_file_threads(self):
        try:
            while True:
                file_name = self.broadcast_server_sock.recv(1024).decode("utf-8")

                path_to_proj_dir = pathlib.Path().resolve().parent
                path_to_file_dir = os.path.join(path_to_proj_dir, "users_data", self.user_name, file_name)

                if os.path.exists(path_to_file_dir):
                    res = "1"
                else:
                    res = "0"

                time.sleep(1)

                self.broadcast_server_sock.send(res.encode("utf-8")[:1024])

                time.sleep(5)
        except Exception as e:
            print(f"Error: {e}", end="\n\n")
        finally:
            self.request_server_sock.close()

    def request_file(self, file_name):
        time.sleep(1)
        self.request_server_sock.send(file_name.encode("utf-8")[:1024])
        time.sleep(1)

    def start(self):
        try:
            request_file_threads = threading.Thread(target=self.request_file_threads,
                                                    args=())
            request_file_threads.start()

            while True:
                file_name = input("What file you search: ")

                self.request_file(file_name)

                time.sleep(3)

                user_names = self.request_server_sock.recv(1024).decode("utf-8")

                print(f"Users with this file: {user_names}")
        except Exception as e:
            print(f"Error: {e}", end="\n\n")
        finally:
            self.sock.close()
