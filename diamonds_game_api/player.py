class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand.copy()
        self.score = 0
        self.high_cards = [card for card in hand if card.rank >= 11]

    def select_card(self, pos):
        for card in self.hand:
            if card.rect.collidepoint(pos):
                return card
        return None
