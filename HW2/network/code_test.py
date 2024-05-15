import os
import pathlib

path_to_proj_dir = pathlib.Path().resolve().parent
path_to_file_dir = os.path.join(path_to_proj_dir, "users_data", "user_2", "suzaku")

print("Start save file by path: ", path_to_file_dir)

if not os.path.exists(path_to_file_dir):
    os.makedirs(path_to_file_dir)