"""
mythical_stable.patterns.strategies
=====================================
Strategy pattern — pluggable sort algorithms for the Stable.

The SortStrategy Protocol is defined in mythical_stable.protocols. Each class
here satisfies it structurally (no inheritance required). New sorting behaviours
can be added by creating a new class with a sort() method — the Stable.sorted()
call site requires zero changes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mythical_stable.core.creatures import Creature


class SortByPower:
    """Sort creatures by power_level descending (strongest first)."""

    def sort(self, creatures: list["Creature"]) -> list["Creature"]:
        """Return creatures ordered from highest to lowest power_level."""
        return sorted(creatures, key=lambda c: c.power_level, reverse=True)


class SortByName:
    """Sort creatures alphabetically by name."""

    def sort(self, creatures: list["Creature"]) -> list["Creature"]:
        """Return creatures in alphabetical name order."""
        return sorted(creatures, key=lambda c: c.name)


class SortByAvailability:
    """Sort in-stable creatures first, then those on missions, then by name."""

    def sort(self, creatures: list["Creature"]) -> list["Creature"]:
        """Return in-stable creatures before on-mission creatures."""
        return sorted(creatures, key=lambda c: (not c._in_stable, c.name))