import pygame
from abc import ABC, abstractmethod
from enum import Enum, auto
from game.constant import SCREEN_WIDTH, SCREEN_HEIGHT
from game.constant import BACKGROUND_COLOR, TEXT_COLOR, ARROW_COLOR
from game.constant import PROLOGUE_TEXT, STORY_TEXT
from game.path import FontPath, ImagePath
from game.path import CharacterPath, MapPath
from game.exploration.collision_map import CollisionMap
from game.exploration.item_manager import ItemManager

class GameState(Enum):
    TITLE = auto()
    PROLOGUE = auto()
    STORY = auto()
    EXPLORATION = auto()
    END = auto()

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
            GameState.EXPLORATION: ExplorationState(game, self),
            GameState.END: EndState(game, self),
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
    
    def enter(self):
        self.title_image = self.game.image_manager.image(ImagePath.BACKGROUND, "title.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.title_font = self.game.font_manager.font(FontPath.GENKAI, "genkai-mincho.ttf", 70)
        self.play_surface = self.title_font.render("Play", True, TEXT_COLOR)
        self.play_rect = self.play_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.game.audio_manager.stop_bgm()
    
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

        self.target_y = SCREEN_HEIGHT // 2
        self.scroll_speed = 100.0
    
    def create_text_surface(self, text, font, color, max_width):
        lines = []
        for paragraph_line in text.split("\n"):
            if not paragraph_line:
                lines.append("")
                continue
            current_line = ""
            for char in paragraph_line:
                candidate = current_line + char
                if current_line and font.size(candidate)[0] > max_width:
                    lines.append(current_line)
                    current_line = char
                else:
                    current_line = candidate
            if current_line:
                lines.append(current_line)
        
        line_height = font.get_linesize() + 8
        surface_height = max(1, len(lines) * line_height)
        surface = pygame.Surface((max_width, surface_height), pygame.SRCALPHA)
        for index, line in enumerate(lines):
            if not line:
                continue
            rendered_line = font.render(line, True, color)
            rect = rendered_line.get_rect(centerx=max_width // 2, y=index * line_height)
            surface.blit(rendered_line, rect)
        
        return surface

    def enter(self):
        self.is_scroll_finished = False
        self.game.audio_manager.play_bgm("死神のリスト.mp3")

        self.prologue_font = self.game.font_manager.font(FontPath.ORADANO, "OradanoGSRR.ttf", 40)
        self.prologue_surface = self.create_text_surface(PROLOGUE_TEXT, self.prologue_font, TEXT_COLOR, SCREEN_WIDTH)
        self.arrow_font = self.game.font_manager.font(FontPath.POINTERS, "pointers.ttf", 60)
        self.arrow_surface = self.arrow_font.render("4", True, ARROW_COLOR)
        self.arrow_rect = self.arrow_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 5 // 6))
        
        self.scroll_y = (SCREEN_HEIGHT + self.prologue_surface.get_height() // 2)
        
    def exit(self):
        pass

    def update(self, dt):
        if self.is_scroll_finished:
            return
        self.scroll_y -= self.scroll_speed * dt
        if self.scroll_y <= self.target_y:
            self.scroll_y = self.target_y
            self.is_scroll_finished = True
    
    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)
        screen.blit(self.prologue_surface, self.prologue_surface.get_rect(center=(SCREEN_WIDTH // 2, round(self.scroll_y))))
        if self.is_scroll_finished:
            screen.blit(self.arrow_surface, self.arrow_rect)
    
    def handle_event(self, event):
        if (self.is_scroll_finished and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            if self.arrow_rect and self.arrow_rect.collidepoint(event.pos):
                self.handle_click(event.pos)

    def handle_click(self, pos):
        self.state_manager.change_state(GameState.STORY)

class StoryState(State):
    STORY_LINES = STORY_TEXT
    BGM = "死神のリスト.mp3"
    NEXT_STATE = GameState.EXPLORATION

    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)
        self.story_line = list(self.STORY_LINES)
        self.line_index = 0
        self.text = ""
        self.display_text = ""
        self.char_index = 0
        self.type_timer = 0.0
        self.auto_timer = 0.0
        self.type_interval = 0.06
        self.auto_interval = 2.5
        self.is_auto = False
        self.is_typing = False
        self.background = None
        self.character = None
        self.textbox = None
        self.text_rect = pygame.Rect(100, 580, 810, 145)
        self.next_rect = pygame.Rect(900, 680, 48, 40)
        self.auto_rect = pygame.Rect(850, 20, 70, 34)
        self.skip_rect = pygame.Rect(930, 20, 70, 34)

    def show_current_line(self):
        if self.line_index >= len(self.story_line):
            self.state_manager.change_state(self.NEXT_STATE)
            return
        self.text = self.story_line[self.line_index]
        self.display_text = ""
        self.char_index = 0
        self.type_timer = 0.0
        self.auto_timer = 0.0
        self.is_typing = True
    
    def enter(self):
        self.game.audio_manager.play_bgm(self.BGM)
        self.background = self.game.image_manager.image(
            ImagePath.BACKGROUND, "story_background.png", (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.character = self.game.image_manager.image(
            CharacterPath.RIRI, "riri.png", (1000, 1000)
        )
        self.textbox = self.game.image_manager.image(
            ImagePath.UI, "textbox.png", (920, 230)
        )
        self.text_font = self.game.font_manager.font(FontPath.ORADANO, "OradanoGSRR.ttf", 27)
        self.button_font = self.game.font_manager.font(FontPath.ORADANO, "OradanoGSRR.ttf", 20)
        self.line_index = 0
        self.is_auto = False
        self.show_current_line()
    
    def exit(self):
        pass

    def update(self, dt):
        if self.is_typing:
            self.type_timer += dt
            while self.type_timer >= self.type_interval and self.is_typing:
                self.type_timer -= self.type_interval
                self.char_index += 1
                self.display_text = self.text[:self.char_index]
                if self.char_index >= len(self.text):
                    self.is_typing = False
                    self.auto_timer = 0.0
        elif self.is_auto:
            self.auto_timer += dt
            if self.auto_timer >= self.auto_interval:
                self.line_index += 1
                self.show_current_line()
    
    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BACKGROUND_COLOR)
        if self.character:
            screen.blit(self.character, (320, 0))
        if self.textbox:
            screen.blit(self.textbox, (52, 510))
        else:
            pygame.draw.rect(screen, (17, 17, 17), (52, 510, 920, 230))
        self.draw_wrapped_text(screen, self.display_text, self.text_font, TEXT_COLOR, self.text_rect)

        pygame.draw.rect(screen, (17, 17, 17), self.next_rect)
        pygame.draw.rect(screen, TEXT_COLOR, self.next_rect, 1)
        arrow = self.button_font.render("▼", True, TEXT_COLOR)
        screen.blit(arrow, arrow.get_rect(center=self.next_rect.center))
        for rect, label, is_active in (
            (self.auto_rect, "AUTO", self.is_auto),
            (self.skip_rect, "SKIP", False),
        ):
            pygame.draw.rect(screen, (80, 80, 80) if is_active else (17, 17, 17), rect)
            pygame.draw.rect(screen, TEXT_COLOR, rect, 1)
            caption = self.button_font.render(label, True, TEXT_COLOR)
            screen.blit(caption, caption.get_rect(center=rect.center))

    def draw_wrapped_text(self, screen, text, font, color, rect):
        lines = []
        for paragraph in text.split("\n"):
            line = ""
            for char in paragraph:
                candidate = line + char
                if line and font.size(candidate)[0] > rect.width:
                    lines.append(line)
                    line = char
                else:
                    line = candidate
            lines.append(line)
        line_height = font.get_linesize() + 5
        y = rect.y
        for line in lines:
            if y + line_height > rect.bottom:
                break
            if line:
                screen.blit(font.render(line, True, color), (rect.x, y))
            y += line_height
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self.advance_line()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.skip_rect.collidepoint(event.pos):
                self.state_manager.change_state(self.NEXT_STATE)
            elif self.auto_rect.collidepoint(event.pos):
                self.is_auto = not self.is_auto
                self.auto_timer = 0.0
            elif self.next_rect.collidepoint(event.pos):
                self.advance_line()

    def advance_line(self):
        if self.is_typing:
            self.display_text = self.text
            self.char_index = len(self.text)
            self.is_typing = False
            self.auto_timer = 0.0
        else:
            self.line_index += 1
            self.show_current_line()

class ExplorationState(State):
    CAMERA_ZOOM = 0.72

    def __init__(self, game, state_manager):
        super().__init__(game, state_manager)
    
    def enter(self):
        self.map_manager = self.game.map_manager
        self.player_manager = self.game.player_manager
        self.enemy_manager = self.game.enemy_manager
        self.item_manager = ItemManager(self.game)
        self.map_history = []
        _, collision_image = self.map_manager.load()
        self.collision_map = CollisionMap(collision_image)
        position = self.find_start_position()
        self.player_manager.set_map(self.collision_map, position)
        collision_maps = {self.map_manager.current_map_name: self.collision_map}
        for map_name in self.map_manager.maps:
            if map_name == self.map_manager.current_map_name:
                continue
            image = self.game.image_manager.image(MapPath.COLLISION, f"{map_name}.png")
            if image is None:
                raise FileNotFoundError(f"当たり判定画像を読み込めません: {map_name}.png")
            collision_maps[map_name] = CollisionMap(image)
        self.item_manager.spawn_items(
            collision_maps,
            self.map_manager.current_map_name,
            self.player_manager.rect,
        )
        self.enemy_manager.enter_map(self.collision_map, self.player_manager.rect)
        self.font = self.game.font_manager.font(FontPath.KOWAI, "ふぉんとうは怖い明朝体.otf", 24)
        camera_size = (
            round(SCREEN_WIDTH / self.CAMERA_ZOOM),
            round(SCREEN_HEIGHT / self.CAMERA_ZOOM),
        )
        self.camera_surface = pygame.Surface(camera_size)
        self.is_dying = False

    def find_start_position(self, preferred_position=None):
        """Find a walkable spawn point, preferring the map's configured start."""
        start = preferred_position or self.map_manager.current_map.start_position
        player = self.player_manager
        rect = pygame.Rect(start[0] + player.COLLISION_OFFSET[0], start[1] + player.COLLISION_OFFSET[1], *player.COLLISION_SIZE)
        if self.collision_map.is_rect_walkable(rect):
            return start
        origin = rect.topleft
        for radius in range(8, 513, 8):
            for delta in range(-radius, radius + 1, 8):
                for x, y in (
                    (origin[0] + delta, origin[1] - radius),
                    (origin[0] + delta, origin[1] + radius),
                    (origin[0] - radius, origin[1] + delta),
                    (origin[0] + radius, origin[1] + delta),
                ):
                    rect.topleft = (x, y)
                    if self.collision_map.is_rect_walkable(rect):
                        return (x - player.COLLISION_OFFSET[0], y - player.COLLISION_OFFSET[1])
        for y in range(0, self.collision_map.height - player.COLLISION_SIZE[1], 16):
            for x in range(player.COLLISION_OFFSET[0], self.collision_map.width - player.COLLISION_SIZE[0], 16):
                rect.topleft = (x, y)
                if self.collision_map.is_rect_walkable(rect):
                    return (x - player.COLLISION_OFFSET[0], y - player.COLLISION_OFFSET[1])
        raise RuntimeError("プレイヤーを配置できる場所がマップにありません")
    
    def exit(self):
        pass

    def update(self, dt):
        if self.is_dying:
            return
        self.player_manager.update(dt)
        self.enemy_manager.update(dt, self.player_manager.rect)
        if self.enemy_manager.enemy and self.player_manager.rect.colliderect(self.enemy_manager.enemy.rect):
            self.is_dying = True
            self.game.audio_manager.play_bgm("心臓の鼓動.mp3")
            return
        self.item_manager.collect(self.player_manager.rect, self.map_manager.current_map_name)
        if self.item_manager.collected_count >= self.item_manager.item_count:
            self.state_manager.change_state(GameState.END)
    
    def draw(self, screen):
        player = self.player_manager
        camera = self.camera_surface
        camera_size = camera.get_size()
        camera.fill(BACKGROUND_COLOR)
        offset = (camera_size[0] // 2 - player.rect.centerx, camera_size[1] // 2 - player.rect.centery)
        self.map_manager.draw(camera, offset)
        self.map_manager.draw_transition_areas(camera, offset)
        self.item_manager.draw(camera, self.map_manager.current_map_name, offset)
        self.enemy_manager.draw(camera, offset)
        player.draw(camera, offset)
        transition = self.map_manager.transition_at(player.rect)
        if transition:
            prompt = self.font.render("！", True, (255, 230, 0))
            prompt_rect = prompt.get_rect(midbottom=(player.image_rect.centerx + offset[0], player.image_rect.top + offset[1] - 4))
            camera.blit(prompt, prompt_rect)
        screen.blit(pygame.transform.scale(camera, screen.get_size()), (0, 0))
        count = self.font.render(f"紙片 {self.item_manager.collected_count}/{self.item_manager.item_count}", True, TEXT_COLOR)
        screen.blit(count, (16, 16))
        if self.map_history:
            return_hint = self.font.render("Backspace: 戻る", True, TEXT_COLOR)
            screen.blit(return_hint, return_hint.get_rect(topright=(screen.get_width() - 16, 16)))
        if self.is_dying:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            message = self.font.render("GAME OVER", True, TEXT_COLOR)
            screen.blit(message, message.get_rect(center=(screen.get_width()//2, screen.get_height()//2)))
    
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_BACKSPACE and self.map_history:
            map_name, position = self.map_history.pop()
            _, collision_image = self.map_manager.load(map_name)
            self.collision_map = CollisionMap(collision_image)
            self.player_manager.set_map(self.collision_map, position)
            self.enemy_manager.enter_map(self.collision_map, self.player_manager.rect)
            return
        if event.key not in (pygame.K_SPACE, pygame.K_RETURN):
            return
        transition = self.map_manager.transition_at(self.player_manager.rect)
        if transition is None:
            return
        current_map = self.map_manager.current_map_name
        current_position = self.player_manager.image_rect.topleft
        if self.map_history and self.map_history[-1][0] == transition["target_map"]:
            _, position = self.map_history.pop()
        else:
            self.map_history.append((current_map, current_position))
            position = transition["spawn_position"]
        self.game.audio_manager.play_se("ドアを開ける2.mp3")
        _, collision_image = self.map_manager.load(transition["target_map"])
        self.collision_map = CollisionMap(collision_image)
        position = self.find_start_position(position)
        self.player_manager.set_map(self.collision_map, position)
        self.enemy_manager.enter_map(self.collision_map, self.player_manager.rect)
        self.game.audio_manager.play_bgm(
            "心臓の鼓動.mp3" if self.enemy_manager.enemy else "死神のリスト.mp3"
        )

class EndState(StoryState):
    STORY_LINES = (
        "最後の紙片を祭壇に重ねた瞬間、赤い光がひとつずつ消えていった。",
        "屋敷を満たしていた重い気配が薄れ、遠くで鎖の落ちる音が響く。",
        "――ガチャン。玄関の扉の鍵が、ようやく外れた。",
        "リリー：「これで……終わったのね。」",
        "扉の外には、夜明け前の冷たい空気が広がっていた。私は振り返らず、屋敷を後にした。",
        "悪魔を呼び出す儀式は封じられた。あの夜の出来事を、私は決して忘れない。",
    )
    BGM = "死神のリスト.mp3"
    NEXT_STATE = GameState.TITLE
