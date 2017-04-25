from socket import *
import json
import threading


RECV_BUFFER = 1024


class ChatServer:
    def __init__(self):
        self.server_sock = {}
        self.messages = []
        self.chat_socks = []

    def start_server(self, hostname, port_num):
        self.create_socket(hostname, port_num)

    def create_socket(self, port_num):

        self.server_sock = socket(AF_INET, SOCK_STREAM)
        self.server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_sock.bind(('', port_num))
        self.server_sock.listen(15)

    def accept_chat(self, chat_sock):
        while True:
            message = json.loads(chat_sock.recv(RECV_BUFFER).decode())
            self.messages.append('%s: %s\n' % (message['player_name'], message['message']))
            for sock in self.chat_socks:
                sock.send(json.dumps({'messages': self.messages}).encode())

    def accept_chats(self, numplayers, players):
        count = 0
        while count < numplayers:
            (sock, address) = self.server_sock.accept()
            self.chat_socks.append(sock)
            count += 1
        count = 0
        while count < numplayers:
            chat_thread = threading.Thread(target=self.accept_chat, args=(self.chat_socks[count],))
            chat_thread.start()
            count += 1

    def send_message(self, message):
        self.client_sock.send(json.dumps({'message': message}).encode())

    def receive_message(self):
        return json.loads(self.client_sock.recv().decode())
