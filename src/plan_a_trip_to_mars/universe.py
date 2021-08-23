"""This script implements classes for objects that can move in a 2D space.
"""

import bisect
from abc import ABC, abstractmethod
from typing import Union

import plan_a_trip_to_mars.misc.precode2 as pre

# Gravitational constant
G = 6.6743e-11


class Base(ABC):
    """Abstract baseclass for every stationary object to inherit from."""

    def __init__(
        self,
        name: str,
        mass: float,
        pos: pre.Vector2D = pre.Vector2D(0, 0),
        vel: pre.Vector2D = pre.Vector2D(0, 0),
        acc: pre.Vector2D = pre.Vector2D(0, 0),
    ) -> None:
        """Initialise the object with a starting position and velocity.

        Args:
            name: str
                Name the object
            mass: float
                Give the object some mass

        Keyword args:
            pos: pre.Vector2D
                The position vector of the object with respect to origo (0, 0)
            vel: pre.Vector2D
                The velocity vector of the object
            acc: pre.Vector2D
                The acceleration vector of the object
        """
        self.spi: int = 1
        self.name = name
        self.mass = mass
        self.trace = []
        self.pos_init = pos
        self.vel_init = vel
        self.acc_init = acc
        self.reset_movement()

    def reset_movement(self) -> None:
        self.pos = self.pos_init
        self.vel = self.vel_init * self.spi
        self.acc = self.acc_init * self.spi ** 2

    def move(self):
        self.trace.append(self.pos.as_point)
        self.vel += self.acc * self.spi ** 2
        self.pos += self.vel


class Flyer(Base):
    """Abstract baseclass for every moving object to inherit from."""

    @abstractmethod
    def kick():
        """Give the object a kick."""


class Static(Base):
    """Abstract baseclass for every stationary object to inherit from."""


class Rocket(Flyer):

    """Class for a rocket that can manouvre using thrusters that give it a kick."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialise the object with a starting position and velocity.

        Args:
            name: str
                Name the object
            mass: float
                Give the object some mass

        Keyword args:
            pos: pre.Vector2D
                The position vector of the object with respect to origo (0, 0)
            vel: pre.Vector2D
                The velocity vector of the object
            acc: pre.Vector2D
                The acceleration vector of the object
        """
        Flyer.__init__(self, *args, **kwargs)
        self.kick_list = []

    def add_kick_event(self, angle: int, speed: float, time: int):
        bisect.insort(self.kick_list, (time, angle, speed))

    def kick(self, time: int):
        """Kicking the rocket object will completely reset its velocity.

        No matter what the previous velocity was like, the direction of its velocity will
        be rotated the amount given, and the magnitude will be changed to what ever speed
        is given.
        """
        if len(self.kick_list) == 0:
            pass
        elif time == self.kick_list[0][0]:
            the_kick = self.kick_list.pop(0)
            self.vel = the_kick[2] * self.vel.normalized() * self.spi
            self.vel = self.vel.rotate(the_kick[1])


class Planet(Static):
    """Class for the planets (and the Sun)."""


class Universe:
    """Class that keeps track of all objects in our universe and calculates their path."""

    def __init__(self, spi=None) -> None:
        self.objects = []
        self.objects_app = self.objects.append
        self.__start: bool = False
        self.__spi: int = 1 if spi is None else spi

    def set_spi(self, spi: int) -> None:
        if not self.__start:
            self.__spi = spi
        else:
            print(
                "The simulation of the universe already started. Not resetting the spi."
            )

    def add_object(self, *obj: Union[Planet, Rocket]) -> None:
        if not self.__start:
            for o in obj:
                self.objects_app(o)
        else:
            print("You already called the 'ready()' method. Skipping adding objects.")

    def ready(self) -> None:
        self.__start = True
        for obj in self.objects:
            obj.spi = self.__spi
            obj.reset_movement()

    def move(self, time):
        if not self.__start:
            raise ValueError(
                "Please initialise the universe by calling the 'ready()' method."
            )
        # We first update the new acceleration of each object based on a snapshot in time
        for obj in self.objects:
            self.__calculate_force(obj)

        # Let us now update the movement of each object with the gravitational pull it
        # gets from all the other objects
        for obj in self.objects:
            obj.move()
            if isinstance(obj, Rocket):
                obj.kick(time)

    def __calculate_force(self, obj) -> None:
        net_force = pre.Vector2D(0, 0)
        for o in [y for y in self.objects if y is not obj]:
            distance_vec = o.pos - obj.pos
            gravityForce = G * (obj.mass * o.mass) / (abs(distance_vec) ** 2)
            net_force += gravityForce * distance_vec.normalized()
        obj.acc = net_force / obj.mass
