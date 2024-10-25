"""The script where we program what the simulated universe should look like."""

import contextlib
import inspect
import sys
from dataclasses import dataclass

from returns.maybe import Maybe, Nothing, Some
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from plan_a_trip_to_mars import scenarios

console = Console()


@dataclass
class Scenario:
    """Container for a simulation scenario."""

    name: str
    sim: scenarios.BigScenario


class Sim:
    """Simulate a 2D universe.

    Decide which scenario to run, if and in what format it should be saved and whether
    to show the trace or not.
    """

    def __init__(self) -> None:
        self.save: bool = False
        self.save_as: str = "mp4"
        self.trace: bool = True
        self.suppress_prints: bool = False
        self._set_simulation_menu()

    def _set_simulation_menu(self) -> None:
        self.scenarios: list[Scenario] = [
            Scenario(name=n, sim=c())
            for n, c in inspect.getmembers(scenarios, inspect.isclass)
            if c.__module__ == "plan_a_trip_to_mars.scenarios" and n != "BigScenario"
        ]
        self.options = [str(i) for i, _ in enumerate(self.scenarios, start=1)]
        table = Table(box=None)
        table.add_column("Selection", style="cyan")
        table.add_column("Item", style="magenta")
        for i, s in zip(self.options, self.scenarios, strict=True):
            table.add_row(i, s.name)
        table.add_row("s", "Settings")
        table.add_row("q", "Quit")
        self.menu_items = table

    def loop(self) -> None:
        """Run the simulation as an infinite loop."""
        while True:
            with console.screen():
                self.setup()
            if self.suppress_prints:
                with contextlib.redirect_stdout(None):
                    self.run_simulation()
            else:
                self.run_simulation()
            self.play_animation()

    def setup(self) -> None:
        """Set up a new simulation."""
        match self.menu():
            case Maybe.empty:
                console.print("Thank you for playing. Bye!")
                sys.exit()
            case Some(scene):
                self.scenario = scene
        console.print(f"Running {self.scenario.name}:")
        self.scenario.sim.setup()

    def run_simulation(self) -> None:
        """Run the simulation."""
        self.scenario.sim.run_simulation()

    def play_animation(self) -> None:
        """Re-create the simulation by animating the trace of the objects."""
        self.scenario.sim.play_animation((self.save, self.save_as), trace=self.trace)

    def _adjust_settings(self) -> None:
        self.trace = Confirm.ask("Do you want to plot the trace of each object?")
        self.suppress_prints = Confirm.ask(
            "Would you like to override the printing done by simulation scenarios?"
        )
        self.save = Confirm.ask("Do you want to save the animation?")

    def _selection_menu(self) -> str:
        console.print(self.menu_items, markup=True)
        return Prompt.ask(
            "Choose simulation or option from the list above by typing in the"
            " corresponding character: ",
            choices=["q", "s", *self.options],
        )

    def menu(self) -> Maybe[Scenario]:
        """List all available simulations."""
        while (ans := self._selection_menu()) not in ["q", *self.options]:
            match ans:
                case "s":
                    self._adjust_settings()
                case _:
                    pass

        return Nothing if ans.lower() == "q" else Some(self.scenarios[int(ans) - 1])


def main() -> None:
    """Run the main program."""
    sim = Sim()
    sim.loop()


if __name__ == "__main__":
    main()
