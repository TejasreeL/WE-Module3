import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 775
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Diamonds Card Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.SysFont(None, 30)

# Mapping of suit symbols to text
SUIT_TEXT_MAP = {"♠": "spade", "♥": "heart", "♦": "diamond", "♣": "club"}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.suit_text = SUIT_TEXT_MAP.get(suit)
        self.image = pygame.image.load(f"images/{rank}{self.suit_text}.png")  # Load image from file
        self.image = pygame.transform.scale(self.image, (100, 140))
        self.rect = self.image.get_rect()

    def __str__(self):
        return f"{self.rank}{self.suit_text}"

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand.copy()
        self.score = 0
        self.high_cards = [card for card in hand if card.rank >= 11]  # Track high cards

    def select_card(self, pos):
        for card in self.hand:
            if card.rect.collidepoint(pos):
                return card
        return None

    def play_smart_card(self, revealed_diamond):
        remaining_high_cards = [card for card in self.high_cards if card.rank >= revealed_diamond.rank]
        remaining_low_cards = [card for card in self.hand if card.rank < revealed_diamond.rank]
        
        if remaining_high_cards:
            bid_card = min(remaining_high_cards, key=lambda card: card.rank)
        elif remaining_low_cards:
            bid_card = max(remaining_low_cards, key=lambda card: card.rank)
        else:
            bid_card = min(self.hand, key=lambda card: card.rank)
        if len(self.hand) > len(self.high_cards) and len(self.hand) > len(remaining_high_cards):
            bid_threshold = revealed_diamond.rank * 0.75
            if bid_card.rank >= bid_threshold and self.high_cards:
                bid_card = min(self.high_cards, key=lambda card: card.rank)
        
        self.hand.remove(bid_card)
        if bid_card in self.high_cards:
            self.high_cards.remove(bid_card)
            
        return bid_card

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_cards(cards, x, y):
    for i, card in enumerate(cards):
        card.rect.topleft = (x + i * 110, y)
        screen.blit(card.image, card.rect.topleft)

def simulate_game(player_name, deck):
    random.shuffle(deck)
    diamonds = [card for card in deck if card.suit == "♦"]
    player_hand = [card for card in deck if card.suit == "♠"]
    computer_hand = random.sample([card for card in deck if card.suit == "♣" or card.suit == "♥"], len(player_hand))

    player = Player(player_name, player_hand)
    computer = Player("Computer", computer_hand)

    running = True
    while running:
        screen.fill(WHITE)
        draw_text("Your hand:", font, BLACK, 10, 10)
        draw_cards(player.hand, 10, 50)
        draw_text("Computer's hand:", font, BLACK, 10, 300)
        draw_cards(computer.hand, 10, 340)

        # Draw the revealed diamond card if available
        if diamonds:
            revealed_diamond = diamonds[0]
            draw_text("Revealed diamond:", font, BLACK, 10, 580)
            screen.blit(revealed_diamond.image, (270, 580))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                selected_card = player.select_card(pos)
                if selected_card:
                    player_bid = selected_card
                    player.hand.remove(selected_card)  # Remove selected card from player's hand
                    if diamonds:
                        revealed_diamond = diamonds.pop(0)
                        computer_bid = computer.play_smart_card(revealed_diamond)  # Computer's bid
                        draw_text(f"Your bid: {player_bid.rank} {player_bid.suit_text}", font, BLACK, 10, 620)
                        draw_text(f"{computer.name}'s bid: {computer_bid.rank} {computer_bid.suit_text}", font, BLACK, 10, 650)
                        # Determine winner
                        if player_bid.rank > computer_bid.rank:
                            winner = player
                        elif computer_bid.rank > player_bid.rank:
                            winner = computer
                        else:
                            winner = None
                        if winner:
                            winner.score += revealed_diamond.rank
                        pygame.display.flip()
                        pygame.time.delay(2000)  # Delay to show result
                        if not diamonds:
                            running = False
                        else:
                            try:
                                computer.hand.remove(computer_bid)  # Remove computer's bid card
                            except ValueError:
                                continue

    # Print final scores
    screen.fill(WHITE)
    draw_text("Game Over! Scores:", font, BLACK, 10, 10)
    draw_text(f"{player.name}: {player.score}", font, BLACK, 10, 50)
    draw_text(f"{computer.name}: {computer.score}", font, BLACK, 10, 100)

    if player.score > computer.score:
        draw_text(f"{player.name} wins!", font, GREEN, 10, 150)
    elif computer.score > player.score:
        draw_text(f"{computer.name} wins!", font, RED, 10, 150)
    else:
        draw_text("It's a tie!", font, BLACK, 10, 150)

    draw_text("Press any key to exit...", font, BLACK, 10, 200)
    pygame.display.flip()

    # Wait for any key press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False

    pygame.quit()
    sys.exit()

# Load card images
deck = [Card(rank, suit) for rank in range(2, 15) for suit in ["♠", "♥", "♦"]]

# Example usage
simulate_game("You", deck)
