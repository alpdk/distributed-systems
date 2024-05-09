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

    path = pathlib.Path().resolve().parent
    path = os.path.join(path, "users_data", data[0], 'data', data[1])

    try:
        os.remove(path)  # or use os.unlink(file_path)
        print("File deleted successfully:", path)
    except OSError as e:
        print("Error deleting file:", e)
