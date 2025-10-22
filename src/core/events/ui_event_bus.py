"""
Simple UI Event Bus
Used to decouple domain objects from UI signal emission. Domain elements can publish
change events to this bus; UI adapters can subscribe and re-emit as Qt signals.
"""
from typing import Callable, Dict, List, Any


class UIEventBus:
    """A minimal publish/subscribe bus for UI-related domain change events."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_name: str, callback: Callable[[Any], None]) -> None:
        """Subscribe a callback to an event name."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        if callback not in self._subscribers[event_name]:
            self._subscribers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable[[Any], None]) -> None:
        """Unsubscribe a callback from an event name."""
        if event_name in self._subscribers and callback in self._subscribers[event_name]:
            self._subscribers[event_name].remove(callback)

    def publish(self, event_name: str, payload: Any) -> None:
        """Publish an event to all subscribers."""
        for callback in list(self._subscribers.get(event_name, [])):
            try:
                callback(payload)
            except Exception:
                # Keep UI bus robust — swallow exceptions from listeners
                continue
