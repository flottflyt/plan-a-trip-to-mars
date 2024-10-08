"""The script where we program what the simulated universe should look like."""

from plan_a_trip_to_mars import scenarios

__SCENARIOS__: dict[int, scenarios.BigScenario] = {
    1: scenarios.Simpl(),
    2: scenarios.Mayhem(),
    3: scenarios.Jerk(),
    4: scenarios.MarsTransfer(),
    5: scenarios.Parabolic(),
    6: scenarios.Tadpole(),
}


class Sim:
    """Simulate a 2D universe.

    Decide which scenario to run, if and in what format it should be saved and whether
    to show the trace or not.
    """

    def __init__(self) -> None:
        self.scenario = __SCENARIOS__[3]
        self.scenario.setup()
        self.save: tuple[bool, str] = (False, "mp4")
        self.trace: bool = False

    def run_simulation(self) -> None:
        """Run the simulation."""
        self.scenario.run_simulation()

    def play_animation(self) -> None:
        """Re-create the simulation by animating the trace of the objects."""
        self.scenario.play_animation(self.save, trace=self.trace)


def main():
    sim = Sim()
    sim.run_simulation()
    sim.play_animation()


if __name__ == "__main__":
    main()
