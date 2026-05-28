"""Stable container holding mythical creatures."""

from __future__ import annotations
from typing import Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    from .creatures import Creature
    from mythical_stable.protocols import SortStrategy


class StableIterator:
    """Iterator that walks through a snapshot of creatures in the stable."""

    def __init__(self, creatures: list[Creature]) -> None:
        """Initialise the iterator with a list of creatures."""
        self._creatures = creatures
        self._index = 0

    def __iter__(self) -> StableIterator:
        """Return self as the iterator."""
        return self

    def __next__(self) -> Creature:
        """Return the next creature, raising StopIteration when exhausted."""
        if self._index >= len(self._creatures):
            raise StopIteration
        creature = self._creatures[self._index]
        self._index += 1
        return creature


class Stable:
    """A container that manages a collection of mythical creatures."""

    def __init__(self) -> None:
        """Initialise an empty stable."""
        self._creatures: dict[str, Creature] = {}

    def add(self, creature: Creature) -> None:
        """Add a creature to the stable, raising ValueError if the name already exists."""
        if creature.name in self._creatures:
            raise ValueError(f"A creature named {creature.name!r} is already in the stable")
        self._creatures[creature.name] = creature

    def remove(self, name: str) -> Creature:
        """Remove and return a creature by name, raising KeyError if not found."""
        if name not in self._creatures:
            raise KeyError(f"No creature named {name!r} in the stable")
        return self._creatures.pop(name)

    def get(self, name: str) -> Creature:
        """Return a creature by name without removing it, raising KeyError if not found."""
        if name not in self._creatures:
            raise KeyError(f"No creature named {name!r} in the stable")
        return self._creatures[name]

    def available_by_power(self) -> StableIterator:
        """Return a StableIterator over in-stable creatures, sorted by power descending."""
        available = [c for c in self._creatures.values() if not c.on_mission]
        available.sort(key=lambda c: c.power_level, reverse=True)
        return StableIterator(available)

    def sorted(self, strategy: SortStrategy) -> list[Creature]:
        """Return a new sorted list using the given SortStrategy; does not modify the stable."""
        return strategy.sort(list(self._creatures.values()))

    def __len__(self) -> int:
        """Return the number of creatures currently registered in the stable."""
        return len(self._creatures)

    def __contains__(self, name: object) -> bool:
        """Return True if a creature with the given name is in the stable."""
        return name in self._creatures

    def __iter__(self) -> Iterator[Creature]:
        """Iterate over all creatures in the stable."""
        return iter(self._creatures.values())

    def __getitem__(self, name: str) -> Creature:
        """Return a creature by name using bracket notation."""
        return self.get(name)

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the stable."""
        return f"Stable({list(self._creatures.keys())})"