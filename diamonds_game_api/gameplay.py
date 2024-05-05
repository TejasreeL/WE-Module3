import pygame
import random
import sys
from ui import *
from card import Card
from player import Player
from strategies import PlayerStrategy

def simulate_game(player_name, deck):
    # Initialize Pygame
    screen = initialize_game_ui()

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

        if diamonds:
            revealed_diamond = diamonds[0]
            draw_text("Revealed diamond:", font, BLACK, 10, 580)
            screen.blit(revealed_diamond.image, (270, 580))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                selected_card = player.select_card(pos)
                if selected_card:
                    player_bid = selected_card
                    player.hand.remove(selected_card)
                    if diamonds:
                        revealed_diamond = diamonds.pop(0)
                        computer_bid = PlayerStrategy.smart_card(computer.hand, computer.high_cards, revealed_diamond)
                        draw_text(f"Your bid: {player_bid.rank} {player_bid.suit_text}", font, BLACK, 10, 620)
                        draw_text(f"{computer.name}'s bid: {computer_bid.rank} {computer_bid.suit_text}", font, BLACK, 10, 650)
                        if player_bid.rank > computer_bid.rank:
                            winner = player
                        elif computer_bid.rank > player_bid.rank:
                            winner = computer
                        else:
                            winner = None
                        if winner:
                            winner.score += revealed_diamond.rank
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        if not diamonds:
                            running = False
                        else:
                            try:
                                computer.hand.remove(computer_bid)
                            except ValueError:
                                continue

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

    wait_for_key()
    close_game_ui()

# Load card images
deck = [Card(rank, suit) for rank in range(2, 15) for suit in ["♠", "♥", "♦"]]

simulate_game("You", deck)
