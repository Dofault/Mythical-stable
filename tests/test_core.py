import pytest

def test_dragon_mission_duration_days(frostbite) -> None:
    assert frostbite.mission_duration_days() == 14

def test_phoenix_mission_duration_days(ember) -> None:
    assert ember.mission_duration_days() == 7

def test_unicorn_mission_duration_days(stardust) -> None:
    assert stardust.mission_duration_days() == 3

def test_unicorn_send_on_mission_low_power(tinsel) -> None:
    with pytest.raises(RuntimeError, match = "A unicorn with a power level under 50 cannot be sent alone on mission"):
        tinsel.send_on_mission()

def test_unicorn_send_on_mission_high_power(stardust) -> None:
    tinsel.send_on_mission()
    assert stardust._in_Stable == False

def test_phoenix_resurrect(ember):
    before = ember.resurrection_count
    ember.resurrect()
    assert ember.resurrection_count == before + 1


Phoenix.resurrect() increments resurrection_count
power_level setter raises ValueError for out-of-range values