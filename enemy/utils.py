from .enemy_type import EnemyType

ENEMY_DAMAGE_DIST = {
    EnemyType.ASTEROID_LARGE: 8000,
    EnemyType.ASTEROID_MEDIUM: 3500,
    EnemyType.ASTEROID_SMALL: 1700,
    EnemyType.ALIEN: 2000
}


def get_hitbox_distance(enemy_type: EnemyType) -> int:
    try:
        return ENEMY_DAMAGE_DIST[enemy_type]
    except KeyError:
        raise ValueError(f"{enemy_type=}; enemy_type should be a valid enemy_type, but is not")
