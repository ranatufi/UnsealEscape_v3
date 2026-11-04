import pygame
from game.screen import ScreenManager
from game.constant import FPS

class GameManager:
    def __init__(self):
        pygame.init()
        self.is_running = True

        self.screen_manager = ScreenManager()

    def run(self):
        try:
            while self.is_running:
                dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
        finally:
            pygame.quit()