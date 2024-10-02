"""Implementation of classes for objects that can move in a 2D space."""

from abc import abstractmethod
from dataclasses import dataclass

import plan_a_trip_to_mars.misc.precode2 as pre
from plan_a_trip_to_mars.config import G


@dataclass
class Kicker:
    """Container object for a kick given to a flyer object.

    By default, the angle refers to the current velocity of the rocket. If, however, the
    velocity of the rocket is zero, so that it cannot be normalised, the direction is
    re-set to the default direction towards east / right, and angle will describe the
    angle on a typical unit circle. This behaviour can also be accomplished by setting
    `static` to True (referring to a static coordinate system).

    Attributes
    ----------
    angle : float
        The angle that the velocity vector should be rotated in degrees. Positive values
        rotate the vector anti-clockwise, negative clockwise, just as you would expect
        from the right hand rule.
    speed : float
        The change in speed from the current speed (delta V). If `multiply` is set to
        `True`, this will instead scale the current speed.
    time : int
        The simulation time when the kick should be applied.
    multiply : bool
        If the current speed should be multiplied by the speed provided, or added.
        Default is to add.
    static : bool, optional
        If the angle is with respect to the universe grid, set static to True,
        otherwise, the angle is relative to the velocity of the rocket. Defaults to
        False.
    """

    angle: float
    speed: float
    time: int
    multiply: bool = False
    static: bool = False


class Base:
    """Abstract baseclass that every moving object in the universe inherit from.

    Parameters
    ----------
    name : str
        Name the object
    mass : float
        Give the object some mass
    pos : pre.Vector2D | None
        The position vector of the object with respect to origo (0, 0)
    vel : pre.Vector2D | None
        The velocity vector of the object
    acc : pre.Vector2D | None
        The acceleration vector of the object
    """

    def __init__(
        self,
        name: str,
        mass: float,
        pos: pre.Vector2D | None = None,
        vel: pre.Vector2D | None = None,
        acc: pre.Vector2D | None = None,
    ) -> None:
        self.spi: int = 1
        self.name = name
        self.mass = mass
        self.trace: list[tuple[float, float]] = []
        self.pos_init = pos or pre.Vector2D(0, 0)
        self.vel_init = vel or pre.Vector2D(0, 0)
        self.acc_init = acc or pre.Vector2D(0, 0)
        self.reset_movement()

    def reset_movement(self) -> None:
        """Reset the position, velocity and acceleration to the initial values."""
        self.pos = self.pos_init
        self.vel = self.vel_init * self.spi
        self.acc = self.acc_init * self.spi**2

    def move(self) -> None:
        """Move the objects in the universe."""
        self.trace.append(self.pos.as_point)
        self.vel += self.acc * self.spi**2
        self.pos += self.vel


class Flyer(Base):
    """Baseclass for every moving object to inherit from."""

    @abstractmethod
    def kick(self, time: int) -> None:
        """Give the object a kick."""


class Static(Base):
    """Baseclass that every stationary object inherit from.

    Any object that cannot move itself using thrusters or similar is a Static. That
    includes stars, planets, moons and so on.
    """


class Rocket(Flyer):
    """Class for a rocket that can manoeuvre using thrusters that give it a kick.

    Parameters
    ----------
    name : str
        Name the object
    mass : float
        Give the object some mass
    pos : pre.Vector2D | None
        The position vector of the object with respect to the origin (0, 0)
    vel : pre.Vector2D | None
        The velocity vector of the object
    acc : pre.Vector2D | None
        The acceleration vector of the object
    """

    def __init__(
        self,
        name: str,
        mass: float,
        pos: pre.Vector2D | None = None,
        vel: pre.Vector2D | None = None,
        acc: pre.Vector2D | None = None,
    ) -> None:
        Flyer.__init__(self, name=name, mass=mass, pos=pos, vel=vel, acc=acc)
        self.kick_list: list[Kicker] = []

    def add_kick_event(self, *kick: Kicker) -> None:
        """Add an instant change of the velocity vector at any time during the simulation.

        Parameters
        ----------
        *kick : Kicker
            Any number of Kicker container objects.
        """
        seen = {k.time for k in self.kick_list}
        unique = []
        for obj in kick:
            if obj.time not in seen:
                unique.append(obj)
                seen.add(obj.time)
            else:
                print(
                    f"WARNING: Several kick events cannot be set to the same time. Skipping the event {obj}."
                )
        self.kick_list = self.kick_list + unique

    def kick(self, time: int) -> None:
        """Kicking the rocket object will completely reset its velocity.

        No matter what the previous velocity was like, the direction of its velocity will
        be rotated the amount given, and the magnitude will be changed to what ever speed
        is given.

        Parameters
        ----------
        time : int
            The simulation time at which the kick should take effect.
        """
        if len(self.kick_list) == 0:
            pass
        elif time == self.kick_list[0].time:
            # pop removes the last element of the list and returns it. Giving the 0
            # argument (or in general any int 'n') removes the 0-th (n-th) element and
            # returns it.
            the_kick = self.kick_list.pop(0)
            try:
                self.vel.normalized()
            except ZeroDivisionError:
                direction: pre.Vector2D = pre.Vector2D(1, 0)
            else:
                direction = pre.Vector2D(1, 0) if the_kick.static else self.vel
            if the_kick.multiply:
                delta_v = direction.normalized() * self.spi
                delta_v = delta_v.rotate(the_kick.angle)
                self.vel = self.vel.rotate(the_kick.angle)
                self.vel *= the_kick.speed
            else:
                delta_v = the_kick.speed * direction.normalized() * self.spi
                delta_v = delta_v.rotate(the_kick.angle)
                self.vel += delta_v


class Planet(Static):
    """Class for stars, planets and moons."""


class Universe:
    """Class that keeps track of all objects in our universe and calculates their path.

    We assume that some objects will be included in the universe, and thus create a list
    to place them in. We also set a boolean to False that makes sure some things cannot
    be done / can only be done when it is False. For example it would make no sense
    adding more objects to the universe after the simulation have started.

    Parameters
    ----------
    spi : int | None
        Set the 'seconds-per-iteration'. Defaults to one. This can also be set at a
        later point using the method 'set_spi()'.
    """

    def __init__(self, spi: int | None = None) -> None:
        self.objects: list[Planet | Rocket] = []
        self.objects_app = self.objects.append
        self._start: bool = False
        self._spi: int = 1 if spi is None else spi

    def set_spi(self, spi: int) -> None:
        """Set the 'seconds-per-iteration' value.

        Parameters
        ----------
        spi : int
            Decide how many seconds passes per iteration.
        """
        if not self._start:
            self._spi = spi
        else:
            print(
                "The simulation of the universe already started. Not re-setting the spi."
            )

    def add_object(self, *obj: Planet | Rocket) -> None:
        """Add any number of objects to the universe as an unordered list of arguments.

        Parameters
        ----------
        *obj : Planet | Rocket
            Adds the object to the list of object. Can be either a Planet object or a
            Rocket object.
        """
        if not self._start:
            for o in obj:
                self.objects_app(o)
        else:
            print("You already called the 'ready()' method. Skipping adding objects.")

    def ready(self) -> None:
        """Let the universe know you are done modifying it, and ready to simulate.

        Sets the hidden attribute _start to True and updates all objects with the
        current 'spi' value.
        """
        if not self.objects:
            msg = (
                "You forgot to add/implement any Planet and/or Rocket objects. You can "
                "make a planet with the Planet class and a rocket with the Rocket "
                "class. Add them to your universe with method `self.add_object()`."
            )
            raise NotImplementedError(msg)
        self._start = True
        for obj in self.objects:
            obj.spi = self._spi
            obj.reset_movement()

    def move(self, time: int) -> None:
        """Update all objects in the universe.

        Calling this method moves the universe one time step forward. The position,
        velocity and acceleration vectors of each object are updated depending on all
        other objects.
        """
        if not self._start:
            msg = "Please initialise the universe by calling the 'ready()' method."
            raise ValueError(msg)
        # We first update the new acceleration of each object based on a snapshot in time
        for obj in self.objects:
            self._calculate_force(obj)

        # Let us now update the movement of each object with the gravitational pull it
        # gets from all the other objects
        for obj in self.objects:
            obj.move()
            if isinstance(obj, Rocket):
                obj.kick(time)

    def _calculate_force(self, obj: Planet | Rocket) -> None:
        """Calculate the sum of forces on each object.

        Updates the gravitational force a given object feels from all other objects in the
        universe.

        Should be called only from within this class.

        Parameters
        ----------
        obj : Planet | Rocket
            Adds the object to the list of object. Can be either a Planet object or a
            Rocket object.
        """
        # Starts with a net force of zero
        net_force: pre.Vector2D = pre.Vector2D(0, 0)

        # The list comprehension picks out all objects from self.objects that is not the
        # one objects we are looking at
        for o in [y for y in self.objects if y is not obj]:
            # Find the distance vector between one of the other objects and calculate the
            # gravitational pull it get from this
            distance_vec = o.pos - obj.pos
            gravity = G * (obj.mass * o.mass) / (abs(distance_vec) ** 2)
            # Add the gravitational pull from this one object to the net sum of all forces
            net_force += gravity * distance_vec.normalized()

        obj.acc = net_force / obj.mass
