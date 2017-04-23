from random import shuffle


# Generates deck for the game shuffled. 0-9 are the standard 0-9 uno cards.
# 10 is Draw two cards.
# 11 is Reverse cards.
# 12 is Skip cards.
# 13 is Wild cards.
# 14 is wild draw 4 cards.
def generate_deck():
    card_colors = ["red", "green", "yellow", "blue"]
    # Card types 0-12 are all the cards that have a color (Not wild cards).
    card_types = list(range(0, 10))
    other_types = ['Draw two', 'Reverse', 'Skip']
    card_types += other_types
    deck = []
    for color in card_colors:
        for card_type in card_types:
            deck.append({'type': card_type, 'color': color})
            # Add 2 of each except for 0.
            if not card_type == 0:
                deck.append({'type': card_type, 'color': color})
    for i in range(0, 4):
        deck.append({'type': 13, 'color': 'black'})
        deck.append({'type': 14, 'color': 'black'})

    shuffle(deck)

    return deck

