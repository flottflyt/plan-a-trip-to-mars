"""Scenarios to run in the simulation class."""

import math
import os
from abc import ABC, abstractmethod
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np

import plan_a_trip_to_mars.config as cf
import plan_a_trip_to_mars.misc.animate as ani
import plan_a_trip_to_mars.misc.precode2 as pre
import plan_a_trip_to_mars.universe as uni


class BigScenario(ABC):
    """Abstract baseclass to create simulation scenarios."""

    # All times are in seconds
    SIZE = 3 * cf.AU  # The side length of the simulated universe
    # The time actual time used by the simulation is
    FPS = 24  # Frames-per-second: speed up the animation
    TOT_TIME = 5e4  # The total time the animation should run
    # Scale current time scale to get to a better unit, e.g. seconds to days:
    # TIME_SCALE = 3600 * 24
    TIME_SCALE = 1
    UNIT = ""

    def __init__(self) -> None:
        self.my_uni = uni.Universe()
        self._create_complete_univers()
        self.__finally()

    @abstractmethod
    def _create_complete_univers(self) -> None:
        """Abstract method that create objects and add them to the universe 'self.my_uni'.

        This code is run before the universe is simulated. This means that everything you
        want to be included in the universe should be included here. This method also
        creates the 'storyline'. If you want something to happen at some specified time,
        for example that a rocket should be launched at a specific day, this must be set
        here.

        Note that the time used in the universe is seconds, unless some scaling is given
        with the `uni.Universe().set_spi()` method, which specifies how many
        'seconds-per-iteration' should be used.
        """

    def __finally(self) -> None:
        """Method that locks the universe for further changes."""
        self.my_uni.ready()

    def run_simulation(self) -> None:
        for time in range(int(self.TOT_TIME)):
            self.my_uni.move(time)
            self._run_simulation(time)

    def _run_simulation(self, time: int) -> None:
        """Any logic that should be done every time step of the simulation.

        This is called at each time step of the simulation. This means that everything
        that cannot be determined before the simulation is done goes here. For example, if
        you try to answer a question using your simulation, the checks needed to obtain
        the answer from the simulation must be implemented here.
        """

    def play_animation(self, save: tuple[bool, str], trace: bool) -> None:
        """Re-create the simulation by animating the trace of the objects."""
        # Now that the for loop is finished, the whole simulation is also finished. But
        # instead of animating every step, let us speed things up by keeping only every
        # n-th item from the trace lists.
        n = self.FPS
        for obj in self.my_uni.objects:
            obj.trace = obj.trace[0::n]
        a = ani.AnimatedScatter(
            self.my_uni.objects,
            self.FPS,
            self.TOT_TIME,
            self.SIZE,
            self.TIME_SCALE,
            self.UNIT,
        )
        a.show_trace = trace
        if save[0]:
            os.makedirs("data", exist_ok=True)
            a.ani.save(f"data/animation.{save[1]}", fps=self.FPS)
        plt.show()


class MarsTransfer(BigScenario):
    """Simulate a transition from Earth to Mars."""

    # Change the default SIZE and FPS of the universe
    SIZE = 2.5 * cf.AU
    FPS = 24
    TOT_TIME = 24 * 365 * 2

    def _create_complete_univers(self) -> None:
        """Implement the objects and events of our universe.

        Let us create four objects; the Sun, Earth, Mars and a rocket. Then we give the
        rocket many arbitrary kicks just to see an example of how the `kick` actually
        works.
        """

        # Create the Sun, Earth and Mars
        sun = uni.Planet("Sun", cf.M_sun)
        earth = uni.Planet(
            "Earth",
            cf.M_earth,
            pos=pre.Vector2D(cf.D_earth, 0),
            vel=pre.Vector2D(0, cf.V_earth),
        )
        mars_angle = 47
        mars = uni.Planet(
            "Mars",
            cf.M_mars,
            pos=pre.Vector2D(cf.D_mars, 0).rotate(mars_angle),
            vel=pre.Vector2D(0, cf.V_mars).rotate(mars_angle),
        )

        # Create a rocket
        mars_shuttle = uni.Rocket(
            "Go!",
            1e4,
            pos=pre.Vector2D(cf.D_earth, 10 * cf.R_earth),
            vel=pre.Vector2D(0, 4.8e3 + cf.V_earth),
        )

        mars_shuttle.add_kick_event(0, 2.65e3, 250 * 24)
        # mars_shuttle.add_kick_event(0, cf.V_mars, 250 * 24)
        # mars_shuttle.add_kick_event(0, cf.V_mars, 250)

        # Create the universe all objects should live in
        self.my_uni.add_object(sun, earth, mars, mars_shuttle)
        self.my_uni.set_spi(3600)

    def _run_simulation(self, time) -> None:
        """Run the simulation.

        We loop through the total time given in `config.py` and update the universe at
        each time step with the 'move()' method. Additionally we may add some more logic
        that is checked at each time step, for example when the Earth and Mars are aligned
        with the Sun.
        """
        # Let us add some code that checks whether Sun, Earth and Mars are aligned.
        s = self.my_uni.objects[0].pos.copy()
        e = self.my_uni.objects[1].pos.copy()
        e = e - s
        e_angle = math.degrees(math.atan2(e.y, e.x))
        m = self.my_uni.objects[2].pos.copy()
        m = m - s
        m_angle = math.degrees(math.atan2(m.y, m.x))

        # We say that if their angular positions differ with less than one degree,
        # they are at the same place in their orbits. This will trigger more than once
        # per passage, but it does the job. Note also that the 'spi' value greatly
        # influences the numerical precision and also the number of times the
        # if-statements below will trigger.
        if abs(e_angle - m_angle) < 1:
            print(f"Aligned at time = {time % int(self.TOT_TIME / self.FPS)}")
            # New syntax in python >=3.9
            # print(f"Aligned at {time = }")
        if abs(180 - e_angle + m_angle) < 1:
            print(
                f"Opposite of each other at time = {time % int(self.TOT_TIME / self.FPS)}"
            )
            # New syntax in python >=3.9
            # print(f"Opposite of each other at {time = }")

        # Add check to see if the rocket is close to Mars ...


class Simpl(BigScenario):

    SIZE = 3e3
    TOT_TIME = 50 * 60 * 24
    TIME_SCALE = 60
    UNIT = " mins"

    def _create_complete_univers(self) -> None:
        """Simplest case."""
        stone = uni.Planet(
            "Stone", 1e14, pos=pre.Vector2D(1e3, -1e3), vel=pre.Vector2D(0, 1.1)
        )
        rock = uni.Planet(
            "Rock", 1e14, pos=pre.Vector2D(-1e3, -1e3), vel=pre.Vector2D(0, -1)
        )
        self.my_uni.add_object(stone, rock)


class Parabolic(BigScenario):

    SIZE = 5 * cf.AU
    TOT_TIME = 1e4
    FPS = 24
    UNIT = " days"

    def _create_complete_univers(self) -> None:
        """Simplest case."""
        sun = uni.Planet(
            "Sun",
            cf.M_sun,
            pos=pre.Vector2D(0, 0),
            vel=pre.Vector2D(0, 0),
        )
        rock = uni.Rocket(
            "Rock",
            1e4,
            pos=pre.Vector2D(-cf.AU, 0),
            vel=pre.Vector2D(0, cf.V_earth),
        )
        rotates = 49
        stone = uni.Planet(
            "Stone",
            1e4,
            pos=pre.Vector2D(-0.5 * cf.AU, 0).rotate(rotates),
            vel=pre.Vector2D(0, 2 * cf.V_earth).rotate(rotates),
        )
        v_r = (1.0 * cf.G * cf.M_sun / cf.AU) ** (1 / 2)
        rock.add_kick_event(90, v_r, 1000)
        self.my_uni.add_object(sun, rock, stone)
        self.my_uni.set_spi(3600)


class Mayhem(BigScenario):

    TOT_TIME = 5e4
    SIZE = 5 * cf.AU

    def _create_complete_univers(self) -> None:
        """Absolute mayhem."""
        self.my_uni.set_spi(3600)
        rockets = ["1", "2", "3", "4", "5"]
        m = 1e30
        origo = pre.Vector2D(0, - 4 * cf.AU)
        poss = [
            origo + pre.Vector2D(-cf.AU, 0),
            origo + pre.Vector2D(-cf.AU, 0).rotate(245),
            origo + pre.Vector2D(-cf.AU, 0).rotate(40),
            origo + pre.Vector2D(-cf.AU, 0).rotate(330),
            origo + pre.Vector2D(-cf.AU, 0).rotate(180),
        ]
        vels = [
            pre.Vector2D(0, cf.V_earth).rotate(180),
            pre.Vector2D(0, cf.V_earth).rotate(80),
            pre.Vector2D(0, cf.V_earth).rotate(280),
            pre.Vector2D(0, cf.V_earth).rotate(10),
            pre.Vector2D(0, cf.V_earth),
        ]
        objs = [uni.Rocket(n, m, p, v) for n, p, v in zip(rockets, poss, vels)]
        self.my_uni.add_object(*objs)
        angle = [180, 277, 10, 200, 55, 170, 234, 62, 300, 340, 145, 82, 91, 240, 340, 180, 180, 180, 180, 180, 180]
        velocities = (
            np.array(
                [180, 277, 10, 0, 55, 170, 34, 62, 30, 30, 45, 82, 91, 0, 0, 20, 200, 200, 200, 200, 0]
            )
            * cf.V_earth
            / 100
        )
        times = (
            np.array(
                [180, 277, 10, 60, 55, 170, 34, 62, 300, 340, 45, 82, 91, 240, 340, 20, 180, 180, 180, 180, 180]
            )
            * 24
        )
        # for o, a, v, t in zip(cycle(objs), angle, velocities, times):
        #     o.add_kick_event(a, v, int(t))
