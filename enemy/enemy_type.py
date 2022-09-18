from enum import Enum, auto


class EnemyType(Enum):
    ASTEROID_LARGE = auto()
    ASTEROID_MEDIUM = auto()
    ASTEROID_SMALL = auto()
    ALIEN = auto()