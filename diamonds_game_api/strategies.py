import random

class PlayerStrategy:
    @staticmethod
    def random_card(hand):
        return random.choice(hand)

    @staticmethod
    def smart_card(hand, high_cards, revealed_diamond):
        remaining_high_cards = [card for card in high_cards if card.rank >= revealed_diamond.rank]
        remaining_low_cards = [card for card in hand if card.rank < revealed_diamond.rank]

        if remaining_high_cards:
            bid_card = min(remaining_high_cards, key=lambda card: card.rank)
        elif remaining_low_cards:
            bid_card = max(remaining_low_cards, key=lambda card: card.rank)
        else:
            bid_card = min(hand, key=lambda card: card.rank)
        if len(hand) > len(high_cards) and len(hand) > len(remaining_high_cards):
            bid_threshold = revealed_diamond.rank * 0.75
            if bid_card.rank >= bid_threshold and high_cards:
                bid_card = min(high_cards, key=lambda card: card.rank)

        return bid_card
