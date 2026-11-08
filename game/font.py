import pygame
from game.path import FontPath

FontKey = tuple[FontPath, str, int]

class FontManager:
    def __init__(self):
        self.fonts: dict[FontKey, pygame.font.Font] = {}

    def font(self, path: FontPath, filename: str, size: int) -> pygame.font.Font:
        key = (path, filename, size)
        if key not in self.fonts:
            target_path = path.value / filename
            try:
                self.fonts[key] = pygame.font.Font(str(target_path), size)
            except (pygame.error, FileNotFoundError) as e:
                print(f"フォント読み込みに失敗: {target_path}, {e}")
                self.fonts[key] = pygame.font.Font(None, size)
        return self.fonts[key]