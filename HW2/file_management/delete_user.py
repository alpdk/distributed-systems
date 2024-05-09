import os
import sys
import pathlib
import shutil

if __name__ == '__main__':
    data = sys.argv[1:]

    if len(data) < 1:
        print('Error: missing argument')
        sys.exit(1)
    elif len(data) > 1:
        print('Error: too much arguments')
        sys.exit(1)

    path = pathlib.Path().resolve()
    path = os.path.join(path, "users_data", data[0])

    if os.path.exists(path):
        shutil.rmtree(path)