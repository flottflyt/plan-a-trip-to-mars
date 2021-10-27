# :rocket: Plan A Trip To Mars :rocket:

![](assets/animation.gif)

## Problems

### 1

Use the simulation to obtain a reasonable value for the amount of days between two Mars
oppositions, that is, the amount of days that passes between two occasions that Earth and
Mars are aligned with the Sun.

### 2

Calculate the velocity needed for a rocket to travel from Earth to Mars on a Hohmann
transfer orbit, i.e. the relative velocity with respect to Earth. (Hint: We already did
this in an exercise a few weeks ago.)

### 3

Using the program, obtain a reasonable number for the amount of days it takes for the
rocket to complete the transfer orbit, i.e. the amount of days until it arrives on Mars.
You should use your answer from problem 1 to place Earth in Mars in a good position for
the transfer orbit.

### 4

How much must the velocity of the rocket increase upon arrival at Mars if it were to
follow the same orbit? Confirm by giving the rocket a `kick` on the day of arrival and
confirm that the rocket and Mars move as a pair.

### 5

If the rocket missed a bit on the timing of the transfer orbit and is on Mars's orbit, but
some distance behind, how would you adjust its velocity so that it overtakes Mars?
Explain.

### 6

A rocket sits on a circular trajectory, when a sudden impact in the radial direction sends
it on a parabolic trajectory. Find the velocity needed to get it on a parabolic
trajectory, and the closest point the parabolic trajectory will have to the centre object.

## Install

### Pyenv and poetry

#### For virtual environments

To install `pyenv`, see their github repos,
[here](https://github.com/pyenv/pyenv#installation) and/or
[here](https://github.com/pyenv/pyenv-installer), for a detailed guide.

Another project that takes care of virtual environments in a nice way is
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). And even more
than these two examples exists.

#### For python packaging

[`poetry`](https://python-poetry.org/docs/master/#installation) is simpler, you just do:

```sh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Package `plan-a-trip-to-mars`

Clone the repository and `cd` into it:

```sh
git clone <repo-url>
cd plan-a-trip-to-mars
```

#### With `poetry`

It is always useful to use a virtual environment for a new python project, for example
`pyenv`. If you install using `poetry` and a virtual environment is not activated,
`poetry` will set one up and install into it. If an environment is activated, `poetry`
will notice and install into this. In either case, do:

```sh
poetry install
```

and run with:

```sh
poetry run plan-a-trip-to-mars
poetry run python src/plan_a_trip_to_mars/simulation.py
```

Alternatively you can start the virtual environment with `poetry shell` and run the
program like you normally would:

```sh
plan-a-trip-to-mars
python src/plan_a_trip_to_mars/simulation.py
```

#### Without `poetry` (using `pip`):

If you do not want to use `poetry`, a second option is to install with the `setup.py`
script. This will install into a virtual environment if one is already activated, or to
your global python version if no virtual environment is activated. In either case, do:

```sh
python setup.py install
```

and run with:

```sh
plan-a-trip-to-mars
python src/plan_a_trip_to_mars/simulation.py
```

## Usage

### Scenario constants

There are five scenario constants:

-   `SIZE`: The length of the sides of the simulation, in metres.
-   `TOT_TIME`: The total time of the simulation, in units of `spi`. That is, changing
    the `spi` will change the unit of the total time (e.g. seconds to hours). This value
    decides how many iterations the simulation will use.
-   `FPS`: The frame rate of the animation. After the simulation has been calculated,
    only every `n`-th iteration is used (for `FPS=n`). Useful if you need high temporal
    resolution, but a faster simulation.
-   `TIME_SCALE`: The clock shown in the animation is divided by `TIME_SCALE`,
    effectively changing the time unit.
-   `UNIT`: Add a time unit to the simulation clock.

### `Universe().set_spi()`

The `spi` decides how many seconds pass per iteration (seconds-per-iteration). By default,
everything is calculated using SI units, meaning seconds for time. This quickly become
computationally expensive when you want to simulate a solar system. Setting the `spi` to
`3600` will instead update all positions, velocities, etc. every hour. Be careful to also
change the timing of events; the time of a rocket's `kick` is now specified in hours.
