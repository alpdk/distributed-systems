import hashlib
import json
import os
import sys
import pathlib


def merge_parts(path_to_file_dir, file_name):
    path_to_file_info = os.path.join(path_to_file_dir, "file_info.json")

    if not os.path.exists(path_to_file_info):
        sys.exit("File info file does not exist")

    with open(path_to_file_info, "r") as f:
        info_dict = json.load(f)

    lst = os.listdir(path_to_file_dir)
    number_files = len(lst)

    if number_files - 1 != info_dict["part_counts"]:
        sys.exit("Incorrect count of parts")

    # part_dict = {}
    #
    # for key in info_dict.keys():
    #     if key == "part_counts" or key == "extension":
    #         continue
    #
    #     path_to_file_part = os.path.join(path_to_file_dir, key)
    #
    #     if not os.path.exists(path_to_file_part):
    #         sys.exit(f"There is no file part: {key}")
    #
    #     with open(path_to_file_part, "rb") as f:
    #         read_data = f.read()
    #
    #         part_dict[hashlib.md5(read_data).hexdigest()] = read_data
    #
    # res = bytearray()
    #
    # for key in info_dict.keys():
    #     if key == "part_counts" or key == "extension":
    #         continue
    #
    #     for check_sum in part_dict.keys():
    #         if check_sum == info_dict[key]["checksum"]:
    #             res.extend(part_dict[check_sum])
    #             break
    #
    #
    # path_to_proj_dir = pathlib.Path().resolve().parent
    # path_to_user_dir = os.path.join(path_to_proj_dir, "users_data", user_name)
    # path_to_directory_with_combined_files = os.path.join(path_to_user_dir, "combined_files")
    #
    # if not os.path.exists(path_to_directory_with_combined_files):
    #     os.mkdir(path_to_directory_with_combined_files)
    #

    path_to_proj_dir = pathlib.Path().resolve().parent
    path_to_user_dir = os.path.join(path_to_proj_dir, "users_data", user_name)
    path_to_directory_with_combined_files = os.path.join(path_to_user_dir, "combined_files")
    path_to_combined_file = os.path.join(path_to_directory_with_combined_files, file_name + info_dict["extension"])

    res = bytearray()

    for key in info_dict.keys():
        if key == "part_counts" or key == "extension":
            continue

        path_to_file_part = os.path.join(path_to_file_dir, key)

        if not os.path.exists(path_to_file_part):
            sys.exit(f"There is no file part: {key}")

        file_part_data = bytearray()

        with open(path_to_file_part, "rb") as f:
            read_data = f.read()

            file_part_data = read_data

        res.extend(file_part_data)

    with open(path_to_combined_file, "wb") as f:
        f.write(res)


if __name__ == '__main__':
    data = sys.argv[1:]

    if len(data) < 2:
        print('Error: missing argument')
        sys.exit(1)
    elif len(data) > 2:
        print('Error: too much arguments')
        sys.exit(1)

    user_name = data[0]
    file_name = data[1]

    path_to_proj_dir = pathlib.Path().resolve().parent
    path_to_file_dir = os.path.join(path_to_proj_dir, "users_data", user_name, file_name)

    if os.path.exists(path_to_file_dir):
        merge_parts(path_to_file_dir, file_name)
