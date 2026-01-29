from typing import Dict, List
from event_pipeline.models import Event


class EventRegistry:
    def __init__(self):
        self._events: Dict[str, List[Event]] = {}

    def add(self, event: Event):
        self._events.setdefault(event.type, []).append(event)

    def all(self) -> Dict[str, List[Event]]:
        return self._events


registry = EventRegistry()
