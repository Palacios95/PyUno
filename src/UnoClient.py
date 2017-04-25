from socket import *
import json
import threading

RECV_BUFFER = 1024


class UnoClient:
    def __init__(self):
        self.player = {}
        self.client_sock = {}
        self.turn = {}
        self.current_card = {}
        self.win = {}
        self.your_turn = False
        self.cards_drawn = []

    def create_socket(self, hostname, port_num):
        self.client_sock = socket(AF_INET, SOCK_STREAM)
        self.client_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.client_sock.connect((hostname, port_num))
        print("Connected to host!")

    def join_game(self, player_name):
        self.player = {"player_name": player_name}
        self.client_sock.send(json.dumps(self.player).encode())

    def start_game(self):
        starting_dict = json.loads(self.client_sock.recv(RECV_BUFFER).decode())
        self.turn = starting_dict['turn']
        self.player['hand'] = starting_dict['hand']
        self.current_card = starting_dict['current_card']

    def send_card(self, card):
        self.player['hand'].remove(card)
        self.client_sock.send(json.dumps({'card': card, 'hand': self.player['hand']}).encode())

    def wait_turndata(self):
        turndata = json.loads(self.client_sock.recv(RECV_BUFFER).decode())
        self.win = turndata['win']
        if not self.win:
            self.current_card = turndata['current_card']
            self.cards_drawn = turndata['draw_cards']
            self.draw_cards(self.cards_drawn)



    def draw_cards(self, cards):
        for card in cards:
            self.player['hand'].append(card)

    def receive_card(self):
        return json.loads(self.client_sock.recv(RECV_BUFFER).decode())

    def change_cardcolor(self, wild_card, color):
        for card in self.player['hand']:
            if card['type'] == wild_card['type']:
                card['color'] = color

