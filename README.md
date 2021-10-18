# :rocket: Plan A Trip To Mars :rocket:

## Install

With `poetry`:

```sh
poetry install
```

and run with:

```sh
poetry run plan-a-trip-to-mars
```

Without `poetry` (using `pip`):

```sh
python -m pip install -e .
```

and run with:

```sh
plan-a-trip-to-mars
```

## TODO

Things I can change so it become more challenging:

- Change time scale (FPS)
- Move planets and/or change their velocities to be off
- Git the rocket many arbitrary kicks

## Problems

### 1

Use the simulation to obtain a reasonable value for the amount of days between two Mars
oppositions, that is, the amount of days that passes between two occasions that Earth and
Mars are aligned with the Sun.

### 2

Calculate the velocity needed for a rocket to travel from Earth to Mars on a Hohmann
transfer orbit. (Hint: We already did this in an exercise a few weeks ago.)

### 3

Using the program, obtain a reasonable number for the amount of days it takes for the
rocket to complete the transfer orbit, i.e. the amount of days until it arrives on Mars.

### 4

How much must the velocity of the rocket increase upon arrival at Mars if it were to
follow the same orbit? Confirm by giving the rocket a `kick` on the day arrival and see
that the rocket and Mars move as a pair.

### 5

If the rocket missed a bit on the timing of the transfer orbit and is on Mars's orbit, but
some distance behind, how would you adjust its velocity so that it overtakes Mars?
Explain.

### 6

A rocket sits on a circular path, when a sudden impact in the radial direction sends it on
a parabolic path. Find the velocity needed, and the closest point the rocket will come to
the object it originally orbited.
