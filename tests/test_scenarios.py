"""Tests for the implemented scenarios."""

import inspect

import plan_a_trip_to_mars.scenarios as s


def test_instantiate() -> None:
    """Test that all scenarios inherit from `BigScenario`."""
    for n, c in inspect.getmembers(s, inspect.isclass):
        if c.__module__ == "plan_a_trip_to_mars.scenarios" and n != "BigScenario":
            c()
            assert issubclass(c, s.BigScenario)  # noqa: S101


if __name__ == "__main__":
    test_instantiate()
