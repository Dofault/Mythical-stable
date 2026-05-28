"""Mythical creature classes for the stable package."""

from __future__ import annotations
from abc import ABC, abstractmethod


class Creature(ABC):
    """Abstract base class for all mythical creatures."""

    def __init__(self, name: str, origin: str, power_level: int) -> None:
        """Initialise a creature with a name, origin, and power level."""
        self.name = name
        self.origin = origin
        self._power_level = None
        self.power_level = power_level  # triggers validation via setter
        self.on_mission: bool = False

    @property
    def power_level(self) -> int:
        """Return the creature's power level (0–100)."""
        return self._power_level

    @power_level.setter
    def power_level(self, value: int) -> None:
        """Set the power level, raising ValueError if out of range 0–100."""
        if not 0 <= value <= 100:
            raise ValueError(f"power_level must be between 0 and 100, got {value}")
        self._power_level = value

    @abstractmethod
    def mission_duration_days(self) -> int:
        """Return the default mission duration in days for this creature type."""
        ...

    def send_on_mission(self) -> None:
        """Mark the creature as on a mission."""
        self.on_mission = True

    def return_to_stable(self) -> None:
        """Mark the creature as back in the stable."""
        self.on_mission = False

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return f"{self.__class__.__name__}(name={self.name!r}, power_level={self.power_level})"


class Dragon(Creature):
    """A fire-breathing creature capable of long-distance missions."""

    def __init__(self, name: str, origin: str, power_level: int, element: str = "fire") -> None:
        """Initialise a Dragon with an optional elemental affinity."""
        super().__init__(name, origin, power_level)
        self.element = element

    def mission_duration_days(self) -> int:
        """Return 14 — dragons take two weeks per mission."""
        return 14


class Phoenix(Creature):
    """A reborn bird creature that can resurrect after defeat."""

    def __init__(self, name: str, origin: str, power_level: int) -> None:
        """Initialise a Phoenix with a resurrection counter starting at zero."""
        super().__init__(name, origin, power_level)
        self.resurrection_count: int = 0

    def mission_duration_days(self) -> int:
        """Return 7 — phoenixes complete missions in one week."""
        return 7

    def resurrect(self) -> None:
        """Increment the resurrection count by one."""
        self.resurrection_count += 1


class Unicorn(Creature):
    """A graceful horned creature that requires minimum power to go on missions."""

    def mission_duration_days(self) -> int:
        """Return 3 — unicorns complete short missions in three days."""
        return 3

    def send_on_mission(self) -> None:
        """Send the unicorn on a mission, raising RuntimeError if power_level < 50."""
        if self.power_level < 50:
            raise RuntimeError(
                f"{self.name} needs power_level >= 50 to go on a mission "
                f"(current: {self.power_level})"
            )
        super().send_on_mission()