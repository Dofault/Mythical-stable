class EventBus:
    """Publish/subscribe event bus — decouples publishers from listeners."""

    def __init__(self) -> None:
        self._listeners: dict[str, list] = {}

    def subscribe(self, event: str, fn) -> None:
        self._listeners.setdefault(event, []).append(fn)

    def publish(self, event: str, payload) -> None:
        for fn in self._listeners.get(event, []):
            fn(payload)

# Listener functions — plain functions are valid listeners
def audit_logger(payload) -> None:
    from datetime import datetime
    print(f'[AUDIT {datetime.now():%H:%M:%S}] {payload}')

def overdue_checker(record: MissionRecord) -> None:
    if record.is_overdue:
        print(f'⚠️  OVERDUE: {record.creature_name} was due back on {record.return_date}')