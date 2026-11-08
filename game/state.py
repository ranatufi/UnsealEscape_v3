import pygame
from abc import ABC, abstractmethod
from enum import Enum, auto
from game.constant import SCREEN_WIDTH, SCREEN_HEIGHT, TEXT_COLOR
from game.path import ImagePath

class GameState(Enum):
    TITLE = auto()
    PROLOGUE = auto()
    STORY = auto()
    EXPLORATION = auto()

class State(ABC):
    def __init__(self, game, state_manager):
        self.game = game
        self.state_manager = state_manager

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

class StateManager:
    def __init__(self, game, initial_state=GameState.TITLE):
        self.game_manager = game
        self.states = {
            GameState.TITLE: TitleState(game, self),
            GameState.PROLOGUE: PrologueState(game, self),
            GameState.STORY: StoryState(game, self),
            GameState.EXPLORATION: ExplorationState(game, self)
        }
        self.current_state = self.states[initial_state]
        self.current_state.enter()

    def change_state(self, new_state):
        if new_state not in self.states:
            raise ValueError(f"存在しないステート: {new_state}")
        if self.current_state is self.states[new_state]:
            return
        self.current_state.exit()
        self.current_state = self.states[new_state]
        self.current_state.enter()
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game_manager.is_running = False
            self.current_state.exit()
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_manager.is_running = False
                self.current_state.exit()
                return
            if event.key == pygame.K_F11:
                self.game_manager.toggle_fullscreen()
                return
        self.current_state.handle_event(event)

    def update(self, dt):
        self.current_state.update(dt)

    def draw(self, screen):
        #screen.fill(BG_COLOR)
        self.current_state.draw(screen)

class TitleState(State):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)
        self.title_image = None
        self.title_surface = None
        self.play_surface = None
        self.play_rect = None
    
    def enter(self):
        self.title_image = self.game.image_manager.image(ImagePath.BACKGROUND, "title.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.title_font = pygame.font.SysFont("Georgia", 70, bold=True)
        self.play_surface = self.title_font.render("Play", True, TEXT_COLOR)
        self.play_rect = self.play_surface.get_rect(center=(SCREEN_WIDTH // 2, 400))
    
    def exit(self):
        pass

    def update(self, dt):
        pass
    
    def draw(self, screen):
        screen.blit(self.title_image, (0, 0))
        screen.blit(self.play_surface, self.play_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)
    
    def handle_click(self, pos):
        if self.play_rect and self.play_rect.collidepoint(pos):
            self.state_manager.change_state(GameState.PROLOGUE)

class PrologueState(State):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)
    
    def enter(self):
        self.game.audio_manager.play_bgm("死神のリスト.mp3")
        pass
    
    def exit(self):
        pass

    def update(self, dt):
        pass
    
    def draw(self, screen):
        pass
    
    def handle_event(self, event):
        pass

class StoryState(State):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)
    
    def enter(self):
        pass
    
    def exit(self):
        pass

    def update(self, dt):
        pass
    
    def draw(self, screen):
        pass
    
    def handle_event(self, event):
        pass

class ExplorationState(State):
    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)
    
    def enter(self):
        pass
    
    def exit(self):
        pass

    def update(self, dt):
        pass
    
    def draw(self, screen):
        pass
    
    def handle_event(self, event):
        pass