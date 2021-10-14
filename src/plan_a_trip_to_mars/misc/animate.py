"""Functions that animate.

Class from https://stackoverflow.com/questions/9401658/how-to-animate-a-scatter-plot,
modified to accept input.
"""
from itertools import cycle

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

import plan_a_trip_to_mars.config as cf


class AnimatedScatter:
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""

    def __init__(self, args):
        self.show_trace = False
        self.numpoints = len(args)
        self.points = args
        self.names = [obj.name for obj in self.points]
        self.prepeare_data()
        self.stream = self.data_stream()

        # Set-up the figure and axes...
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.ax.set_facecolor("k")
        # Then set-up FuncAnimation.
        self.ani = animation.FuncAnimation(
            self.fig, self.update, interval=5, init_func=self.setup_plot, blit=True
        )

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        x, y, s, c = next(self.stream).T

        # Draw all objects as a scatter plot
        self.scat = self.ax.scatter(
            x, y, c=c, s=s, vmin=0, vmax=1, cmap="jet", edgecolor="w"
        )
        # Draw their trace
        if self.show_trace:
            for j, (x_, y_) in enumerate(zip(x, y)):
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
        self.ax.axis([-cf.SIZE, cf.SIZE, -cf.SIZE, cf.SIZE])

        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        returns = [self.scat]
        if self.show_trace:
            for j in range(len(x)):
                returns.append(getattr(self, f"line_{j}"))
        return returns + self.txt

    def prepeare_data(self):
        """Prepare data for the data stream.

        A list is filled with iterator objects, such that calling next on one of them
        reveal the next point in the trace that should be drawn on screen.
        """
        self.p_list = []
        for obj in self.points:
            self.p_list.append(cycle(obj.trace))

    def data_stream(self):
        s, c = np.random.random((self.numpoints, 2)).T
        while True:
            xy = np.array([next(pair) for pair in self.p_list])
            s = 0.1 * np.ones_like(xy[:, 0])
            c += 0.02 * (np.random.random(self.numpoints) - 0.5)
            yield np.c_[xy[:, 0], xy[:, 1], s, c]

    def update(self, i):
        """Update the scatter plot."""
        data = next(self.stream)

        # Set x and y data ...
        self.scat.set_offsets(data[:, :2])
        # Set sizes ...
        self.scat.set_sizes(300 * abs(data[:, 2]) ** 1.5 + 100)
        # Set colours ...
        self.scat.set_array(data[:, 3])

        # Draw traces ...
        if self.show_trace:
            for j, obj in enumerate(self.points):
                xs = [x[0] for x in obj.trace[: i + 1]]
                ys = [y[1] for y in obj.trace[: i + 1]]
                line = getattr(self, f"line_{j}")
                line.set_xdata(xs)
                line.set_ydata(ys)

        # Set text position and update simulation time ...
        for txt, x, y in zip(self.txt[1:], data[:, 0], data[:, 1]):
            txt.set_position((x, y))
        self.txt[0].set_text(f"Time = {i % cf.TOT_TIME * cf.FPS}")

        # We need to return the updated artists for FuncAnimation to draw. Note that it
        # expects a sequence of artists, so if we only had one artist we would add a
        # trailing comma:
        # return [self.scat,]
        returns = [self.scat]
        if self.show_trace:
            for j in range(len(self.points)):
                returns.append(getattr(self, f"line_{j}"))
        return returns + self.txt
