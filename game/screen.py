import pygame
from game.constant import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE_NAME

class ScreenManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(TITLE_NAME)