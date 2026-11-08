import pygame
from game.constant import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE_NAME, FPS, BACKGROUND_COLOR
from game.path import CharacterPath
from game.audio import AudioManager
from game.image import ImageManager
from game.state import StateManager

class GameManager:
    def __init__(self):
        pygame.init()
        self.is_running = True
        self.is_fullscreen = False

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE)
        pygame.display.set_caption(TITLE_NAME)
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.image_manager = ImageManager()

        icon = self.image_manager.image(CharacterPath.RIRI, "riri_mini.png")
        pygame.display.set_icon(icon)

        self.audio_manager = AudioManager()
        self.state_manager = StateManager(self)
        self.clock = pygame.time.Clock()

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    def pos_to_surface(self, pos):
        window_width, window_height = self.screen.get_size()
        scale = min(window_width / SCREEN_WIDTH, window_height / SCREEN_HEIGHT)
        scaled_width = SCREEN_WIDTH * scale
        scaled_height = SCREEN_HEIGHT * scale
        offset_x = (window_width - scaled_width) // 2
        offset_y = (window_height - scaled_height) // 2
        if not (offset_x <= pos[0] <= offset_x + scaled_width and offset_y <= pos[1] <= offset_y + scaled_height):
            return None
        surface_x = (pos[0] - offset_x) / scale
        surface_y = (pos[1] - offset_y) / scale
        return (int(surface_x), int(surface_y))
    
    def process_event(self, event):
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            pos = self.pos_to_surface(event.pos)
            if pos is None:
                return
            attributes = event.dict.copy()
            attributes['pos'] = pos
            if event.type == pygame.MOUSEMOTION:
                window_width, window_height = self.screen.get_size()
                scale = min(window_width / SCREEN_WIDTH, window_height / SCREEN_HEIGHT)
                rel = getattr(event, 'rel', (0, 0))
                attributes['rel'] = (rel[0] / scale, rel[1] / scale)
            event = pygame.event.Event(event.type, attributes)
        self.state_manager.handle_event(event)
    
    def process_draw(self):
        self.state_manager.draw(self.surface)
        window_width, window_height = self.screen.get_size()
        scale = min(window_width / SCREEN_WIDTH, window_height / SCREEN_HEIGHT)
        scaled_width = max(1, round(SCREEN_WIDTH * scale))
        scaled_height = max(1, round(SCREEN_HEIGHT * scale))
        offset_x = (window_width - scaled_width) // 2
        offset_y = (window_height - scaled_height) // 2
        
        self.screen.fill(BACKGROUND_COLOR)
        scaled_surface = pygame.transform.scale(self.surface, (scaled_width, scaled_height))
        self.screen.blit(scaled_surface, (offset_x, offset_y))
        pygame.display.flip()

    def run(self):
        try:
            while self.is_running:
                dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
                for event in pygame.event.get():
                    self.process_event(event)
                    if not self.is_running:
                        break
                if not self.is_running:
                    break
                self.state_manager.update(dt)
                self.process_draw()
        finally:
            self.audio_manager.close()
            pygame.quit()