from dataclasses import dataclass

import pygame

from game.path import MapPath


@dataclass(frozen=True)
class MapData:
    name: str
    start_position: tuple[int, int]


class MapManager:
    """Loads the view and collision images for the current exploration map."""

    MAP_NAME = "entrance"

    def __init__(self, game):
        self.game = game
        self.maps = {
            name: MapData(name, (220, 344))
            for name in (
                "warehouse", "study_room", "reception_room", "library",
                "kitchen", "hallway_right", "hallway_left", "guest_room",
                "entrance", "dining", "bed_room",
            )
        }
        self.current_map_name = self.MAP_NAME
        self.background = None
        self.collision_image = None
        self.transitions = {
            "reception_room": [
                self._exit("reception_to_hall_left", (1320, 350, 200, 180), "hallway_left", (40, 40)),
            ],
            "hallway_left": [
                self._exit("hall_left_to_reception", (35, 78, 82, 72), "reception_room", (1370, 390)),
                self._exit("hall_left_to_library", (12, 175, 62, 72), "library", (140, 260)),
                self._exit("hall_left_to_study", (12, 355, 62, 78), "study_room", (700, 920)),
                self._exit("hall_left_to_bed", (12, 545, 62, 78), "bed_room", (1120, 500)),
                self._exit("hall_left_to_entrance", (30, 665, 90, 40), "entrance", (35, 190)),
            ],
            "hallway_right": [
                self._exit("hall_right_to_dining", (30, 78, 90, 72), "dining", (1200, 350)),
                self._exit("hall_right_to_kitchen", (82, 175, 62, 72), "kitchen", (1280, 350)),
                self._exit("hall_right_to_guest", (82, 355, 62, 78), "guest_room", (650, 400)),
                self._exit("hall_right_to_warehouse", (82, 545, 62, 78), "warehouse", (700, 900)),
                self._exit("hall_right_to_entrance", (30, 665, 90, 40), "entrance", (340, 190)),
            ],
            "library": [
                self._exit("library_to_hall_left", (100, 230, 260, 160), "hallway_left", (40, 180)),
            ],
            "study_room": [
                self._exit("study_to_hall_left", (650, 900, 220, 124), "hallway_left", (40, 360)),
            ],
            "bed_room": [
                self._exit("bed_to_hall_left", (1040, 480, 290, 150), "hallway_left", (40, 550)),
            ],
            "dining": [
                self._exit("dining_to_hall_right", (1160, 300, 330, 180), "hallway_right", (50, 40)),
            ],
            "kitchen": [
                self._exit("kitchen_to_hall_right", (1220, 350, 300, 180), "hallway_right", (75, 140)),
            ],
            "guest_room": [
                self._exit("guest_to_hall_right", (600, 360, 300, 160), "hallway_right", (75, 320)),
            ],
            "warehouse": [
                self._exit("warehouse_to_hall_right", (640, 890, 260, 130), "hallway_right", (75, 500)),
            ],
            "entrance": [
                self._exit("entrance_to_hall_left", (-20, 400, 100, 140), "hallway_left", (40, 640)),
                self._exit("entrance_to_hall_right", (420, 400, 100, 140), "hallway_right", (40, 640)),
            ],
        }

    @staticmethod
    def _exit(name, area, target_map, spawn_position):
        return {
            "name": name,
            "area": pygame.Rect(area),
            "target_map": target_map,
            "spawn_position": spawn_position,
        }

    @property
    def current_map(self):
        return self.maps[self.current_map_name]

    def load(self, map_name=None):
        if map_name is not None:
            if map_name not in self.maps:
                raise ValueError(f"存在しないマップ: {map_name}")
            self.current_map_name = map_name
        name = self.current_map_name
        self.background = self.game.image_manager.image(MapPath.VIEW, f"{name}.png")
        self.collision_image = self.game.image_manager.image(MapPath.COLLISION, f"{name}.png")
        if self.background is None or self.collision_image is None:
            raise FileNotFoundError(f"マップ画像を読み込めません: {name}")
        return self.background, self.collision_image

    def transition_at(self, player_rect):
        for transition in self.transitions.get(self.current_map_name, ()):
            if player_rect.colliderect(transition["area"]):
                return transition
        return None

    def draw_transition_areas(self, screen, offset=(0, 0)):
        """Show the active map's interaction zones as translucent white boxes."""
        for transition in self.transitions.get(self.current_map_name, ()):
            rect = transition["area"].move(offset)
            overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 32))
            screen.blit(overlay, rect.topleft)

    def draw(self, screen, offset=(0, 0)):
        if self.background is not None:
            screen.blit(self.background, offset)
