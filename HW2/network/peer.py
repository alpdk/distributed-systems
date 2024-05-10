import socket
import threading


class Peer:
    def __init__(self, host, port, broad_cast_host="255.255.255.255", broad_cast_port=5000):
        self.host = host
        self.port = port

        self.all_ports = []

        self.broad_cast_host = broad_cast_host
        self.broad_cast_port = broad_cast_port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind((self.host, self.port))

        self.stop_flag = threading.Event()

    def file_request(self, file_name):
        if self.stop_flag.is_set():
            return

        file_name_bytes = file_name.encode('utf-8')

        self.socket.sendto(file_name_bytes, (self.broad_cast_host, self.broad_cast_port))
        print(self.broad_cast_host, self.broad_cast_port)

    def listening_request(self):
        while not self.stop_flag.is_set():
            data, addr = self.socket.recvfrom(1024)

            print(f"Received broadcast message: {data.decode('utf-8')} from {addr}")

    def start(self):
        self.stop_flag.clear()

        listening_broad_cast_request = threading.Thread(target=self.listening_request, args=())
        listening_broad_cast_request.start()

    def stop(self):
        self.stop_flag.set()
