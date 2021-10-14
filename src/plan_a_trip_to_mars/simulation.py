"""The script where we program what the simulated universe should look like.
"""

import math

import matplotlib.pyplot as plt

import plan_a_trip_to_mars.config as cf
import plan_a_trip_to_mars.misc.animate as ani
import plan_a_trip_to_mars.misc.precode2 as pre
import plan_a_trip_to_mars.universe as uni


class Sim:
    def __init__(self) -> None:
        """Initialise the simulation setup."""
        self.create_complete_universe()

    def create_complete_universe(self) -> None:
        """Implement the objects and events of our universe."""

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
        self.my_uni = uni.Universe()
        self.my_uni.add_object(sun, earth, mars, mars_shuttle)
        self.my_uni.set_spi(3600)
        self.my_uni.ready()

    def run_simulation(self) -> None:
        """Run the simulation.

        We loop through the total time given in `config.py` and update the universe at
        each time step with the 'move()' method. Additionally we may add some more logic
        that is checked at each time step, for example when the Earth and Mars are aligned
        with the Sun.
        """
        for time in range(int(cf.TOT_TIME)):
            self.my_uni.move(time)

            # Let us add some code that checks whether Sun, Earth and Mars is aligned.
            s = self.my_uni.objects[0].pos.copy()
            e = self.my_uni.objects[1].pos.copy()
            e = e - s
            e_angle = math.degrees(math.atan2(e.y, e.x))
            m = self.my_uni.objects[2].pos.copy()
            m = m - s
            m_angle = math.degrees(math.atan2(m.y, m.x))

            # We say that if their angular positions differ with less than one degree,
            # thay are at the same place in their orbits. This will trigger more than once
            # per passage, but it does the job. Note also that the spi value greatly
            # influences the  numerical precision and also the number of times the
            # if-statements below will trigger.
            if abs(e_angle - m_angle) < 1:
                print(f"Aligned at time = {time}")
                # New syntax in python >=3.9
                # print(f"Aligned at {time = }")
            if abs(180 - e_angle + m_angle) < 1:
                print(f"Opposite of each other at time = {time}")
                # New syntax in python >=3.9
                # print(f"Opposite of each other at {time = }")

            # Add check to see if the rocket is close to Mars ...

    def play_animation(self) -> None:
        """Re-create the simulation by animating the trace of the objects."""
        # Now that the for loop is finished, the whole simulation is also finished. But
        # instead of animating every step, let us speed things up by keeping only every
        # n-th item from the trace lists.
        n = cf.FPS
        for obj in self.my_uni.objects:
            obj.trace = obj.trace[0::n]
        a = ani.AnimatedScatter(self.my_uni.objects)
        a.show_trace = True
        plt.show()


def main():
    sim = Sim()
    sim.run_simulation()
    sim.play_animation()


if __name__ == "__main__":
    main()
