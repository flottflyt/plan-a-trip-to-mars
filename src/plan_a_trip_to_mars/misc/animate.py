"""Functions that anumate.

Class from https://stackoverflow.com/questions/9401658/how-to-animate-a-scatter-plot,
modified to accept input.
"""
from itertools import cycle

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

import plan_a_trip_to_mars.config as cf


class AnimatedScatter(object):
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""

    def __init__(self, args):
        self.numpoints = len(args)
        self.points = args
        self.names = [obj.name for obj in self.points]
        self.prepeare_data()
        self.stream = self.data_stream()

        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(
            self.fig, self.update, interval=5, init_func=self.setup_plot, blit=True
        )

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        x, y, s, c = next(self.stream).T

        self.scat = self.ax.scatter(
            x, y, c=c, s=s, vmin=0, vmax=1, cmap="jet", edgecolor="k"
        )
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
        for i, n in enumerate(self.names):
            setattr(
                self, f"txt_{i}", self.ax.text(x[i], y[i], n, va="bottom", ha="center")
            )
            self.txt.append(getattr(self, f"txt_{i}"))
        self.ax.axis([-cf.SIZE, cf.SIZE, -cf.SIZE, cf.SIZE])
        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        return [self.scat] + self.txt

    def prepeare_data(self):
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

        # Set x and y data...
        self.scat.set_offsets(data[:, :2])
        # Set sizes...
        self.scat.set_sizes(300 * abs(data[:, 2]) ** 1.5 + 100)
        # Set colors..
        self.scat.set_array(data[:, 3])

        # Set text position ...
        for txt, x, y in zip(self.txt[1:], data[:, 0], data[:, 1]):
            txt.set_position((x, y))

        self.txt[0].set_text(f"Time = {i % cf.TOT_TIME}")

        # We need to return the updated artist for FuncAnimation to draw..
        # Note that it expects a sequence of artists, thus the trailing comma.
        # return (self.scat,self.txt)
        return [self.scat] + self.txt


if __name__ == "__main__":
    a = AnimatedScatter()
    plt.show()

# enter image description here

# import  matplotlib.pyplot as plt

# def plt_anim(*args):
#     # w, x, y = extra_data()
#     # with np.load("docs/assets/video_data_ions_vectorized.npz", mmap_mode="r") as f:
#     #     w = f["w"]
#     #     x = f["x_ax"]
#     #     y = f["y_ax"]
#     # if x.shape[0] != y.shape[0]:
#     #     y = y.T

#     fig, ax = plt.subplots(figsize=(12, 6))
#     # Electrons
#     # ax.set(xlim=(-1e-6, 6e-6), ylim=(-1.1, 1.1))
#     # ax.set(xlim=(- 1e-5, 1.6e-4), ylim=(-1.1, 1.1))
#     # Ions
#     # ax.set(xlim=(-2e-6, 1e-5), ylim=(-1.1, 1.1))
#     # ax.set(xlim=(- 1e-5, 1.6e-4), ylim=(-1.1, 1.1))
#     # inityr = np.real(y[:, 0])
#     # inityi = np.imag(y[:, 0])
#     lines = []
#     for obj in args:
#         x = [i[0] for i in obj.trace]
#         y = [i[1] for i in obj.trace]
#         lines.append(
#             ax.plot(x, y, "r--", lw=0.7, label="Real")[0]
#         )
#     # line1 = ax.plot(x, inityr, "r--", lw=0.7, label="Real")[0]
#     # line2 = ax.plot(x, inityi, "b--", lw=0.7, label="Imag")[0]
#     ax.legend()

#     def draw(frame, add_colorbar):
#         y_ = y[:, frame]
#         y_r = np.real(y_)
#         y_i = np.imag(y_)
#         line1.set_ydata(y_r)
#         line2.set_ydata(y_i)
#         # f = w[frame] / (2 * np.pi)
#         # title = f"f = {f:.2e}"
#         # ax.set_title(title)
#         return ax

#     def init():
#         return draw(0, add_colorbar=True)

#     def animate(frame):
#         return draw(frame, add_colorbar=False)

#     frames = len(w)

#     ani = animation.FuncAnimation(
#         fig, animate, frames, interval=100, init_func=None, repeat=False
#     )
#     plt.show()
#     # if save:
#     #     ani.save("video_ions_zoom.mp4", writer=animation.FFMpegWriter(fps=60), dpi=400)
#     plt.close(fig)
