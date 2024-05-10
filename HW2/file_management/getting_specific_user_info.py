import os
import sys
import json
import pathlib


def get_user_info(user_name):
    path_to_dir = pathlib.Path().resolve().parent
    path_to_user_folder = os.path.join(path_to_dir, "users_data", user_name)

    if os.path.exists(path_to_user_folder):
        path_to_user_info = os.path.join(path_to_user_folder, "user_info.json")

        f = open(str(path_to_user_info), "r")
        user_data = json.load(f)
        f.close()

        return user_data

    return None
