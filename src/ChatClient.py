from socket import *
import json


RECV_BUFFER= 1024

class ChatClient:
    def __init__(self):
        self.client_sock = {}

    def start_client(self, hostname, port_num):
        self.create_socket(hostname, port_num)

    def create_socket(self, hostname, port_num):
        self.client_sock = socket(AF_INET, SOCK_STREAM)
        self.client_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.client_sock.connect((hostname, port_num))
        print("Connected to chat!")

    def send_message(self, player_name, message):
        self.client_sock.send(json.dumps({'player_name': player_name, 'message': message}).encode())

    def receive_messages(self):
        return json.loads(self.client_sock.recv(RECV_BUFFER).decode())['messages']
