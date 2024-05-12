import os
import sys
import json
import pathlib

def get_unique_host_and_port(port_to_sock_path):
    f = open(port_to_sock_path, "r")
    data_port_to_sock = json.load(f)
    f.close()

    host = "127.0.0.1"

    path_to_proj_dir = pathlib.Path().resolve().parent
    path_to_user_data = os.path.join(path_to_proj_dir, "users_data")
    path_to_free_ports = os.path.join(path_to_user_data, "free_ports.json")

    if os.path.exists(path_to_free_ports):

        with open(path_to_free_ports, 'r') as file:
            free_ports = json.load(file)

        if free_ports:
            port = int(min(free_ports["free"]))

            free_ports["free"].remove(str(port))

            if not free_ports["free"]:
                del free_ports["free"]

            with open(path_to_free_ports, 'w') as file:
                json.dump(free_ports, file, indent=4)

            if not free_ports:
                os.remove(path_to_free_ports)
    elif not bool(data_port_to_sock):
        return host, str(5001)
    else:
        port = int(max(data_port_to_sock.keys())) + 1


    return host, str(port)

def write_in_port_to_hosts(path_to_dir, host, port):
    port_to_sock_path = os.path.join(path_to_dir, "users_data", "port_to_hosts.json")

    if not os.path.exists(port_to_sock_path):
        with open(str(port_to_sock_path), "w") as file:
            pass

    f = open(port_to_sock_path, "r")
    data_port_to_sock = json.load(f)
    f.close()

    if port in data_port_to_sock and (not host in data_port_to_sock[port]):
        data_port_to_sock[port].append(host)
    else:
        data_port_to_sock[port] = [host]

    with open(str(port_to_sock_path), "w") as json_file:
        json.dump(data_port_to_sock, json_file, indent=4)

def write_user_info(path_to_dir, user_name, user_password, host, port):
    user_info_path = os.path.join(path_to_dir, "users_data", user_name, "user_info.json")

    user_info = {"name": user_name,
                 "password": user_password,
                 "host": host,
                 "port": port}

    with open(str(user_info_path), "w") as json_file:
        json.dump(user_info, json_file, indent=4)

if __name__ == '__main__':
    data = sys.argv[1:]

    if len(data) < 2:
        print('Error: missing argument')
        sys.exit(1)
    elif len(data) > 2:
        print('Error: too much arguments')
        sys.exit(1)

    user_name = data[0]
    user_password = data[1]

    path_to_dir = pathlib.Path().resolve().parent
    path_to_user_folder = os.path.join(path_to_dir, "users_data", user_name)

    if not os.path.exists(path_to_user_folder):
        os.makedirs(path_to_user_folder)

        port_to_sock_path = os.path.join(path_to_dir, "users_data", "port_to_hosts.json")
        host, port = get_unique_host_and_port(port_to_sock_path)

        write_in_port_to_hosts(path_to_dir, host, port)

        write_user_info(path_to_dir, user_name, user_password, host, port)
