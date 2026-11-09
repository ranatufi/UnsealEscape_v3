import math

import pygame

from game.constant import PLAYER_SPEED
from game.path import CharacterPath


class PlayerManager:
    SIZE = (48, 64)
    COLLISION_SIZE = (24, 20)
    COLLISION_OFFSET = (12, 40)

    def __init__(self, game):
        self.game = game
        self.direction = "down"
        self.frames = {}
        self.frame = 0
        self.timer = 0.0
        self.image_rect = pygame.Rect(0, 0, *self.SIZE)
        self.rect = pygame.Rect(0, 0, *self.COLLISION_SIZE)
        self.collision_map = None
        for direction in ("up", "down", "left", "right"):
            self.frames[direction] = [
                game.image_manager.image(CharacterPath.RIRI, f"{direction}/{index}.png", self.SIZE)
                for index in range(4)
            ]

    def set_map(self, collision_map, position):
        self.collision_map = collision_map
        self.image_rect.topleft = position
        self.rect.topleft = (position[0] + self.COLLISION_OFFSET[0], position[1] + self.COLLISION_OFFSET[1])

    def move(self, dx, dy, dt):
        if not dx and not dy:
            return False
        length = math.hypot(dx, dy)
        dx, dy = dx / length, dy / length
        moving = False
        for axis, delta in (("x", round(dx * PLAYER_SPEED * dt)), ("y", round(dy * PLAYER_SPEED * dt))):
            if delta:
                candidate = self.rect.move(delta, 0) if axis == "x" else self.rect.move(0, delta)
                if self.collision_map and self.collision_map.is_rect_walkable(candidate):
                    setattr(self.rect, axis, getattr(candidate, axis))
                    moving = True
        self.image_rect.topleft = (self.rect.x - self.COLLISION_OFFSET[0], self.rect.y - self.COLLISION_OFFSET[1])
        return moving

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        if dy < 0: self.direction = "up"
        elif dy > 0: self.direction = "down"
        elif dx < 0: self.direction = "left"
        elif dx > 0: self.direction = "right"
        moving = self.move(dx, dy, dt)
        if not moving:
            self.frame, self.timer = 0, 0.0
        else:
            self.timer += dt
            if self.timer >= 0.15:
                self.timer -= 0.15
                self.frame = (self.frame + 1) % 4

    def draw(self, screen, offset=(0, 0)):
        screen.blit(self.frames[self.direction][self.frame], self.image_rect.move(offset))
