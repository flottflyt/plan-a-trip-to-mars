"""Scenarios to run in the simulation class."""

import math
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt

import plan_a_trip_to_mars.config as cf
import plan_a_trip_to_mars.misc.animate as ani
import plan_a_trip_to_mars.misc.precode2 as pre
import plan_a_trip_to_mars.universe as uni


class BigScenario(ABC):
    """Abstract baseclass to create simulation scenarios."""

    # All times are in seconds
    FPS = 24  # Frames-per-second: speed up the animation
    SIZE = 3 * cf.AU  # The side length of the simulated universe
    TOT_TIME = 5e4  # The total time the animation should run

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
        """

    def __finally(self) -> None:
        """Method that locks the universe for further changes."""
        self.my_uni.ready()

    def run_simulation(self) -> None:
        for time in range(int(self.TOT_TIME)):
            self.my_uni.move(time)
            self._run_simulation(time)

    @abstractmethod
    def _run_simulation(self, time: int) -> None:
        """Any logic that should be done every time step of the simulation.

        This is called at each time step of the simulation. This means that everything
        that cannot be determined before the simulation is done goes here. For example, if
        you try to answer a question using your simulation, the checks needed to obtain
        the answer from the simulation must be implemented here.
        """

    def play_animation(self) -> None:
        """Re-create the simulation by animating the trace of the objects."""
        # Now that the for loop is finished, the whole simulation is also finished. But
        # instead of animating every step, let us speed things up by keeping only every
        # n-th item from the trace lists.
        n = self.FPS
        for obj in self.my_uni.objects:
            obj.trace = obj.trace[0::n]
        a = ani.AnimatedScatter(self.my_uni.objects, self.FPS, self.SIZE, self.TOT_TIME)
        a.show_trace = True
        plt.show()


class MarsTransfer(BigScenario):
    """Simulate a transition from Earth to Mars."""

    # Change the default SIZE and FPS of the universe
    SIZE = 2.5 * cf.AU
    FPS = 10

    def _create_complete_univers(self) -> None:
        """Implement the objects and events of our universe.

        Let us create four objects; the Sun, Erath, Mars and a rocket. Then we give the
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
