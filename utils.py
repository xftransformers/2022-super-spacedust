from constants import *
from pgzero.builtins import *
from os import startfile


def handle_screen_bounds(obj: Actor, width: int = ACTIVE_WIDTH, height: int = ACTIVE_HEIGHT):
    """
    Implements the screen bounds behaviour, whereby an object that goes off one side of the screen returns on the other
    :param width: the width of the bounding box.  Defaults to constants.WIDTH
    :type width: int
    :param height: the height of the bounding box.  Defaults to constants.HEIGHT
    :type height: int
    :param obj: the actor to implement the behaviour on
    :type obj: Actor
    :return: None
    :rtype: None
    """
    x, y = obj.pos
    mrx, _ = obj.midright
    mlx, _ = obj.midleft
    _, mty = obj.midtop
    _, mby = obj.midbottom

    if x > width:
        obj.pos = (x - width, y)

    if mrx < 0:
        obj.pos = (x + width, y)

    if y > height:
        obj.pos = (x, y - height)

    if mby < 0:
        obj.pos = (x, y + height)


def is_in_screen_bounds_v(obj: Actor) -> bool:
    _, mty = obj.midtop
    _, mby = obj.midbottom
    return mty >= 0 and mby <= HEIGHT


def is_in_screen_bounds_h(obj: Actor) -> bool:
    mlx, _ = obj.midleft
    mrx, _ = obj.midright
    return mlx >= 0 and mrx <= WIDTH


def run_main():
    startfile("main.py")

