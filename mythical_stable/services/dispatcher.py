


class MissionDispatcher:
    def __init__(self, notifier: MissionNotifier) -> None:
        self._notifier = notifier

    def dispatch(self, creature_name: str, destination: str) -> None:
        # Sends the creature on the mission and notifies via the injected notifier
        self._notifier.notify(f"🐉 {creature_name} dispatched to {destination}.")