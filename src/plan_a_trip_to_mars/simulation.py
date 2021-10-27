"""The script where we program what the simulated universe should look like.
"""

from plan_a_trip_to_mars import scenarios

__SCENARIOS__ = {
    1: scenarios.Simpl,
    2: scenarios.Mayhem,
    3: scenarios.Jerk,
}


class Sim:
    def __init__(self) -> None:
        """Initialise the simulation setup."""
        self.scenario = __SCENARIOS__[3]()
        self.save: tuple[bool, str] = (False, "mp4")
        self.trace: bool = True

    def run_simulation(self) -> None:
        """Run the simulation."""
        self.scenario.run_simulation()

    def play_animation(self) -> None:
        """Re-create the simulation by animating the trace of the objects."""
        self.scenario.play_animation(self.save, self.trace)


def main():
    sim = Sim()
    sim.run_simulation()
    sim.play_animation()


if __name__ == "__main__":
    main()
