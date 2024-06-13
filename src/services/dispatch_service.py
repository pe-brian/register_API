from ..injector import declare
from ..service import Service
from ..subscriber import Subscriber


@declare
class DispatchService(Service):
    """Dispatch service"""

    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber: Subscriber) -> None:
        """Add a subscriber"""
        if not subscriber in self._subscribers:
            self._subscribers.append(subscriber)

    def dispatch(self, event: str, *args, **kwargs) -> None:
        """Dispatch an event to the subscriber"""
        for subscriber in self._subscribers:
            subscriber.on_event(event, *args, **kwargs)
