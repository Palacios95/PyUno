from socket import *
from src.UnoDeck import *
import json

RECV_BUFFER = 1024


def create_socket(port_num):
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('', port_num))
    s.listen(15)
    return s


def accept_players(s_sock, players, numplayers):

    deck = generate_deck()

    while len(players) < numplayers:
        (sock, address) = s_sock.accept()
        player = json.loads(sock.recv(RECV_BUFFER).decode())
        player['socket'] = sock
        players.append(player)
        distribute_cards(player, deck)


def distribute_cards(player, deck):
        hand = []
        for i in range(0, 7):
            card = deck.pop()
            hand.append(card)
        player['socket'].send(json.dumps(hand).encode())


#main()