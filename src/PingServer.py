from socket import *


class PingServer:

    def __init__(self):
        self.ping_sock = {}

    def create_socket(self, port):
        ping_sock = socket(AF_INET, SOCK_DGRAM)
        ping_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        ping_sock.bind(('', port))
        self.ping_sock = ping_sock

    def accept_pings(self):
        while True:
            data, addr = self.ping_sock.recvfrom(1024)
            return 'Ping received from %s\n' % data.decode()



