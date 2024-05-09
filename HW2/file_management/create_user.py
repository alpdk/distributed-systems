import os
import sys
import json
import pathlib

def get_unique_host_and_port(port_to_sock_path):
    f = open(port_to_sock_path, "r")
    data_port_to_sock = json.load(f)
    f.close()

    if not bool(data_port_to_sock):
        return "192.168.0.1", 5000

    last_port = max(data_port_to_sock.keys())
    last_host = max(data_port_to_sock[last_port])

    res_port = int(last_port)
    res_host = [int(x) for x in last_host.split(".")]

    res_host[2] = (res_host[3] + 1) // 255
    res_port += (res_host[3] + 1) // 255

    res_host[3] = (res_host[3] + 1) % 255

    if res_host[3] == 0:
        res_host[3] += 1

    return ".".join(map(str, res_host)), str(res_port)

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
