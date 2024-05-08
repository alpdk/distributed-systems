import os
import sys
import pathlib

if __name__ == '__main__':
    data = sys.argv[1:]

    if len(data) < 4:
        print('Error: missing argument')
        sys.exit(1)
    elif len(data) < 4:
        print('Error: too much arguments')
        sys.exit(1)

    path = pathlib.Path().resolve().parent
    path = str(path) + f"/users_data/{data[0]}"
    path = pathlib.Path(path)

    print(data[3])

    if not os.path.exists(path):
        os.makedirs(path)

        os.makedirs(pathlib.Path(str(path) + '/data'))

        f = open(pathlib.Path(str(path) + '/user_info'), "w")
        f.write(f"{data[2]} {data[3]}")
        f.close()