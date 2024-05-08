import os
import sys
import pathlib

import requests
import shutil

if __name__ == '__main__':
    data = sys.argv[1:]

    if len(data) < 2:
        print('Error: missing argument')
        sys.exit(1)
    elif len(data) > 2:
        print('Error: too much arguments')
        sys.exit(1)

    source = pathlib.Path(data[1])

    path = pathlib.Path().resolve()
    destination = os.path.join(path, "users_data", data[0], 'data')

    try:
        shutil.copy(source, destination)
        print("File copied successfully from", source, "to", destination)
    except IOError as e:
        print("Unable to copy file:", e)
