from socket import *
import json


RECV_BUFFER = 1024


def main():
    c_sock = create_socket('localhost', 2121)
    join_game('AlexThyMan', c_sock)
    receive_hand(c_sock)


def create_socket(hostname, port_num):
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.connect((hostname, port_num))
    print("Connected to host!")
    return s


def join_game(player_name, c_sock):
    player_json = json.dumps({"player_name": player_name})
    c_sock.send(player_json.encode())


def receive_hand(c_sock):
    hand = json.loads(c_sock.recv(RECV_BUFFER).decode())
    print(hand)


main()
