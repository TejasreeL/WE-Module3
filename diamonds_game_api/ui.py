import pygame
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

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_cards(cards, x, y):
    for i, card in enumerate(cards):
        card.rect.topleft = (x + i * 110, y)
        screen.blit(card.image, card.rect.topleft)

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False

def initialize_game_ui():
    pygame.init()
    return pygame.display.set_mode((1500, 775))

def close_game_ui():
    pygame.quit()
    sys.exit()
