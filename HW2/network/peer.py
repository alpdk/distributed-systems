import json
import math
import os
import pathlib
import socket
import threading
import time
import random


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

    def transpose_string_to_list(self, users):
        res = []

        split_str = users.split()

        for i in split_str:
            strings = i.split(":")
            res.append((strings[0], int(strings[1])))

        return split_str

    def save_files(self, dictionary, data, file_name):
        path_to_proj_dir = pathlib.Path().resolve().parent
        path_to_file_dir = os.path.join(path_to_proj_dir, "users_data", self.user_name, file_name)

        print("Start save file by path: ", path_to_file_dir)

        if not os.path.exists(path_to_file_dir):
            os.makedirs(path_to_file_dir)

            for sub_file_key in dictionary.keys():
                if sub_file_key == "extension":
                    continue

                sub_file_name = sub_file_key
                path_to_file_part = os.path.join(path_to_file_dir, sub_file_name)

                with open(str(path_to_file_part), "wb") as write_file:
                    write_file.write(data[dictionary[sub_file_key]["part"] - 1])

        path_to_file_info = os.path.join(path_to_file_dir, "file_info.json")

        with open(str(path_to_file_info), "w") as json_file:
            json.dump(dictionary, json_file, indent=4)

    def direct_request(self, addresses, file_name):
        who_will_be_asked = random.randint(0, len(addresses) - 1)

        will_ask = addresses[who_will_be_asked].split(":")
        will_ask[1] = int(will_ask[1])

        direct_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        direct_sock.connect((will_ask[0], will_ask[1]))

        direct_sock.send(file_name.encode("utf-8")[:1024])

        count_of_files = int(direct_sock.recv(1024).decode("utf-8"))

        data = []

        for i in range(count_of_files):
            file_data = direct_sock.recv(1024)

            data.append(file_data)

        count_of_json_parts = int(direct_sock.recv(1024).decode())

        json = ""

        for i in range(count_of_json_parts):
            json_part = direct_sock.recv(1024).decode("utf-8")

            json = json + json_part

        dictionary = eval(json)

        self.save_files(dictionary, data, file_name)

    def start_sending_file(self, client_socket, addr, file_name):
        path_to_proj_dir = pathlib.Path().resolve().parent
        path_to_file_dir = os.path.join(path_to_proj_dir, "users_data", self.user_name, file_name)

        lst_len = len(os.listdir(path_to_file_dir))

        time.sleep(0.5)

        client_socket.send(str(lst_len - 1).encode("utf-8")[:1024])

        for i in range(1, lst_len):
            path_to_file_part = os.path.join(path_to_file_dir, file_name + "_" + str(i))

            with open(str(path_to_file_part), "rb") as file:
                time.sleep(0.5)
                client_socket.send(file.read())

        path_to_file_inf = os.path.join(path_to_file_dir, "file_info.json")
        f = open(path_to_file_inf)

        file_info = json.load(f)

        string_file_info = str(file_info).encode("utf-8")

        count_of_send = math.ceil(len(string_file_info) / 1024)

        time.sleep(0.5)

        client_socket.send(str(count_of_send).encode("utf-8")[:1024])

        for i in range(0, count_of_send):
            time.sleep(0.5)

            client_socket.send(string_file_info[i * 1024:(min((i + 1) * 1024, len(string_file_info)))])

        client_socket.close()


    def direct_request_file(self):
        while True:
            client_socket, addr = self.sock.accept()

            file_requested = client_socket.recv(1024).decode("utf-8")
            self.start_sending_file(client_socket, addr, file_requested)

    def start(self):
        try:
            self.sock.listen()

            request_file_threads = threading.Thread(target=self.request_file_threads,
                                                    args=())
            request_file_threads.start()

            direct_request_threads = threading.Thread(target=self.direct_request_file,
                                                    args=())
            direct_request_threads.start()

            while True:
                file_name = input("What file you search: ")

                self.request_file(file_name)

                time.sleep(3)

                users_with_file = self.request_server_sock.recv(1024).decode("utf-8")

                if users_with_file == "No one":
                    print(f"Nobody hos file")
                    continue

                addresses = self.transpose_string_to_list(users_with_file)

                self.direct_request(addresses, file_name)
        except Exception as e:
            print(f"Error: {e}", end="\n\n")
        finally:
            self.sock.close()
