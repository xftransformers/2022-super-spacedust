from .enemy import Enemy
from .enemy_type import EnemyType
from .utils import get_hitbox_distance
from constants import *
from utils import handle_screen_bounds
from math import cos, sin, radians
from ship import Ship


class Alien(Enemy):
    IMAGES = ["alien0", "alien1"]
    SCORE = 25
    HITBOX_SIZE = 2000
    MIN_WAVE_SPAWN = 2

    def __init__(self, angle_of_velocity: int = 0, speed: int = 0, ship: Ship = None, **kwargs):
        super(Alien, self).__init__(type_=EnemyType.ALIEN, _img="alien0", angle_of_velocity=angle_of_velocity,
                                    **kwargs)
        self.hitbox_size = get_hitbox_distance(EnemyType.ALIEN)
        self._speed = speed

    def update(self, curr_frame: int, ship: Ship):
        self.angle_of_velocity = self.angle_to(ship)
        super(Alien, self).update(curr_frame, ship)

