import time

from peer import Peer

if __name__ == '__main__':
    a = Peer("192.168.0.1",  5001)

    a.start()

    a.file_request("aboba.png")