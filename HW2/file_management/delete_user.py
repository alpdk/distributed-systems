import os
import sys
import json
import pathlib
import shutil

from getting_specific_user_info import get_user_info


def add_released_port(port):
    path_to_proj_dir = pathlib.Path().resolve().parent
    path_to_user_data = os.path.join(path_to_proj_dir, "users_data")
    path_to_free_ports = os.path.join(path_to_user_data, "free_ports.json")

    free_ports = {}

    if os.path.exists(path_to_free_ports):
        with open(path_to_free_ports, 'r') as file:
            free_ports = json.load(file)

        if "free" in free_ports:
            free_ports["free"].append(port)
        else:
            free_ports["free"] = [port]


    with open(path_to_free_ports, 'w') as file:
        json.dump(free_ports, file, indent=4)


def del_user_port_and_host(port_to_sock_path, host, port):
    f = open(port_to_sock_path, "r")
    data_port_to_sock = json.load(f)
    f.close()

    if port in data_port_to_sock and host in data_port_to_sock[port]:
        data_port_to_sock[port].remove(host)

        if not data_port_to_sock[port]:
            del data_port_to_sock[port]

        add_released_port(port)

        with open(str(port_to_sock_path), "w") as json_file:
            json.dump(data_port_to_sock, json_file, indent=4)


if __name__ == '__main__':
    data = sys.argv[1:]

    if len(data) < 1:
        print('Error: missing argument')
        sys.exit(1)
    elif len(data) > 1:
        print('Error: too much arguments')
        sys.exit(1)

    user_name = data[0]

    path_to_proj_dir = pathlib.Path().resolve().parent
    path_to_user = os.path.join(path_to_proj_dir, "users_data", user_name)

    if os.path.exists(path_to_user):
        user_info = get_user_info(user_name)
        port_to_sock_path = os.path.join(path_to_proj_dir, "users_data", "port_to_hosts.json")

        del_user_port_and_host(port_to_sock_path, user_info["host"], user_info["port"])

        shutil.rmtree(path_to_user)
