from __future__ import annotations

from pgzero.builtins import *
from typing import Tuple, List
from math import sin, cos, radians
from utils import handle_screen_bounds
from constants import *
from screen_traveller import ScreenTraveller
from ship import Ship

ENEMY_DAMAGE_DIST = {
    EnemyType.ASTEROID_LARGE: 8000,
    EnemyType.ASTEROID_MEDIUM: 3500,
    EnemyType.ASTEROID_SMALL: 1700,
    EnemyType.ALIEN: 2000
}


class Enemy(ScreenTraveller):
    RAMMABLE = True
    MIN_WAVE_SPAWN = 1
    IMAGES = []
    SPLIT_RETURN_TYPE = None

    def __init__(self, type_: EnemyType,_img: str, center: Tuple[float, float] = (0, 0), speed: (int, float) = 5,
                 score: int = 0, angle_of_velocity: int = 0):
        super(Enemy, self).__init__(_img, center)
        self._score = score
        self._type = type_
        self.hitbox_size = -1  # Implemented in subclasses
        self.curr_image_index = 0
        self.angle_of_velocity = angle_of_velocity

    def __str__(self):
        return f"Enemy of angle {self.angle_of_velocity}"

    @property
    def speed(self):
        return self._speed

    @property
    def score(self):
        return self._score

    def handle_break(self) -> List[Enemy]:
        return []  # Implemented in subclasses

    def get_score(self) -> int:
        pass  # Implemented in subclasses

    def update(self, curr_frame: int, ship: Ship):
        self.update_image(curr_frame)

        angle = self.angle_of_velocity
        self.x += self._speed * sin(radians(angle))
        self.y += self._speed * cos(radians(angle))

        handle_screen_bounds(self)
        self.angle_of_velocity = angle

    def update_image(self, curr_frame: int):
        if curr_frame % 5 == 0:  # Every 5 frames, change the asteroid image
            self.curr_image_index += 1

        if self.curr_image_index >= len(self.IMAGES):
            self.curr_image_index = 0

        self.image = self.IMAGES[self.curr_image_index]






