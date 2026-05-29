"""
mythical_stable.patterns.observers
=====================================
Observer pattern — a decoupled publish/subscribe event bus.

Publishers emit named events; listeners subscribe to the events they care about
and are called automatically. Neither side knows about the other directly, which
eliminates coupling between the dispatching logic and the notification/audit logic.
"""

from __future__ import annotations

from datetime import datetime
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from mythical_stable.core.mission_record import MissionRecord


class EventBus:
    """Publish/subscribe event bus — decouples publishers from listeners."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable]] = {}

    def subscribe(self, event: str, fn: Callable) -> None:
        """Register fn to be called whenever event is published."""
        self._listeners.setdefault(event, []).append(fn)

    def publish(self, event: str, payload) -> None:
        """Call every subscriber registered for event with payload."""
        for fn in self._listeners.get(event, []):
            fn(payload)


# ── Built-in listener functions ───────────────────────────────────────────────

def audit_logger(payload) -> None:
    """Print a timestamped audit line for any event payload."""
    print(f"[AUDIT {datetime.now():%H:%M:%S}] {payload}")


def overdue_checker(record: "MissionRecord") -> None:
    """Warn if the recalled mission record was overdue."""
    if record.is_overdue:
        print(f"⚠️  OVERDUE: {record.creature_name} was due back on {record.return_date}")