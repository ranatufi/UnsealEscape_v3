import math
import random

from game.exploration.enemy import Enemy


class EnemyManager:
    def __init__(self, game, spawn_probability=0.35, min_spawn_distance=160):
        self.game = game
        self.spawn_probability = spawn_probability
        self.min_spawn_distance = min_spawn_distance
        self.enemy = None

    def enter_map(self, collision_map, player_rect):
        self.enemy = None
        if random.random() >= self.spawn_probability:
            return
        width, height = Enemy.SIZE
        for _ in range(2000):
            x = random.randint(0, max(0, collision_map.width - width))
            y = random.randint(0, max(0, collision_map.height - height))
            rect = player_rect.copy()
            rect.size, rect.topleft = Enemy.SIZE, (x, y)
            if collision_map.is_rect_walkable(rect) and math.hypot(rect.centerx-player_rect.centerx, rect.centery-player_rect.centery) >= self.min_spawn_distance:
                self.enemy = Enemy(self.game, collision_map, (x, y))
                return

    def update(self, dt, player_rect):
        if self.enemy:
            self.enemy.update(dt, player_rect)

    def draw(self, screen, offset=(0, 0)):
        if self.enemy:
            self.enemy.draw(screen, offset)
