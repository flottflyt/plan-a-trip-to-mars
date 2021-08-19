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
        """Initialise what ever we want to use to view the simulation."""
        self.create_complete_universe()

    def create_complete_universe(self) -> None:
        # Create the Sun, Earth and Mars
        sun = uni.Planet("Sun", cf.M_sun)
        earth = uni.Planet(
            "Earth",
            cf.M_earth,
            pos=pre.Vector2D(cf.D_earth, 0),
            vel=pre.Vector2D(0, cf.V_earth),
        )
        mars_angle = 100
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
            vel=pre.Vector2D(0, 6e3 + cf.V_earth),
        )

        # mars_shuttle.add_kick_event(0, 1e4, 20)
        # mars_shuttle.add_kick_event(-90, 1e5, 1000)
        # mars_shuttle.add_kick_event(-180, 5e4, 100)

        self.my_uni = uni.Universe()
        self.my_uni.add_object(sun, earth, mars, mars_shuttle)

    def start_simulation(self) -> None:
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
            # per passage, but it does the job.
            if abs(e_angle - m_angle) < 1:
                print(f"Aligned at {time = }")
            if abs(180 - e_angle + m_angle) < 1:
                print(f"Opposite of each other at {time = }")

            # Add check to see if the rocket is close to Mars ...

        _ = ani.AnimatedScatter(self.my_uni.objects)
        plt.show()


def main():
    sim = Sim()
    sim.start_simulation()


if __name__ == "__main__":
    main()
