# :rocket: Plan A Trip To Mars :rocket:

![](assets/animation.gif)

## Problems

### 1

Use the simulation to obtain a reasonable value for the amount of days between two Mars
oppositions, that is, the amount of days that passes between two occasions that Earth
and Mars are aligned with the Sun.

### 2

Calculate the velocity needed for a rocket to travel from Earth to Mars on a Hohmann
transfer orbit, i.e., the relative velocity with respect to Earth. (Hint: We already did
this in an exercise a few weeks ago.)

### 3

Using the program, obtain a reasonable number for the amount of days it takes for the
rocket to complete the transfer orbit, i.e., the amount of days until it arrives at
Mars. You should use your answer from problem 1 to place Earth in Mars in a good
position for the transfer orbit.

### 4

How much must the velocity of the rocket increase upon arrival at Mars if it were to
follow the same orbit? Confirm by giving the rocket a `kick` on the day of arrival and
confirm that the rocket and Mars move as a pair.

### 5

If the rocket missed somewhat on the timing of the transfer orbit and is on Mars's orbit,
but some distance behind, how would you adjust its velocity so that it overtakes Mars?
Explain.

### 6

A rocket sits on a circular trajectory, when a sudden impact in the radial direction
sends it on a parabolic trajectory. Find the velocity needed to get it on a parabolic
trajectory, and the closest point the parabolic trajectory will have to the centre
object.

## Install

### Poetry

This project is packaged with [Poetry]. Install via their website at
[https://python-poetry.org/docs/master/#installation](https://python-poetry.org/docs/master/#installation).

_If_ you cannot get the installation of poetry using the above links to work, a last
resort is to install from PyPI via `pip`:

```bash
pip install --user poetry
```

### Package `plan-a-trip-to-mars`

Clone the repository and `cd` into it:

```bash
git clone <repo-url>
cd plan-a-trip-to-mars
```

Then you can use poetry to install the whole project:

```bash
poetry install
```

You will now be able to run the python code! This can be done in two ways; either
prepend `poetry run` to all commands (this makes sure the python code is run in the
correct way, in the correct environment):

```bash
# Option 1
poetry run plan-a-trip-to-mars
poetry run python src/plan_a_trip_to_mars/simulation.py
```

Alternatively you can start the virtual environment with `poetry shell` and run the
program like you normally would:

```bash
# Option 2
poetry shell
plan-a-trip-to-mars
python src/plan_a_trip_to_mars/simulation.py
```

<details>
<summary>Notes on virtual environments</summary>

When working on a python project, the best practice is to work inside a virtual
environment. This can be confusing to begin with, but the pros massively outweighs the
cons. Many programs exist the creates and manages virtual environments, Poetry will
actually do this automatically for you!

Other good alternatives that makes this easier is [pyenv] and [virtualenvwrapper]. Pick
your favourite and learn how to use it.

</details>

## Usage

### Scenario constants

Five scenario constants exists:

- `SIZE`: The length of the sides of the simulation, in metres.
- `TOT_TIME`: The total time of the simulation, in units of `spi`. That is, changing the
  `spi` will change the unit of the total time (e.g. seconds to hours). This value
  decides how many iterations the simulation will use.
- `FPS`: The frame rate of the animation. After the simulation has been calculated, only
  every `n`-th iteration is used (for `FPS=n`). Useful if you need high temporal
  resolution, but a faster simulation.
- `TIME_SCALE`: The clock shown in the animation is divided by `TIME_SCALE`, effectively
  changing the time unit.
- `UNIT`: Add a time unit to the simulation clock.

### `Universe().set_spi()`

The `spi` decides how many seconds pass per iteration (seconds-per-iteration). By
default, everything is calculated using SI units, meaning seconds for time. This quickly
become computationally expensive when you want to simulate a solar system. Setting the
`spi` to `3600` will instead update all positions, velocities, etc. every hour. Be
careful to also change the timing of events; the time of a rocket's `kick` is now
specified in hours.

[poetry]: https://python-poetry.org
[virtualenvwrapper]: https://virtualenvwrapper.readthedocs.io/en/latest/
[pyenv]: https://github.com/pyenv/pyenv
