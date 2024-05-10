import time

from peer import Peer

if __name__ == '__main__':
    a = Peer("127.0.0.1",  5002)

    a.start()