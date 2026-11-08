import pygame
from enum import Enum

ImageKey = tuple[Enum, str]
ScaledKey = tuple[ImageKey, tuple[int, int]]

class ImageManager:
    def __init__(self):
        self.images: dict[ImageKey, pygame.Surface | None] = {}
        self.scaled_images: dict[ScaledKey, pygame.Surface | None] = {}
    
    def image(self, path: Enum, filename: str, size: tuple[int, int] | None = None) -> pygame.Surface | None:
        image_key = (path, filename)
        if image_key not in self.images:
            target_path = path.value / filename
            try:
                image = pygame.image.load(target_path).convert_alpha()
            except pygame.error as e:
                print(f"画像読み込みに失敗: {target_path}, {e}")
                image = None
            self.images[image_key] = image

        original_image = self.images[image_key]
        if original_image is None or size is None or original_image.get_size() == size:
            return original_image

        scaled_key = (image_key, size)
        if scaled_key not in self.scaled_images:
            try:
                self.scaled_images[scaled_key] = pygame.transform.smoothscale(original_image, size)
            except pygame.error as e:
                print(f"画像のスケーリングに失敗: {image_key}, {e}")
                self.scaled_images[scaled_key] = None
        return self.scaled_images[scaled_key]