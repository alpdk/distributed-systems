import os
import sys
import pathlib

if __name__ == '__main__':
    data = sys.argv[1:]

    if len(data) < 4:
        print('Error: missing argument')
        sys.exit(1)
    elif len(data) > 4:
        print('Error: too much arguments')
        sys.exit(1)

    path = pathlib.Path().resolve().parent
    path = os.path.join(path, "users_data", data[0])

    if not os.path.exists(path):
        os.makedirs(path)

        os.makedirs(os.path.join(path, 'data'))

        f = open(pathlib.Path(str(path) + '/user_info'), "w")
        f.write(f"{data[2]} {data[3]}")
        f.close()