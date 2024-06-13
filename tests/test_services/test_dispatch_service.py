from src.services.dispatch_service import DispatchService
from src.subscriber import Subscriber


class FakeSubscriber(Subscriber):
    def __init__(self):
        self.events_handled = []

    def on_event(self, event, *args, **kwargs):
        self.events_handled.append((event, args, kwargs))


class TestDispatchService:
    def test_subscribe_adds_subscriber(self):
        dispatch_service = DispatchService()
        subscriber = FakeSubscriber()
        dispatch_service.subscribe(subscriber)
        assert subscriber in dispatch_service._subscribers

    def test_dispatch_notifies_subscriber(self):
        dispatch_service = DispatchService()
        subscriber = FakeSubscriber()
        dispatch_service.subscribe(subscriber)
        dispatch_service.dispatch("test_event", 42, key="value")
        assert subscriber.events_handled == [("test_event", (42,), {"key": "value"})]

    def test_dispatch_multiple_subscribers(self):
        dispatch_service = DispatchService()
        subscriber1 = FakeSubscriber()
        subscriber2 = FakeSubscriber()
        dispatch_service.subscribe(subscriber1)
        dispatch_service.subscribe(subscriber2)
        dispatch_service.dispatch("test_event")
        assert len(subscriber1.events_handled) == 1
        assert len(subscriber2.events_handled) == 1
