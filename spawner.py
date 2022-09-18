from constants import *
from enemy import LargeAsteroid, Alien, Enemy, LargeRamProofAsteroid
from random import choice
from utils import run_main
from typing import List

spawner_ledger = []
GUARANTEED_SPAWNS = {
    2: [LargeRamProofAsteroid, Alien]
}


def setup_ledger():
    global spawner_ledger
    spawner_ledger += [LargeRamProofAsteroid]
    spawner_ledger += 3 * [LargeAsteroid]
    spawner_ledger += 4 * [Alien]

    if DEBUG:
        print(f"{spawner_ledger=}")


def get_next_spawn(curr_round: int, curr_round_spawner_ledger=spawner_ledger) -> Enemy:
    spawnable = choice(curr_round_spawner_ledger)
    return spawnable


def get_spawn_list(curr_round) -> List[Enemy]:
    spawn_list: List[Enemy] = []
    req_spawnables_count = ROUND_1_ASTEROIDS - 1 + curr_round
    curr_round_spawn_ledger = [n for n in spawner_ledger if n.MIN_WAVE_SPAWN <= curr_round]

    try:
        req_spawnables = GUARANTEED_SPAWNS[curr_round]
        spawn_list += req_spawnables
    except KeyError:
        if DEBUG:
            print(f"No req. spawns for wave {curr_round}")

    spawn_list += [get_next_spawn(curr_round, curr_round_spawn_ledger) for n in
                   (range(req_spawnables_count - len(spawn_list)))]

    if DEBUG:
        print(f"{spawn_list=}")

    return spawn_list


if __name__ == '__main__':
    DEBUG = True  # prints all req. info
    setup_ledger()

    curr_round_ = 1

    while (cmd := input("> ")) is not None or cmd != "":
        print(f"ROUND {str(curr_round_)}")
        get_spawn_list(curr_round_)
        curr_round_ += 1

