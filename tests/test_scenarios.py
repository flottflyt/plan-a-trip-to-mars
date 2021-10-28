import inspect

import plan_a_trip_to_mars.scenarios as s


def test_instantiate():
    for n, c in inspect.getmembers(s, inspect.isclass):
        if c.__module__ == "plan_a_trip_to_mars.scenarios":
            if n != "BigScenario":
                c()
                assert issubclass(c, s.BigScenario)


if __name__ == "__main__":
    test_instantiate()
