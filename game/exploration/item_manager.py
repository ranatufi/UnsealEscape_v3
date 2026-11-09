import random

import pygame

from game.path import ImagePath


class ItemManager:
    def __init__(self, game, item_count=5, item_size=24):
        self.game = game
        self.item_count = item_count
        self.item_size = item_size
        self.items = []
        self.collected_count = 0
        self.image = game.image_manager.image(ImagePath.MATERIAL, "paper.png", (item_size, item_size))

    def spawn_items(self, collision_maps, current_map_name, player_rect):
        """Place the total item supply across distinct walkable maps."""
        self.items.clear()
        map_names = [
            name for name in collision_maps
            if not name.startswith("hallway") and name != "entrance"
        ]
        if not map_names:
            raise ValueError("紙片を配置できるマップがありません")
        destinations = random.sample(map_names, min(self.item_count, len(map_names)))
        used_maps = set()
        for item_index in range(self.item_count):
            preferred = destinations[item_index % len(destinations)]
            candidates = [preferred] + [name for name in map_names if name != preferred]
            candidates = [name for name in candidates if name not in used_maps]
            placed = False
            for map_name in candidates:
                collision_map = collision_maps[map_name]
                for _ in range(3000):
                    x = random.randint(0, max(0, collision_map.width - self.item_size))
                    y = random.randint(0, max(0, collision_map.height - self.item_size))
                    rect = pygame.Rect(x, y, self.item_size, self.item_size)
                    if not collision_map.is_rect_walkable(rect):
                        continue
                    if map_name == current_map_name and rect.colliderect(player_rect):
                        continue
                    if any(item["map_name"] == map_name and item["rect"].colliderect(rect) for item in self.items):
                        continue
                    self.items.append({"map_name": map_name, "rect": rect})
                    used_maps.add(map_name)
                    placed = True
                    break
                if placed:
                    break
            if not placed:
                self.items.clear()
                raise RuntimeError("紙片を配置できませんでした。通行可能領域を確認してください。")

    def collect(self, player_rect, current_map_name):
        remaining = []
        for item in self.items:
            if item["map_name"] == current_map_name and item["rect"].colliderect(player_rect):
                self.collected_count += 1
            else:
                remaining.append(item)
        self.items = remaining

    def draw(self, screen, current_map_name, offset=(0, 0)):
        if self.image:
            for item in self.items:
                if item["map_name"] == current_map_name:
                    screen.blit(self.image, item["rect"].move(offset))
