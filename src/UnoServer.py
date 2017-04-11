from socket import *

from src.UnoDeck import *


def create_socket(port_num):
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('', port_num))
    s.listen(15)
    return s



def main():
    sock = create_socket(80)
    deck = generate_deck()
    print(deck)


main()
