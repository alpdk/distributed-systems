import json
import os
import pathlib
import socket
import threading


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

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.connect((self.server_host, self.server_port))

        self.server_sock.send(self.user_name.encode("utf-8")[:1024])

    def get_host_and_port(self, user_name):
        path_to_proj_dir = pathlib.Path().resolve().parent
        path_to_user = os.path.join(path_to_proj_dir, "users_data", user_name)

        if os.path.exists(path_to_user):
            path_to_user_info = os.path.join(path_to_user, "user_info.json")

            with open(path_to_user_info, 'r') as file:
                user_info = json.load(file)

            return user_info["host"], int(user_info["port"])

        return None