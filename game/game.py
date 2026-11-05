import pygame
from game.constant import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE_NAME, FPS

class GameManager:
    def __init__(self):
        pygame.init()
        self.is_running = True
        self.is_fullscreen = False

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE)
        pygame.display.set_caption(TITLE_NAME)
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        

    def run(self):
        try:
            while self.is_running:
                dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
        finally:
            pygame.quit()