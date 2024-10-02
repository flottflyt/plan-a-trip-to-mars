"""Functions that animate.

Class from https://stackoverflow.com/questions/9401658/how-to-animate-a-scatter-plot,
modified to accept input.
"""

from collections.abc import Generator
from dataclasses import dataclass
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.collections import PathCollection
from matplotlib.text import Text

import plan_a_trip_to_mars.config as cf
from plan_a_trip_to_mars.universe import Planet, Rocket


@dataclass
class SimulationConstants:
    """Container for all constants needed during simulation.

    All times are with respect to seconds.

    Attributes
    ----------
    size : float
        The width and height of the universe.
    fps : int
        The number of frames-per-second. Useful to speed up the simulation.
    total_time : float
        The total time the simulation should run.
    time_scale : float
        Scale the time so that it is presented in a different unit, for example going
        from seconds to days would be `3600 * 24`.
    unit : str
        The time unit, for example year, second, day, etc.
    """

    size: float = 3 * cf.AU
    fps: int = 24
    total_time: float = 5e4
    time_scale: float = 1
    unit: str = ""


class AnimatedScatter:
    """An animated scatter plot using matplotlib.animations.FuncAnimation.

    Parameters
    ----------
    objs : list[Planet | Rocket]
        List of Planets and/or Rockets.
    simulation_constants : SimulationConstants
    """

    def __init__(
        self,
        objs: list[Planet | Rocket],
        simulation_constants: SimulationConstants,
        # fps: int,
        # tot_time: float,
        # size: float,
        # time_scale: float,
        # unit: str,
    ) -> None:
        self.sim_consts = simulation_constants
        # self.fps = fps
        # self.tot_time = tot_time
        # self.size = size
        # self.time_scale = time_scale
        # self.unit = unit
        self.show_trace = False
        self.num_objs = len(objs)
        self.num_pts = cycle(np.arange(len(objs[0].trace)))
        self.points = objs
        self.names = [obj.name for obj in self.points]
        self.prepeare_data()
        self.stream = self.data_stream()

        # Set-up the figure and axes...
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.ax.set_facecolor("k")
        self.ax.set_xlabel("Meter")
        self.ax.set_ylabel("Meter")
        # Then set-up `FuncAnimation`. This is where the methods below are sent. Once an
        # instance of `FuncAnimation` is made (and therefore also when an instance of this
        # class, `AnimatedScatter`, is made) the animation is generated and played in a
        # loop.
        self.ani = animation.FuncAnimation(
            self.fig,
            self.update,
            interval=5,
            init_func=self.setup_plot,
            blit=True,
            save_count=int(self.sim_consts.total_time / self.sim_consts.fps),
        )

    def setup_plot(self) -> list[PathCollection | Text]:
        """Make the initial drawing of the scatter plot."""
        # x, y, s, c = next(self.stream).T
        data, _ = next(self.stream)
        x, y, s, c = data.T

        # Draw all objects as a scatter plot
        self.scat = self.ax.scatter(
            x, y, c=c, s=s, vmin=0, vmax=1, cmap="jet", edgecolor="w"
        )
        # Draw their trace
        if self.show_trace:
            self.traces = []
            for j, (x_, y_) in enumerate(zip(x, y, strict=False)):
                self.traces.append(np.array([x_, y_]))
                setattr(self, f"line_{j}", self.ax.plot(x_, y_)[0])
        # Add text that display the simulation time
        self.txt = [
            self.ax.text(
                0.01,
                0.95,
                "",
                bbox={"facecolor": "w", "alpha": 0.5, "pad": 5},
                transform=self.ax.transAxes,
                ha="left",
            )
        ]
        # Add text that show the name of each object
        for j, n in enumerate(self.names):
            setattr(
                self,
                f"txt_{j}",
                self.ax.text(x[j], y[j], n, va="bottom", ha="center", c="w"),
            )
            self.txt.append(getattr(self, f"txt_{j}"))
        # Define simulation area
        self.ax.axis(
            (
                -self.sim_consts.size,
                self.sim_consts.size,
                -self.sim_consts.size,
                self.sim_consts.size,
            )
        )

        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        returns = [self.scat]
        if self.show_trace:
            returns.extend(getattr(self, f"line_{j}") for j in range(len(x)))
        return [*returns, *self.txt]

    def prepeare_data(self) -> None:
        """Prepare data for the data stream.

        A list is filled with iterator objects, such that calling next on one of them
        reveal the next point in the trace that should be drawn on screen.
        """
        self.p_list: list[cycle[tuple[float, float]]] = []
        self.p_list.extend(cycle(obj.trace) for obj in self.points)

    def data_stream(self) -> Generator[tuple[np.ndarray, np.ndarray]]:
        """Create the data stream that should be animated."""
        s, c = np.random.default_rng().random((self.num_objs, 2)).T
        while True:
            xy = np.array([next(pair) for pair in self.p_list])
            s = 0.1 * np.ones_like(xy[:, 0])
            c += 0.02 * (np.random.default_rng().random(self.num_objs) - 0.5)
            yield np.c_[xy[:, 0], xy[:, 1], s, c], next(self.num_pts)

    def update(self, _: int) -> list[PathCollection | Text]:
        """Update the scatter plot."""
        data, idx = next(self.stream)
        # Set x and y data ...
        self.scat.set_offsets(data[:, :2])
        # Set sizes ...
        self.scat.set_sizes(300 * abs(data[:, 2]) ** 1.5 + 100)
        # Set colours ...
        self.scat.set_array(data[:, 3])
        # Draw traces ...
        if self.show_trace:
            # If we are back to the first time step, re-set the trace list.
            if idx == 0:
                self.traces = []
                self.traces.extend(
                    np.array([x_, y_])
                    for x_, y_ in zip(data[:, 0], data[:, 1], strict=False)
                )
            # Otherwise, append the new positions to the trace.
            else:
                for j, (t, (x_, y_)) in enumerate(
                    zip(self.traces, data[:, :2], strict=False)
                ):
                    self.traces[j] = np.c_[t, np.array([x_, y_])]
                    line = getattr(self, f"line_{j}")
                    line.set_data(self.traces[j][0, :], self.traces[j][1, :])
        # Set text position and update simulation time ...
        for txt, x, y in zip(self.txt[1:], data[:, 0], data[:, 1], strict=False):
            txt.set_position((x, y))
        self.txt[0].set_text(
            f"Time = {int(idx / self.sim_consts.time_scale)}{self.sim_consts.unit}"
        )

        # We need to return the updated artists for FuncAnimation to draw. Note that it
        # expects a sequence of artists, so if we only had one artist we would add a
        # trailing comma:
        # return [self.scat,]
        returns = [self.scat]
        if self.show_trace:
            returns.extend(getattr(self, f"line_{j}") for j in range(len(self.points)))
        return [*returns, *self.txt]
