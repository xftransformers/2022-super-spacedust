from pgzero.builtins import *
from constants import *
from time import time
from screen_traveller import ScreenTraveller


class Bullet(ScreenTraveller):
    """
    Wrapper class of a bullet.  A bullet class is destroyed and instantiated each frame.
    """
    def __init__(self, start_time, speed, **kw):
        """
        Initializes the class
        """
        super(Bullet, self).__init__("bullet", **kw)
        self._start_time = start_time
        self._speed = speed

    @property
    def is_alive(self) -> bool:
        """
        Returns True if the bullet has not eclipsed its time to live.  Else, it returns False
        :return: Whether the bullet has not eclipsed its time to live.
        :rtype: bool
        """
        return time() - self.start_time <= BULLET_TIME_TO_LIVE

    @property
    def start_time(self):
        return self._start_time

    @property
    def speed(self):
        return self._speed



