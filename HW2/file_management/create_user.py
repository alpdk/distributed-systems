import os
import sys
import json
import pathlib

def write_in_port_to_hosts(path_to_dir, host, port):
    port_to_sock_path = os.path.join(path_to_dir, "users_data", "port_to_hosts.json")

    if not os.path.exists(port_to_sock_path):
        with open(str(port_to_sock_path), "w") as file:
            pass

    f = open(port_to_sock_path, "r")
    data_port_to_sock = json.load(f)
    f.close()

    if port in data_port_to_sock and not host in data_port_to_sock[port]:
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

    if len(data) < 4:
        print('Error: missing argument')
        sys.exit(1)
    elif len(data) > 4:
        print('Error: too much arguments')
        sys.exit(1)

    user_name = data[0]
    user_password = data[1]
    host = data[2]
    port = data[3]

    path_to_dir = pathlib.Path().resolve()
    path_to_user_folder = os.path.join(path_to_dir, "users_data", user_name)

    if not os.path.exists(path_to_user_folder):
        os.makedirs(path_to_user_folder)

        write_in_port_to_hosts(path_to_dir, host, port)

        write_user_info(path_to_dir, user_name, user_password, host, port)
