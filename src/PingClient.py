from socket import *


class PingClient:
    def __init__(self):
        self.ping_sock = {}
        self.port = 2123
        self.hostname = 'localhost'

    def start_client(self, hostname, port):
        ping_sock = socket(AF_INET, SOCK_DGRAM)
        self.port = port
        self.hostname = hostname
        self.ping_sock = ping_sock

    def send_ping(self, playername):
        self.ping_sock.sendto(('Ping from %s' % playername).encode(), (self.hostname, self.port))
