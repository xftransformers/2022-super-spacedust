from pgzero.builtins import *
from constants import *
from typing import List, Tuple


class ScreenTraveller(Actor):
    def draw(self):
        super(ScreenTraveller, self).draw()
        x, y = self.pos

        obj_1 = Actor(image=self.image, pos=(x + ACTIVE_WIDTH, y))
        obj_1.angle = self.angle
        obj_1.draw()

        obj_2 = Actor(image=self.image, pos=(x, y + ACTIVE_HEIGHT))
        obj_2.angle = self.angle
        obj_2.draw()

        obj_3 = Actor(image=self.image, angle=self.angle, pos=(x + ACTIVE_WIDTH, y + ACTIVE_HEIGHT))
        obj_3.angle = self.angle
        obj_3.draw()

    def get_pos_of_all_instances(self) -> List[Tuple[int, int]]:
        x, y = self.pos
        return [
            (x, y),
            (x + ACTIVE_WIDTH, y),
            (x, y + ACTIVE_HEIGHT),
            (x + ACTIVE_WIDTH, y + ACTIVE_HEIGHT)
        ]

