class SortStrategy(Protocol):
    def sort(self, creatures: list[Creature]) -> list[Creature]: ...

class SortByPower:
    """Sort creatures by power_level descending."""
    def sort(self, creatures: list[Creature]) -> list[Creature]:
        return sorted(creatures, key=lambda c: c.power_level, reverse=True)

class SortByName:
    """Sort creatures alphabetically by name."""
    def sort(self, creatures: list[Creature]) -> list[Creature]:
        return sorted(creatures, key=lambda c: c.name)

class SortByAvailability:
    """Sort in-stable creatures first, then those on missions."""
    def sort(self, creatures: list[Creature]) -> list[Creature]:
        return sorted(creatures, key=lambda c: (not c._in_stable, c.name))