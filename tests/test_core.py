import pytest
import unittest

from datetime import date, timedelta
import copy

from tests.conftest import frostbite, ember, stardust, tinsel, populated_stable
from mythical_stable.core import MissionRecord, Stable, StableIterator

"""
    Creatures
"""
def test_dragon_mission_duration_days(frostbite) -> None:
    """ Dragon.mission_duration_days() returns 14 """
    assert frostbite.mission_duration_days() == 14 # should be 14

def test_phoenix_mission_duration_days(ember) -> None:
    """Phoenix.mission_duration_days() returns 7"""
    assert ember.mission_duration_days() == 7

def test_unicorn_mission_duration_days(stardust) -> None:
    """Unicorn.mission_duration_days() returns 3"""
    assert stardust.mission_duration_days() == 3

def test_unicorn_send_on_mission_low_power(tinsel) -> None:
    """Unicorn.send_on_mission() raises RuntimeError when power_level < 50"""
    # with pytest.raises(RuntimeError, match = "A unicorn with a power level under 50 cannot be sent alone on mission"):
    with pytest.raises(RuntimeError):
        tinsel.send_on_mission()

def test_unicorn_send_on_mission_high_power(stardust) -> None:
    """Unicorn.send_on_mission() succeeds when power_level >= 50"""
    stardust.send_on_mission()
    assert stardust._in_stable == False

def test_phoenix_resurrect(ember)->None:
    """Phoenix.resurrect() increments resurrection_count"""
    before = ember.resurrection_count
    ember.resurrect()
    assert ember.resurrection_count == before + 1

def test_creature_power_level_value(frostbite)->None:
    """power_level setter raises TypeError for not integer"""
    with pytest.raises(ValueError, match = r".*must be between 0 and 100.*"):
        frostbite.power_level = 101

def test_creature_power_level_type(frostbite)->None:
    """power_level setter raises ValueError for out-of-range values"""
    with pytest.raises(ValueError, match = r".*must be a number.*"):
        frostbite.power_level = "str"

"""
    MissionRecord
"""
def test_mission_record_return_date(frostbite):
    """return_date = departure_date + timedelta(days=duration_days)"""
    mr = MissionRecord(creature_name=frostbite.name,
                       destination="Whatever",
                       departure_date=date.today(),
                       duration_days=frostbite.mission_duration_days())
    assert mr.return_date == mr.departure_date + timedelta(days=mr.duration_days)

def test_mission_record_equality(frostbite):
    """Two records with same creature_name + departure_date are equal"""
    mr1 = MissionRecord(creature_name=frostbite.name,
                        destination="Whatever",
                        departure_date=date.today(),
                        duration_days=frostbite.mission_duration_days())

    mr2 = MissionRecord(creature_name=frostbite.name,
                        destination="Whatever",
                        departure_date=date.today(),
                        duration_days=frostbite.mission_duration_days())
    assert mr1 == mr2

def test_mission_record_hash(frostbite):
    """Two records with same creature_name + departure_date have the same hash"""
    mr1 = MissionRecord(creature_name=frostbite.name,
                        destination="Whatever",
                        departure_date=date.today(),
                        duration_days=frostbite.mission_duration_days())
    mr2 = MissionRecord(creature_name=frostbite.name,
                        destination="Whatever",
                        departure_date=date.today(),
                        duration_days=frostbite.mission_duration_days())
    assert hash(mr1) == hash(mr2)

def test_mission_record_post_init_empty_destination(frostbite):
    """__post_init__ raises ValueError for empty destination"""
    with pytest.raises(ValueError, match = r".*not be empty.*"):
        mr = MissionRecord(creature_name=frostbite.name,
                           destination="",
                           departure_date=date.today(),
                           duration_days=frostbite.mission_duration_days())

def test_mission_record_post_init_positive_duration(frostbite):
    """__post_init__ raises ValueError for non-positive duration_days"""
    with pytest.raises(ValueError, match = r".*positive integer.*"):
        mr = MissionRecord(creature_name=frostbite.name,
                           destination="Whatever",
                           departure_date=date.today(),
                           duration_days=-1)


def test_mission_record_is_overdue_active_past(frostbite):
    """is_overdue is True only when active and return_date is in the past"""
    mr = MissionRecord(creature_name=frostbite.name,
                       destination="Whatever",
                       departure_date=date(2026,5, 1),
                       duration_days=frostbite.mission_duration_days())
    active = mr._active
    past = (mr.return_date < date.today())
    active_and__past = active and past
    assert active_and__past and mr.is_overdue

def test_mission_record_is_overdue_close(frostbite):
    """is_overdue is False after close()"""
    mr = MissionRecord(creature_name=frostbite.name,
                       destination="Whatever",
                       departure_date=date(2026,5, 1),
                       duration_days=frostbite.mission_duration_days())
    mr.close()
    assert not mr.is_overdue


"""
Stable
"""
def test_stable_creature_same_name(populated_stable, stardust):
    """add() raises ValueError when a creature with the same name is added twice"""
    with pytest.raises(ValueError, match = r".*is already registered.*"):
        populated_stable.add(stardust)

def test_stable_remove_unknown(populated_stable, tinsel):
    """remove() raises KeyError for an unknown name"""
    with pytest.raises(KeyError):
        populated_stable.remove(tinsel.name)

def test_stable_contains_registered(populated_stable, frostbite):
    """__contains__ returns True for a registered creature's name"""
    assert populated_stable.__contains__(frostbite.name)

def test_stable_len_remove(populated_stable, frostbite):
    """__len__ returns the correct count after remove"""
    length = populated_stable.__len__()
    populated_stable.remove(frostbite.name)
    assert length == populated_stable.__len__() + 1

def test_stable_len_add(populated_stable, tinsel):
    """__len__ returns the correct count after add"""
    length = populated_stable.__len__()
    populated_stable.add(tinsel)
    assert length == populated_stable.__len__() - 1

def test_stable_iter(populated_stable):
    """__iter__ iterates over all creatures"""
    creature_iter = iter(populated_stable)
    for item in range(len(populated_stable)):
        next(creature_iter)
    with pytest.raises(StopIteration):
        next(creature_iter)

def test_stable_available_by_power(populated_stable, frostbite, ember, stardust):
    """available_by_power() only returns in-stable creatures, in descending power order"""
    l = [[c.power_level, c.name] for c in populated_stable._creatures if c._in_stable]
    l.sort(reverse = True)
    si = populated_stable.available_by_power()
    for index in range(len(populated_stable._creatures)):
        assert l[index][1] == next(si).name
