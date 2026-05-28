class Command(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...

class DispatchCommand:
    """Dispatch a creature on a mission. Undoable with recall."""

    def __init__(self, service: MissionService, name: str, destination: str, days: int) -> None:
        self._service     = service
        self._name        = name
        self._destination = destination
        self._days        = days

    def execute(self) -> None:
        self._service.dispatch(self._name, self._destination, self._days)

    def undo(self) -> None:
        self._service.recall(self._name)

class CommandHistory:
    """Stack of executed commands. Supports single-level undo."""

    def __init__(self) -> None:
        self._stack: list[Command] = []

    def execute(self, cmd: Command) -> None:
        cmd.execute()
        self._stack.append(cmd)

    def undo_last(self) -> None:
        if not self._stack:
            raise IndexError('Nothing to undo.')
        self._stack.pop().undo()