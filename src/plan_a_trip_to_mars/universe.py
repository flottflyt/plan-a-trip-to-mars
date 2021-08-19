"""This script implements classes for objects that can move in a 2D space.
"""

import bisect
from abc import ABC, abstractmethod
from typing import Union

import matplotlib.pyplot as plt

import plan_a_trip_to_mars.config as cf
import plan_a_trip_to_mars.misc.precode2 as pre


class Flyer(ABC):
    """Abstract baseclass for every moving object to inherit from."""

    # @abstractmethod
    # def draw():
    #     """Abstract draw method as a declarator.

    #     Draw method should be implemented for all Flyer-classes.
    #     """

    @abstractmethod
    def move():
        """Abstract move method as a declarator.

        Move method should be implemented for all Flyer-classes.
        """

    @abstractmethod
    def kick():
        """Give the object a kick."""


class Static(ABC):
    """Abstract baseclass for every stationary object to inherit from."""

    # @abstractmethod
    # def draw():
    #     """Abstract draw method as a declarator.

    #     Draw method should be implemented for all Flyer-classes.
    #     """

    @abstractmethod
    def move():
        """Abstract move method as a declarator.

        Move method should be implemented for all Flyer-classes.
        """


class Rocket(Flyer):

    """Class for a rocket that can manouvre using thrusters that give it a kick."""

    def __init__(
        self,
        name,
        mass: float,
        pos: pre.Vector2D = pre.Vector2D(0, 0),
        vel: pre.Vector2D = pre.Vector2D(0, 0),
        acc: pre.Vector2D = pre.Vector2D(0, 0),
    ) -> None:
        """Initialise the object with a starting position and velocity."""
        self.name = name
        self.mass = mass
        self.pos = pos
        self.vel = vel * cf.FPS
        self.acc = acc * cf.FPS ** 2
        self.trace = []
        self.kick_list = []

    def move(self):
        self.trace.append(self.pos.as_point)
        self.vel += self.acc * cf.FPS ** 2
        self.pos += self.vel

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
            self.vel = the_kick[2] * self.vel.normalized() * cf.FPS
            self.vel = self.vel.rotate(the_kick[1])


class Planet(Static):
    """Class for the planets (and the Sun)."""

    def __init__(
        self,
        name: str,
        mass: float,
        pos: pre.Vector2D = pre.Vector2D(0, 0),
        vel: pre.Vector2D = pre.Vector2D(0, 0),
        acc: pre.Vector2D = pre.Vector2D(0, 0),
    ) -> None:
        self.name = name
        self.mass = mass
        self.pos = pos
        self.vel = vel * cf.FPS
        self.acc = acc * cf.FPS ** 2
        self.trace = []

    def move(self):
        self.trace.append(self.pos.as_point)
        self.vel += self.acc * cf.FPS ** 2
        self.pos += self.vel


class Universe:
    """Class that keeps track of all objects in our universe and calculates their path."""

    def __init__(self) -> None:
        self.objects = []
        self.objects_app = self.objects.append

    def add_object(self, *obj: Union[Planet, Rocket]) -> None:
        for o in obj:
            self.objects_app(o)

    def move(self, time):
        # Make a copy so we can update based on a snapshot in time
        force_list = []
        force_list_app = force_list.append
        for obj in self.objects:
            # force_list_app(self.calculate_force(obj))
            self.calculate_force(obj)

        # Let us now update the movement of each object with the gravitational pull it
        # gets from all the other objects
        for obj in self.objects:
            obj.move()
            if isinstance(obj, Rocket):
                obj.kick(time)

    def calculate_force(self, obj) -> None:
        net_force = pre.Vector2D(0, 0)
        for o in [y for y in self.objects if y is not obj]:
            distance_vec = o.pos - obj.pos
            gravityForce = cf.G * (obj.mass * o.mass) / (abs(distance_vec) ** 2)
            net_force += gravityForce * distance_vec.normalized()
        obj.acc = net_force / obj.mass
