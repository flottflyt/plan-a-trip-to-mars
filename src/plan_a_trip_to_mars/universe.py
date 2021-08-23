"""This script implements classes for objects that can move in a 2D space.
"""

import bisect
from abc import ABC, abstractmethod
from typing import Union

import plan_a_trip_to_mars.misc.precode2 as pre

# Gravitational constant
G = 6.6743e-11


class Base(ABC):
    """Abstract baseclass that every moving object in the universe inherit from."""

    def __init__(
        self,
        name: str,
        mass: float,
        pos: pre.Vector2D = pre.Vector2D(0, 0),
        vel: pre.Vector2D = pre.Vector2D(0, 0),
        acc: pre.Vector2D = pre.Vector2D(0, 0),
    ) -> None:
        """Initialise with a starting position and velocity.

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
    """Abstract baseclass that every stationary object inherit from.

    Any object that cannot move itself using thrusters or similar is a Static. That
    includes stars, planets, moons and so on.
    """


class Rocket(Flyer):

    """Class for a rocket that can manoeuvre using thrusters that give it a kick."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialise the object with a starting position and velocity.

        Args:
            name: str
                Name the object
            mass: float
                Give the object some mass

        Keyword args:
            pos: pre.Vector2D
                The position vector of the object with respect to the origin (0, 0)
            vel: pre.Vector2D
                The velocity vector of the object
            acc: pre.Vector2D
                The acceleration vector of the object
        """
        Flyer.__init__(self, *args, **kwargs)
        self.kick_list = []

    def add_kick_event(self, angle: int, speed: float, time: int) -> None:
        """Add an instant change of the velocity vector at any time during the simulation.

        Args:
            angle: int (degrees)
                The angle that the velocity vector should be rotated in degrees. Positive
                values rotate the vector to the left, negative to the right, just at you
                would expect from the right hand rule.
            speed: float
                The change in speed from the current speed (delta V)
        """
        bisect.insort(self.kick_list, (time, angle, speed))

    def kick(self, time: int) -> None:
        """Kicking the rocket object will completely reset its velocity.

        No matter what the previous velocity was like, the direction of its velocity will
        be rotated the amount given, and the magnitude will be changed to what ever speed
        is given.

        Args:
            time: int
                The simulation time at which the kick should take effect.
        """
        if len(self.kick_list) == 0:
            pass
        elif time == self.kick_list[0][0]:
            # pop removes the last element of the list and returns it. Giving the 0
            # argument (or in general any int 'n') removes the 0-th (n-th) element and
            # returns it.
            the_kick = self.kick_list.pop(0)
            delV = the_kick[2] * self.vel.normalized() * self.spi
            self.vel += delV
            self.vel = self.vel.rotate(the_kick[1])


class Planet(Static):
    """Class for the stars, planets and moons."""


class Universe:
    """Class that keeps track of all objects in our universe and calculates their path."""

    def __init__(self, spi=None) -> None:
        """Initialise the universe.

        We assume that some objects will be included in the universe, and thus create a
        list to place them in. We also set a boolean to False that makes sure some things
        cannot be done / can only be done when it is False. For example it would make no
        sense adding more objects to the universe after the simulation have started.

        Keyword args:
            spi: int (optional)
                Set the 'seconds-per-iteration'. Defaults to one. This can also be set at
                a later point using the method 'set_spi()'.
        """
        self.objects = []
        self.objects_app = self.objects.append
        self.__start: bool = False
        self.__spi: int = 1 if spi is None else spi

    def set_spi(self, spi: int) -> None:
        """Set the 'seconds-per-iteration' value.

        Args:
            spi: int
                Decide how many seconds passes per iteration.
        """
        if not self.__start:
            self.__spi = spi
        else:
            print(
                "The simulation of the universe already started. Not re-setting the spi."
            )

    def add_object(self, *obj: Union[Planet, Rocket]) -> None:
        """Add any number of objects to the universe as an unordered list of arguments.

        Args:
            obj: Union[Planet, Rocket]
                Adds the object to the list of object. Can be either a Planet object or a
                Rocket object.
        """
        if not self.__start:
            for o in obj:
                self.objects_app(o)
        else:
            print("You already called the 'ready()' method. Skipping adding objects.")

    def ready(self) -> None:
        """Let the universe know you are done modifying it, and ready to simulate.

        Sets the hidden attribute __start to True and updates all objects with the
        current 'spi' value.
        """
        self.__start = True
        for obj in self.objects:
            obj.spi = self.__spi
            obj.reset_movement()

    def move(self, time):
        """Update all objects in the universe.

        Calling this method moves the universe one time step forward. The position,
        velocity and acceleration vectors of each object are updated depending on all
        other objects.
        """
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

    def __calculate_force(self, obj: Union[Planet, Rocket]) -> None:
        """Should be called only from within this class.

        Updates the gravitational force a given object feels from all other objects in the
        universe.

        Args:
            obj: Union[Planet, Rocket]
                Adds the object to the list of object. Can be either a Planet object or a
                Rocket object.
        """
        # Starts with a net force of zero
        net_force = pre.Vector2D(0, 0)

        # The list comprehension picks out all objects from self.objects that is not the
        # one objects we are looking at
        for o in [y for y in self.objects if y is not obj]:
            # Find the distance vector between one of the other objects and calculate the
            # gravitational pull it get from this
            distance_vec = o.pos - obj.pos
            gravityForce = G * (obj.mass * o.mass) / (abs(distance_vec) ** 2)
            # Add the gravitational pull from this one object to the net sum of all forces
            net_force += gravityForce * distance_vec.normalized()

        obj.acc = net_force / obj.mass
