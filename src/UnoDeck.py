

def generate_deck():
    card_colors = ["Red", "Green", "Yellow", "Blue"]
    card_types = range(0, 15)
    deck = []
    for color in card_colors:
        for card_type in card_types:
            deck.append({'type': card_type, 'color': color})
    return deck

