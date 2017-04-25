from socket import *
from src.UnoDeck import *
import json

import threading

RECV_BUFFER = 1024


class UnoServer:
    def __init__(self):
        self.port_num = 0
        self.numplayers = 1
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.players = []
        self.deck = generate_deck()
        self.card_pile = []
        self.thread_list = []
        self.player_index = 0

    def create_socket(self, portnum):
        self.port_num = portnum
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_sock.bind(('', self.port_num))
        self.s_sock.listen(15)

    def accept_players(self, numplayers):
        self.numplayers = numplayers
        while len(self.players) < self.numplayers:
            (sock, address) = self.s_sock.accept()
            player = json.loads(sock.recv(RECV_BUFFER).decode())
            player['socket'] = sock
            self.players.append(player)

        self.start_game()

    def start_game(self):
        first_card = self.deck.pop()
        if first_card['type'] == 'Wild' or first_card['type'] == 'Wild 4':
            first_card['color'] = 'blue'
        self.card_pile.append(first_card)
        for player in self.players:
            hand = []
            for i in range(0, 7):
                card = self.deck.pop()
                hand.append(card)
            player['hand'] = hand
            player['turn'] = self.players[0]['player_name']
            player['socket'].send(json.dumps({'hand': player['hand'],
                                              'turn': player['turn'],
                                              'current_card': self.card_pile[len(self.card_pile) - 1]
                                              }).encode())

    def start_gamethread(self):
        game_thread = threading.Thread(target=self.run_game)
        game_thread.start()

    def run_game(self):
        winner = False
        winning_player = {}
        while not winner:
            self.receive_card()
            (winner, winning_player) = self.check_winner()
            (draw_cards, self.player_index) = self.process_card()
            self.send_turndata(draw_cards)
        self.send_winner(winning_player)

    def receive_card(self):
        player = self.players[self.player_index]
        sent_obj = json.loads(player['socket'].recv(RECV_BUFFER).decode())
        card = sent_obj['card']
        player['hand'] = sent_obj['hand']
        if card['type'] != 'skip turn':
            self.card_pile.append(card)

    def process_card(self):
        current_card = self.card_pile[len(self.card_pile) - 1]
        type = current_card['type']
        color = current_card['color']
        draw_cards = []
        player_index = (self.player_index + 1) % len(self.players)
        if type == 'Draw two':
            count = 0
            while count < 2 and self.deck != []:
                draw_cards.append(self.deck.pop())
                count += 1
        elif type == 'Reverse':
            self.players = self.players[::-1]
        elif type == 'Skip':
            player_index = (self.player_index + 2) % len(self.players)
        elif type == 'Wild 4':
            count = 0
            while count < 4 and self.deck != []:
                draw_cards.append(self.deck.pop())
                count += 1

        player = self.players[player_index]
        has_card = False
        all_cards = player['hand'] + draw_cards

        for card in all_cards:
            if card['type'] == type or card['color'] == color:
                has_card = True
                break
        if not has_card and self.deck != []:
            draw_cards.append(self.deck.pop())

        return draw_cards, player_index

    def send_turndata(self, draw_cards):
        player = self.players[self.player_index]
        current_card = self.card_pile[len(self.card_pile) - 1]
        player['socket'].send(json.dumps({'current_card': current_card, 'win': '', 'draw_cards': draw_cards}).encode())

    def check_winner(self):
        winner = False
        winning_player = {}

        #List is empty
        if not self.deck:
            winner = True
            tentative_winner = {'player': '', 'points': 10000}
            for player in self.players:
                points = 0
                for card in player['hand']:
                    type = card['type']
                    if type == 'Draw two' or type == 'Reverse' or type == 'Skip':
                        points += 20
                    elif type == 'Wild' or type == 'Wild 4':
                        points += 50
                    else:
                        points += int(type)
                if tentative_winner['points'] > points:
                    tentative_winner = {'player': player['player_name'], 'points': points}

        for player in self.players:
            if len(player['hand']) == 1:
                winner = True
                winning_player = player['player_name']

        return winner, winning_player

    def send_winner(self, winning_player):
        for player in self.players:
            player['socket'].send(json.dumps({'win': winning_player}).encode())










