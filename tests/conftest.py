import pytest
from mythical_stable.core import Dragon, Phoenix, Unicorn, Stable


def pytest_runtest_logstart(nodeid, location):
    """
    Completely silences pytest's default behavior of writing the
    technical function name at the start of each test line.
    """
    pass


def pytest_itemcollected(item):
    """
    Modifies the test identifier as soon as pytest discovers it.
    This prevents pytest from printing the technical function name at the start.
    """
    if item.obj and item.obj.__doc__:
        # Extract the first line of the docstring cleanly
        doc = item.obj.__doc__.strip().split("\n")[0].strip()

        # Rewrite the nodeid completely at the collection stage
        item._nodeid = f"{item.fspath.basename} :: {doc}"

@pytest.fixture
def frostbite():
    return Dragon("Frostbite", "Nordic Realms", 95, element="ice")

@pytest.fixture
def ember():
    return Phoenix("Ember", "Ashlands", 80)

@pytest.fixture
def stardust():
    return Unicorn("Stardust", "Silver Meadows", 72)

@pytest.fixture
def tinsel():
    return Unicorn("Tinsel", "Soft Glades", 30)

@pytest.fixture
def populated_stable(frostbite, ember, stardust):
    s = Stable()
    s.add(frostbite)
    s.add(stardust)
    s.add(ember)
    return s