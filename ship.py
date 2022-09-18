from pgzero.builtins import *
from constants import *
from math import sqrt, sin, cos, radians
from time import time
from screen_traveller import ScreenTraveller


class Ship(ScreenTraveller):
    def __init__(self):
        ship_image = f"{SHIP_IMAGE}{'_bounding' if DEBUG else ''}"
        super(Ship, self).__init__(ship_image, center=(WIDTH // 2, HEIGHT // 2))
        self.angle = 0
        self._vel = (0, 0)
        self._shield_active = False
        self._shield_charge = 0
        self._shield_start_time = 0
        self._brake_active = False

    def handle_input(self):
        if keyboard.a:
            self.angle += 2

        if keyboard.d:
            self.angle -= 2

        velx, vely = self._vel

        change_in_vel = 0
        if keyboard.w:
            change_in_vel = SHIP_ACC

        if keyboard.s:
            change_in_vel = -SHIP_ACC

        if change_in_vel == 0:
            if round(velx, 2) != 0 or round(vely, 2) != 0:
                # if no input is detected, than decelerate slightly
                self.change_vel_by_multiplier(SHIP_DECELERATION_MULTIPLIER)
        else:
            velx += -sin(radians(self.angle)) * change_in_vel
            vely += -cos(radians(self.angle)) * change_in_vel

            self._vel = (velx, vely)

    def move(self):
        """
        Function that moves the ship by the already stored velocity
        :return: None
        :rtype: None
        """

        velx, vely = self._vel

        self.x += velx
        self.y += vely

    def update(self, td: float):
        """
        Function called every frame that updates the ship object based on input, and moves the ship accordingly
        :param td: the time delta between frames.
        :type td: float
        :return: None
        """

        if self._brake_active:
            self.change_vel_by_multiplier(SHIP_BRAKE_DECELERATION * td)

        self.handle_input()
        self.move()

        if not self._shield_active:
            self._shield_charge = min(2 * SHIP_SHIELD_REQ_CHARGE, self._shield_charge + self.vel_linear * td)

    @property
    def vel_linear(self):
        velx, vely = self._vel
        return sqrt(velx * velx + vely * vely)

    def toggle_shield_input(self):
        """
        Function called when the user order the shield status to change.  Ensures the input can be completed
        before executing
        :return:
        :rtype:
        """
        if self._shield_charge >= SHIP_SHIELD_REQ_CHARGE:
            self._shield_charge -= SHIP_SHIELD_REQ_CHARGE
            self.shield_active = not self.shield_active

    def disable_shield(self):
        self.shield_active = False

    @property
    def shield_active(self) -> bool:
        return self._shield_active

    @shield_active.setter
    def shield_active(self, value: bool):
        self._shield_active = value
        angle = self.angle
        self.image = f"ship{'_shield' if self._shield_active else ''}"
        self.angle = angle

        if self._shield_active:
            clock.schedule_unique(self.disable_shield, SHIP_SHIELD_ACTIVE_TIME)
            self._shield_start_time = time()
            self._vel = (0, 0)

    def get_shield_status_text(self) -> str:
        if self.shield_active:
            return f"SHIELD ACTIVE - {round(5 - time() + self._shield_start_time)}s REMAINING"

        return f"SHIELD CHARGING - {round(100 * self._shield_charge / SHIP_SHIELD_REQ_CHARGE, 1)}%"

    @property
    def vel(self):
        return self._vel

    def change_vel_by_multiplier(self, multiplier: (int, float)):
        """
        Changes the velocity tuple of a Ship by multiplying it by the multiplier
        :arg multiplier: the amount to multiply the decimal by
        :type multiplier: float
        :return: None
        :rtype: None
        """
        x, y = self._vel
        x *= multiplier
        y *= multiplier
        self._vel = (x, y)

    @property
    def brake_active(self) -> bool:
        return self._brake_active

    @brake_active.setter
    def brake_active(self, value: bool):
        self._brake_active = value

