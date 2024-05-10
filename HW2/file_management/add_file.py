import os
import sys
import json
import pathlib
import hashlib


def save_file(local_path_to_file, path_to_file_dir, file_name):
    source = pathlib.Path(local_path_to_file)

    counter = 1
    chunk_size = 800

    with open(source, "rb") as file:
        data_json_files_info = {}

        while True:

            chunk = file.read(chunk_size)

            if not chunk:
                break

            file_part_name = file_name + "_" + str(counter)
            path_to_file_part = os.path.join(path_to_file_dir, file_part_name)

            with open(str(path_to_file_part), "wb") as write_file:
                write_file.write(chunk)

            data_json_files_info[file_part_name] = {}

            data_json_files_info[file_part_name]["checksum"] = hashlib.md5(chunk).hexdigest()
            data_json_files_info[file_part_name]["part"] = counter

            counter += 1

        path_to_json_info = os.path.join(path_to_file_dir, "file_info.json")

        file_extension = os.path.splitext(local_path_to_file)[1]

        data_json_files_info["extension"] = file_extension

        with open(str(path_to_json_info), "w") as json_file:
            json.dump(data_json_files_info, json_file, indent=4)


if __name__ == '__main__':
    data = sys.argv[1:]

    if len(data) < 3:
        print('Error: missing argument')
        sys.exit(1)
    elif len(data) > 3:
        print('Error: too much arguments')
        sys.exit(1)

    user_name = data[0]
    file_name = data[1]
    local_path_to_file = data[2]

    path_to_proj_dir = pathlib.Path().resolve().parent
    path_to_file_dir = os.path.join(path_to_proj_dir, "users_data", user_name, file_name)

    if not os.path.exists(path_to_file_dir):
        os.makedirs(path_to_file_dir)

        save_file(local_path_to_file, path_to_file_dir, file_name)