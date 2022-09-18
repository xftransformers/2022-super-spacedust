"""
    Marcus R.  Super Spacedust
    Copyright (C) 2022 Marcus R.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    If you want a copy of this source code: https://github.com/xftransformers
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Assets and some code based on resources from Wireframe magazine.
    https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode
"""

import pgzrun
from pgzero.builtins import *
from math import sin, cos, radians, sqrt, atan
from typing import List, Union
from enemy import Enemy, Asteroid, Alien
from constants import *
from ship import Ship
from bullet import Bullet
from utils import handle_screen_bounds
from time import time
from spawner import get_spawn_list, setup_ledger
from random import randint, randrange
from pygame import Surface

ship = Ship()
curr_frame = 0
game_state = GAME_ACTIVE
enemies: List[Enemy] = []
bullets: List[Bullet] = []
curr_round: int = 0
curr_score: int = 0


def draw():

    screen.blit(BACKGROUND, (0, 0))
    for bullet in bullets:
        bullet.draw()

    draw_enemies()
    if (game_state in (GAME_ACTIVE, GAME_ROUND_INTERIM)) or curr_frame % 2 == 0:
        ship.draw()

    if game_state == GAME_WIN:
        screen.draw.text("ALL ENEMIES CLEAR", center=(400, 300), owidth=0.5, ocolor=(255, 255, 0), color=(255, 0, 0),
                         fontsize=50)
        return

    if game_state in GAME_LOSS_STATES:
        screen.draw.text("Click to restart", midbottom=(400, 600), color=WHITE, fontsize=40)
        if game_state == GAME_LOSS_COLLISION:
            screen.draw.text("YOU DIED", center=(400, 300), owidth=0.5, ocolor=(125, 0, 0), color=(255, 0, 0),
                             fontsize=50)

        if game_state == GAME_LOSS_SPEED:
            screen.draw.text("YOUR ROCKET EXPLODED DUE TO YOUR SPEED", center=(400, 300), owidth=0.5, ocolor=(125, 0, 0),
                             color=(255, 0, 0), fontsize=40)
        return

    if game_state == GAME_ROUND_INTERIM:
        screen.draw.text(f"WAVE {str(curr_round)} COMPLETE.  NEXT ROUND STARTING SOON...", center=(400, 300),
                         owidth=0.1, ocolor=(0, 0, 0), color=(128, 128, 0), fontsize=40)
        return

    remaining_enemies = len(enemies)
    screen.draw.text(f"{remaining_enemies} ENEM{'IES' if enemies != 1 else 'Y'} REMAINING", midtop=(400, 0),
                     fontsize=UI_INFO_FONT_SIZE, color=WHITE)
    screen.draw.text(f"WAVE {str(curr_round)}", topright=(800, 0), fontsize=UI_INFO_FONT_SIZE, color=WHITE)
    screen.draw.text(f"VEL: {round(ship.vel_linear, 2)}px/s"
                     f"{' - RAMMING SPEED' if ship.vel_linear >= SHIP_RAM_SPEED else ''}", bottomleft=(0, 600),
                     fontsize=UI_INFO_FONT_SIZE, color=WHITE)
    screen.draw.text(ship.get_shield_status_text(), bottomright=(800, 600), fontsize=UI_INFO_FONT_SIZE, color=WHITE)

    screen.draw.text(f"SCORE {str(curr_score)}", topleft=(0, 0), fontsize=UI_INFO_FONT_SIZE, color=WHITE)


def update(td):
    global curr_frame, game_state
    curr_frame += 1

    if td > 0.17:
        print(f"PERFORMANCE WARNING: {td=}")

    if game_state not in GAME_LOSS_STATES:
        ship.update(td)
        handle_screen_bounds(ship)

        if game_state == GAME_ACTIVE:
            update_bullets()
            update_enemies()
            check_ship_collision()

            if ship.vel_linear >= SHIP_MAX_SPEED:
                game_state = GAME_LOSS_SPEED


def on_key_down(key):
    if game_state == GAME_ACTIVE:
        if key.name == "SPACE":
            make_bullet()

        if key.name == "LSHIFT":
            ship.toggle_shield_input()

        ship.brake_active = key.name == "LCTRL"

        if key.name == "R":
            start_round_1()


def on_mouse_down():
    if game_state == GAME_ACTIVE and not ship.shield_active:
        make_bullet()
        return

    if game_state in GAME_LOSS_STATES:
        start_round_1()
        return


def spawn_enemies(list_to_spawn: list):
    for i, enemy_type in enumerate(list_to_spawn):
        dist = 0
        speed = randrange(ENEMY_MIN_SPEED * 10, ENEMY_MAX_SPEED * 10) / 10
        new_enemy_pos = (0, 0)
        while dist <= enemy_type.HITBOX_SIZE * 5:
            new_enemy_pos = (randint(SPAWN_AREA_BORDER_BUFFER, WIDTH - SPAWN_AREA_BORDER_BUFFER),
                             randint(SPAWN_AREA_BORDER_BUFFER, HEIGHT - SPAWN_AREA_BORDER_BUFFER))
            shipx, shipy = ship.pos
            enx, eny = new_enemy_pos
            dx, dy = shipx - enx, shipy - eny
            dist = dx * dx + dy * dy

        if issubclass(enemy_type, Asteroid):
            new_enemy = enemy_type(center=new_enemy_pos, angle_of_velocity=80 * i + 20, speed=speed)
        elif issubclass(enemy_type, Alien):
            new_enemy = enemy_type(center=new_enemy_pos, speed=speed)
        else:
            raise ValueError(f"{enemy_type=}; enemy is not a valid (spawnable) enemy (must be Alien or Asteroid)")

        enemies.append(new_enemy)


def update_bullets():
    global bullets
    bullets_temp: List[Bullet] = []

    for bullet in bullets:
        if not hit_enemy(bullet) and bullet.is_alive:
            updated_bullet = Bullet(start_time=bullet.start_time, speed=bullet.speed)
            updated_bullet.x = bullet.x + bullet.speed * sin(radians(bullet.angle))
            updated_bullet.y = bullet.y + bullet.speed * cos(radians(bullet.angle))
            updated_bullet.angle = bullet.angle

            handle_screen_bounds(updated_bullet)

            bullets_temp.append(updated_bullet)

    bullets = bullets_temp


def update_enemies():
    global game_state

    if len(enemies) == 0:
        start_next_round()

    for enemy in enemies:
        enemy.update(curr_frame, ship)


def is_on_screen(obj: Actor) -> bool:
    return 0 < obj.x < WIDTH and 0 < obj.y < HEIGHT


def break_enemy(enemy) -> List[Union[Enemy, None]]:
    global curr_score

    curr_score += enemy.SCORE

    # Asteroid is completely destroyed
    return enemy.handle_break()


def hit_enemy(bullet: Actor) -> bool:
    global enemies

    bullet_has_hit = False
    new_enemies: List[Enemy] = []

    for enemy in enemies:
        if enemy.collidepoint(bullet.pos) and not bullet_has_hit:
            new_enemies += break_enemy(enemy)
            bullet_has_hit = True
        else:
            new_enemies.append(enemy)

    enemies = new_enemies

    return bullet_has_hit


def draw_enemies() -> None:
    for enemy in enemies:
        enemy.draw()


def make_bullet() -> None:
    global curr_score

    new_bullet = Bullet(start_time=time(), center=ship.pos, speed=ship.vel_linear + 5)
    new_bullet.angle = (ship.angle + 180) % 360
    bullets.append(new_bullet)

    curr_score = max(0, curr_score - 1)


def check_ship_collision() -> None:
    """
    Checks if there was a colllsion between the player's ship and any enemy
    :return: None
    :rtype: None
    """
    global game_state
    for i, enemy in enumerate(enemies):
        shipx, shipy = ship.pos
        astx, asty = enemy.pos

        # difference in x and y between enemy and spaceship
        dx, dy = abs(shipx - astx), abs(shipy - asty)
        dist = dx * dx + dy * dy

        if dist <= enemy.HITBOX_SIZE:
            velx, vely = ship.vel
            ship_vel_2d = sqrt(velx * velx + vely * vely)

            if ship_vel_2d >= SHIP_RAM_SPEED and enemy.RAMMABLE:
                break_enemy(enemy)
                enemies.pop(i)
                return

            # If the enemy is not rammable, the code will continue through the function and behave as if the
            # player simply hit the enemy

            if not ship.shield_active:
                game_state = GAME_LOSS_COLLISION

                if DEBUG:
                    try:
                        enemy.image = f"ast{enemy.size}_hit"
                    except Exception as e:
                        print(f"{e.with_traceback()}")
                    finally:
                        print(f"{ship_vel_2d=}")


def start_next_round() -> None:
    """
    Function that enters the round interim state, and schedules the start of the next round
    :return: None
    :rtype: None
    """
    global curr_round, game_state, bullets

    bullets = []

    game_state = GAME_ROUND_INTERIM
    clock.schedule(start_next_round_callback, ROUND_INTERIM_LENGTH)


def start_next_round_callback() -> None:
    """
    Callback function that spawns in the next round of enemy, and increments the curr_round variable.
    :return: None
    :rtype: None
    """
    global game_state, curr_round

    curr_round += 1
    enemies_to_spawn = get_spawn_list(curr_round)
    spawn_enemies(enemies_to_spawn)
    game_state = GAME_ACTIVE


def start_round_1() -> None:
    global curr_round, curr_score, enemies, bullets, curr_frame, ship

    enemies = []
    bullets = []
    curr_score = 0

    if not DEBUG:
        curr_round = 0

    curr_frame = 0
    ship = Ship()

    start_next_round_callback()


setup_ledger()
start_round_1()
pgzrun.go()
