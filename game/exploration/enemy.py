import math

import pygame

from game.path import CharacterPath


class Enemy:
    SIZE = (48, 64)
    SPEED = 100

    def __init__(self, game, collision_map, position):
        self.game = game
        self.collision_map = collision_map
        self.rect = pygame.Rect(*position, *self.SIZE)
        self.direction = "down"
        self.animation = {}
        self.frame = 0
        self.timer = 0.0
        for direction in ("up", "down", "left", "right"):
            folder = CharacterPath.TEKI.value / direction
            paths = sorted(
                folder.glob("*.png"),
                key=lambda path: (0, int(path.stem)) if path.stem.isdigit() else (1, path.stem),
            )
            if not paths:
                raise FileNotFoundError(f"敵の歩行画像がありません: {folder}")
            self.animation[direction] = [
                game.image_manager.image(CharacterPath.TEKI, f"{direction}/{path.name}", self.SIZE)
                for path in paths
            ]
        self.image = self.animation[self.direction][0]

    def update(self, dt, target_rect):
        dx = target_rect.centerx - self.rect.centerx
        dy = target_rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance < 1:
            return
        dx, dy = dx / distance, dy / distance
        direction = ("right" if dx > 0 else "left") if abs(dx) > abs(dy) else ("down" if dy > 0 else "up")
        if direction != self.direction:
            self.direction, self.frame, self.timer = direction, 0, 0.0
        for axis, delta in (("x", round(dx * self.SPEED * dt)), ("y", round(dy * self.SPEED * dt))):
            if delta:
                candidate = self.rect.move(delta, 0) if axis == "x" else self.rect.move(0, delta)
                if self.collision_map.is_rect_walkable(candidate):
                    setattr(self.rect, axis, getattr(candidate, axis))
        frames = self.animation[self.direction]
        self.timer += dt
        while self.timer >= 0.15:
            self.timer -= 0.15
            self.frame = (self.frame + 1) % len(frames)
        self.image = frames[self.frame]

    def draw(self, screen, offset=(0, 0)):
        screen.blit(self.image, self.rect.move(offset))
