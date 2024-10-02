"""Scenarios to run in the simulation class."""

import math
import pathlib
from abc import ABC, abstractmethod

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

    def setup(self) -> None:
        """Set up the simulation scenario."""
        self.my_uni = uni.Universe()
        self.create_complete_universe()
        self.__finally()

    @abstractmethod
    def create_complete_universe(self) -> None:
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
        """Lock the universe for further changes."""
        self.my_uni.ready()

    def run_simulation(self) -> None:
        """Start running the simulation."""
        for time in range(int(self.TOT_TIME)):
            self.my_uni.move(time)
            self.do_at_each_time_step(time)

    def do_at_each_time_step(self, time: int) -> None:
        """Any logic that should be done every time step of the simulation.

        This is called at each time step of the simulation. This means that everything
        that cannot be determined before the simulation is done goes here. For example, if
        you try to answer a question using your simulation, the checks needed to obtain
        the answer from the simulation must be implemented here.
        """

    def play_animation(self, save: tuple[bool, str], *, trace: bool) -> None:
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
            data_path = pathlib.Path("data")
            data_path.mkdir(parents=True)
            a.ani.save(data_path / f"animation.{save[1]}", fps=48)
        plt.show()


class Simpl(BigScenario):
    SIZE = 3e3
    TOT_TIME = 50 * 60 * 24
    TIME_SCALE = 60
    UNIT = " mins"

    def create_complete_universe(self) -> None:
        """Simplest case."""
        stone = uni.Planet(
            "Stone", 1e14, pos=pre.Vector2D(1e3, -1e3), vel=pre.Vector2D(0, 1.1)
        )
        rock = uni.Planet(
            "Rock", 1e14, pos=pre.Vector2D(-1e3, -1e3), vel=pre.Vector2D(0, -1)
        )
        self.my_uni.add_object(stone, rock)


class Mayhem(BigScenario):
    TOT_TIME = 3e4
    SIZE = 5 * cf.AU

    def create_complete_universe(self) -> None:
        """Absolute mayhem."""
        self.my_uni.set_spi(3600)
        rockets = ["1", "2", "3", "4", "5"]
        m = 1e30
        origo: pre.Vector2D = pre.Vector2D(0, -4 * cf.AU)

        # If we wanted to to add a lot of kick events...
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
        objs = [
            uni.Rocket(n, m, p, v) for n, p, v in zip(rockets, poss, vels, strict=False)
        ]
        self.my_uni.add_object(*objs)
        angle = [180, 277, 10, 200, 55, 170, 234, 62, 300, 340, 340, 180]
        velocities = (
            np.array([180, 277, 10, 0, 30, 30, 45, 82, 91, 0, 0, 20]) * cf.V_earth / 100
        )
        times = np.array([180, 277, 34, 62, 300, 340, 45, 82, 91, 240, 340, 20]) * 24

        # Cycling through the rockets so that the zip function is not stopped too early.
        # for o, a, v, t in zip(cycle(objs), angle, velocities, times):
        #     o.add_kick_event(a, v, int(t))


class Jerk(BigScenario):
    TOT_TIME = 1e3
    SIZE = 5e3
    FPS = 1

    def create_complete_universe(self) -> None:
        bounce = uni.Rocket("Bounce", 1e3, pos=pre.Vector2D(-1e3, 4e3))
        self.my_uni.add_object(bounce)
        jerks = [
            uni.Kicker(angle=45, speed=10, time=100, static=True),
            uni.Kicker(180, 10, 200, static=False),
            uni.Kicker(-45, 10, 300, static=True),
            uni.Kicker(-90, 10, 350, static=True),
            uni.Kicker(-100, 10, 370, static=True),
            uni.Kicker(-110, 10, 390, static=True),
            uni.Kicker(-120, 10, 410, static=True),
            uni.Kicker(-130, 10, 430, static=True),
            uni.Kicker(-140, 10, 450, static=True),
            uni.Kicker(-150, 10, 470, static=True),
            uni.Kicker(-160, 10, 490, static=True),
            uni.Kicker(-170, 10, 510, static=True),
            uni.Kicker(180, 100, 530, static=False),
            uni.Kicker(180, 17.394, 730, static=False),
            uni.Kicker(-40, 50, 800, static=True),
            uni.Kicker(180, 50, 840, static=False),
            uni.Kicker(110, 50, 841, static=True),
            uni.Kicker(180, 50, 880, static=False),
            uni.Kicker(250, 50, 881, static=True),
            uni.Kicker(180, 50, 920, static=False),
            uni.Kicker(40, 50, 921, static=True),
            uni.Kicker(180, 50, 960, static=False),
            uni.Kicker(180, 50, 961, static=True),
        ]
        bounce.add_kick_event(*jerks)

    def do_at_each_time_step(self, time: int) -> None:
        # Print velocity every 10 time units
        if not time % 10:
            print(abs(self.my_uni.objects[0].vel))
