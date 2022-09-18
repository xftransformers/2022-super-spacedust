

from pgzero.builtins import *
from typing import Tuple, List
from math import sin, cos, radians
from utils import handle_screen_bounds
from constants import *
from screen_traveller import ScreenTraveller
from .enemy import Enemy
from .enemy_type import EnemyType
from .utils import get_hitbox_distance


SCORES = {
            EnemyType.ASTEROID_LARGE: 2,
            EnemyType.ASTEROID_MEDIUM: 5,
            EnemyType.ASTEROID_SMALL: 15
        }

IMG_INDEX = {
    EnemyType.ASTEROID_LARGE: 1,
    EnemyType.ASTEROID_MEDIUM: 2,
    EnemyType.ASTEROID_SMALL: 3
}


class Asteroid(Enemy):

    def __init__(self, _img: str = "", img_frame: (int, str) = 1, type_: EnemyType = EnemyType.ASTEROID_LARGE,
                 angle_of_velocity: float = 0, speed: (int, float) = ENEMY_DEFAULT_SPEED, **kw):
        super(Asteroid, self).__init__(type_, _img or f"ast{IMG_INDEX[type_]}_{str(img_frame)}", **kw)
        self._orientation = angle_of_velocity
        self._speed = speed
        self._type = type_

    def __str__(self):
        return f"Asteroid of angle {self.angle_of_velocity}"

    def handle_break(self) -> List[Enemy]:
        """
        Function called when an asteroid is broken.
        :return: Any new asterios
        :rtype: list
        """

        if self.SPLIT_RETURN_TYPE:
            new_asteroid_1 = self.SPLIT_RETURN_TYPE(center=self.pos, angle_of_velocity=(self._orientation + 90) % 360,
                                                    speed=self.speed)
            new_asteroid_2 = self.SPLIT_RETURN_TYPE(center=self.pos, angle_of_velocity=(self._orientation - 90) % 360,
                                                    speed=self.speed)

            return [new_asteroid_1, new_asteroid_2]
        return []

    @property
    def angle_of_velocity(self):
        return self._orientation

    @angle_of_velocity.setter
    def angle_of_velocity(self, value: float):
        self._orientation = value % 360

    @property
    def type(self):
        return self._type


class SmallAsteroid(Asteroid):
    HITBOX_SIZE = 1700
    SCORE = SCORES[EnemyType.ASTEROID_SMALL]
    IMAGES = [f"ast3_{n}" for n in range(1, 13)]

    def __init__(self, angle_of_velocity: int = 0, speed: int = ENEMY_DEFAULT_SPEED, **kw):
        super(SmallAsteroid, self).__init__(type_=EnemyType.ASTEROID_SMALL, _img="ast3_1", angle_of_velocity=angle_of_velocity,
                                            speed=speed, **kw)

class MediumAsteroid(Asteroid):
    HITBOX_SIZE = 3500
    SCORE = SCORES[EnemyType.ASTEROID_MEDIUM]
    SPLIT_RETURN_TYPE = SmallAsteroid
    IMAGES = [f"ast2_{n}" for n in range(1, 13)]

    def __init__(self, angle_of_velocity: int = 0, speed: int = ENEMY_DEFAULT_SPEED, **kw):
        super(MediumAsteroid, self).__init__(type_=EnemyType.ASTEROID_MEDIUM, _img="ast2_1", angle_of_velocity=angle_of_velocity,
                                             speed=speed, **kw)


class LargeAsteroid(Asteroid):
    HITBOX_SIZE = 8000
    SCORE = SCORES[EnemyType.ASTEROID_LARGE]
    SPLIT_RETURN_TYPE = MediumAsteroid
    IMAGES = [f"ast1_{n}" for n in range(1, 13)]

    def __init__(self, angle_of_velocity: int = 0, speed: int = ENEMY_DEFAULT_SPEED, **kw):
        super(LargeAsteroid, self).__init__(type_=EnemyType.ASTEROID_LARGE, _img="ast1_1", angle_of_velocity=angle_of_velocity,
                                            speed=speed, **kw)




