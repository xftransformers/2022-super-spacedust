from .asteroid import Asteroid
from pgzero.builtins import *
from constants import *
from typing import Tuple
from .asteroid import LargeAsteroid, SmallAsteroid, MediumAsteroid


class RamProofAsteroid(Asteroid):
    RAMMABLE = False
    MIN_WAVE_SPAWN = 2

    def __init__(self, type: int = EnemyType.ASTEROID_LARGE, **kw):
        super(RamProofAsteroid, self).__init__(_img=f"ast{type}_ramproof", type=type, **kw)

    def update_image(self, curr_frame) -> None:
        return  # The image of a RPA is fixed

    def make_copy_of_self(self, size, angle_of_velocity, _):
        # The _ is img_frame in Asteroid, but that is not needed here
        return RamProofAsteroid(center=self.center, type=size, angle_of_velocity=angle_of_velocity,
                                speed=self.speed)

    def __str__(self):
        return f"Ram-Proof Asteroid of angle {self.angle_of_velocity}"


class SmallRamProofAsteroid(SmallAsteroid):
    RAMMABLE = False
    IMAGES = ["ast3_ramproof"]

    def __init__(self, angle_of_velocity: int = 0, speed: int = ENEMY_DEFAULT_SPEED, **kw):
        super(SmallRamProofAsteroid, self).__init__(angle_of_velocity=angle_of_velocity, speed=speed, **kw)


class MediumRamProofAsteroid(MediumAsteroid):
    RAMMABLE = False
    SPLIT_RETURN_TYPE = SmallRamProofAsteroid
    IMAGES = ["ast2_ramproof"]

    def __init__(self, angle_of_velocity: int = 0, speed: int = ENEMY_DEFAULT_SPEED, **kw):
        super(MediumRamProofAsteroid, self).__init__(angle_of_velocity=angle_of_velocity, speed=speed, **kw)
        self.image = "ast2_ramproof"


class LargeRamProofAsteroid(LargeAsteroid):
    RAMMABLE = False
    SPLIT_RETURN_TYPE = MediumRamProofAsteroid
    IMAGES = ["ast1_ramproof"]

    def __init__(self, angle_of_velocity: int = 0, speed: int = ENEMY_DEFAULT_SPEED, **kw):
        super(LargeRamProofAsteroid, self).__init__(angle_of_velocity=angle_of_velocity, speed=speed, **kw)





