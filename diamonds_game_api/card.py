import pygame

# Mapping of suit symbols to text
SUIT_TEXT_MAP = {"♠": "spade", "♥": "heart", "♦": "diamond", "♣": "club"}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.suit_text = SUIT_TEXT_MAP.get(suit)
        self.image = pygame.image.load(f"images/{rank}{self.suit_text}.png")
        self.image = pygame.transform.scale(self.image, (100, 140))
        self.rect = self.image.get_rect()

    def __str__(self):
        return f"{self.rank}{self.suit_text}"
