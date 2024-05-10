import os
import sys
import pathlib
import shutil


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
    path_to_delete_file = os.path.join(path_to_proj_dir, "users_data", user_name, file_name)

    try:
        shutil.rmtree(path_to_delete_file)
        print("File deleted successfully:", path_to_delete_file)
    except OSError as e:
        print("Error deleting file:", e)