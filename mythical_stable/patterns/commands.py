"""
mythical_stable.patterns.commands
===================================
Command pattern — encapsulate requests as reversible objects.

Each command captures everything needed to execute and undo an action.
CommandHistory maintains a stack of executed commands and supports undo/redo.

The Command Protocol is defined in mythical_stable.protocols. DispatchCommand
and RecallCommand satisfy it structurally.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mythical_stable.services.mission_service import MissionService

class DispatchCommand:
    """Dispatch a creature on a mission. Undoable by recalling."""

    def __init__(
            self,
            service: "MissionService",
            name: str,
            destination: str,
            days: int,
    ) -> None:
        self._service = service
        self._name = name
        self._destination = destination
        self._days = days

    def execute(self) -> None:
        """Dispatch the creature."""
        self._service.dispatch(self._name, self._destination, self._days)

    def undo(self) -> None:
        """Undo by recalling the creature."""
        self._service.recall(self._name)


class RecallCommand:
    """Recall a creature from its mission. Undoable by re-dispatching."""

    def __init__(self, service: "MissionService", name: str) -> None:
        self._service = service
        self._name = name
        # Snapshot destination + duration so undo can reproduce the dispatch
        record = service._active.get(name)
        self._destination = record.destination if record else "Unknown"
        self._days = record.duration_days if record else 1

    def execute(self) -> None:
        """Recall the creature."""
        self._service.recall(self._name)

    def undo(self) -> None:
        """Undo by re-dispatching the creature with the original parameters."""
        self._service.dispatch(self._name, self._destination, self._days)


class CommandHistory:
    """Stack of executed commands. Supports single-step undo and redo."""

    def __init__(self) -> None:
        self._stack: list = []
        self._redo_stack: list = []

    def execute(self, cmd) -> None:
        """Execute cmd and push it onto the history stack."""
        cmd.execute()
        self._stack.append(cmd)
        self._redo_stack.clear()  # new action invalidates redo history

    def undo_last(self) -> None:
        """Undo the most recent command. Raises IndexError if nothing to undo."""
        if not self._stack:
            raise IndexError("Nothing to undo.")
        cmd = self._stack.pop()
        cmd.undo()
        self._redo_stack.append(cmd)

    def redo_last(self) -> None:
        """Redo the most recently undone command. Raises IndexError if nothing to redo."""
        if not self._redo_stack:
            raise IndexError("Nothing to redo.")
        cmd = self._redo_stack.pop()
        cmd.execute()
        self._stack.append(cmd)

