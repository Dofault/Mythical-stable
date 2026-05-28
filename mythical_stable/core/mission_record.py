"""Mission record dataclass tracking a single creature deployment."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class MissionRecord:
    """A record of a single creature mission, from departure to return."""

    creature_name: str
    destination: str
    duration_days: int
    departure_date: date = field(default_factory=date.today)
    notes: str = ""
    _closed: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        """Validate destination and duration_days on creation."""
        if not self.destination.strip():
            raise ValueError("destination must not be empty")
        if self.duration_days <= 0:
            raise ValueError("duration_days must be a positive integer")

    @property
    def return_date(self) -> date:
        """Return the expected return date (departure_date + duration_days)."""
        return self.departure_date + timedelta(days=self.duration_days)

    @property
    def is_overdue(self) -> bool:
        """Return True if the mission is still active and past its return date."""
        if self._closed:
            return False
        return date.today() > self.return_date

    def close(self) -> None:
        """Mark this mission record as closed (creature has returned)."""
        self._closed = True

    def __eq__(self, other: object) -> bool:
        """Two records are equal if they share the same creature_name and departure_date."""
        if not isinstance(other, MissionRecord):
            return NotImplemented
        return self.creature_name == other.creature_name and self.departure_date == other.departure_date

    def __hash__(self) -> int:
        """Hash based on creature_name and departure_date."""
        return hash((self.creature_name, self.departure_date))